import os
import numpy as np
import pandas as pd
from osgeo import ogr
from osgeo import gdal, gdal_array
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report


#-------------------------------------------------------#
# Prepare the imagery dataset
#-------------------------------------------------------#


def MakeImageComposite (imagery_folder):
    """Returns a multiband image based on Sentinel-2 imagery folder"""
    #Browse through the S2 product folder and retrieve the required bands.
    #Change depending on your input features
    S2_bands = []
    for root, dirs, files in os.walk(imagery_folder):
        for name in files:
            if name.endswith("B02_10m.jp2"):
                Bpath = os.path.join (root, name)
                S2_bands.append(Bpath)
            elif name.endswith("B03_10m.jp2"):
                Gpath = os.path.join (root, name)
                S2_bands.append(Gpath)
            elif name.endswith("B04_10m.jp2"):
                Rpath = os.path.join (root, name)
                S2_bands.append(Rpath)
            elif name.endswith("B08_10m.jp2"):
                NIRpath = os.path.join (root, name)
                S2_bands.append(NIRpath)            
            elif name.endswith("B11_20m.jp2"):
                SWIR1path = os.path.join (root, name)
                S2_bands.append(SWIR1path)
            elif name.endswith("B12_20m.jp2"):
                SWIR2path = os.path.join (root, name)  
                S2_bands.append(SWIR2path)
            else:
                pass
          
    print ('{nBands} Bands retrieved from the Sentinel-2 imagery folder' .format(nBands = len(S2_bands)))
    
    #Stack the bands into a Composite Image
    outvrt = '/vsimem/stacked.vrt' #/vsimem is special in-memory gdal virtual "directory"
    
    imgComp = os.path.join (workspace, 'inputs','S2A_' + os.path.basename(Gpath)[:15] + '_Band_Composite.tif')
    VrtOptions = gdal.BuildVRTOptions(resolution = 'lowest', separate=True)
    outds = gdal.BuildVRT(outvrt, S2_bands, options = VrtOptions)
    translate_options = gdal.TranslateOptions(format = 'GTiff', 
                                              creationOptions = ['COMPRESS=LZW',
                                                                 'BIGTIFF=YES'])
    outds = gdal.Translate(imgComp, outds, options=translate_options)

    print ('S2 Band Composite created!')
    
    return imgComp


#-------------------------------------------------------#
# Convert the training data from SHP to Raster
#-------------------------------------------------------#


def CreateROIraster (imgComp, roi_shp_path):
    """Returns training data in raster format based on shp input"""
    try:
        global img_ds
        img_ds = gdal.Open(imgComp)
        shp_ds = ogr.Open(roi_shp_path)
        print('Dataset successfully opened!')
    
    except:
        print('Error: could not open dataset!')  
    
    #Fetch the proprities of the imagery raster. this will be used as template for the new ROI raster.
    #Nbr of columns and rows, spatial ref and extent
    global ncol    
    ncol = img_ds.RasterXSize
    global nrow
    nrow = img_ds.RasterYSize
    global proj
    proj = img_ds.GetProjectionRef()
    global ext
    ext = img_ds.GetGeoTransform()
    
    #Create a new raster dataset
    roi_raster = os.path.join (workspace, 'outputs','training_data.tif')
    driver = gdal.GetDriverByName('GTiff')
    roi_raster_ds = driver.Create(roi_raster, 
                                  ncol, 
                                  nrow, 
                                  1, 
                                  gdal.GDT_Byte)
    
    #Set the projection and extent of the new ROI raster
    roi_raster_ds.SetProjection(proj)
    roi_raster_ds.SetGeoTransform(ext)
    
    #Fill the first (and only) band of the new ROI raster with value 0
    band = roi_raster_ds.GetRasterBand(1)
    band.Fill(0)
    
    #Get the first (and only layer) of the ogr shapefile dataset
    layer = shp_ds.GetLayerByIndex(0)
    
    #Run the rasterize task.
    try:
        gdal.RasterizeLayer(roi_raster_ds,  # output to our new dataset
                                 [1],  # output to our new dataset's first band
                                 layer,  # rasterize this layer
                                 None, None,  # No need to set transformations since we're in same projection
                                 [0],  # burn value 0
                                 ['ALL_TOUCHED=TRUE',  # rasterize all pixels touched by polygons
                                  'ATTRIBUTE=Id']  # put raster values according to the 'id' field values
                                 )
        roi_raster_ds = None 
        print ('ROI raster created successfully!')
        
    except:
        print ('Error: could not create ROI raster!')
    
    return roi_raster


#-------------------------------------------------------#
# Prepare inputs (Arrays) for the Model
#-------------------------------------------------------#
    

def PrepareArrays (roi_raster):
    """Returns model inputs: feature and label arrays""" 
    roi_ds = gdal.Open(roi_raster) 
    
    ##Create an Array containing the S2 imagery bands
    # create an empty Array
    global img
    img = np.zeros((nrow, ncol, img_ds.RasterCount),
                   gdal_array.GDALTypeCodeToNumericTypeCode(img_ds.GetRasterBand(1).DataType))
     
    #Fill the Array using pixel values from bands
    for band in range(img.shape[2]):
        print ('Adding pixel values from band {b}'. format (b = band + 1))
        img[:, :, band] = img_ds.GetRasterBand(band + 1).ReadAsArray() #Array index starts at 0, Band nbr starts at 1...so we add 1 to each band call.   
        
    #Check if the image has now all the bands
    print ("The image shape is: {shape}" .format (shape = img.shape))  
    
    #Create another Array for the ROI raster
    roi = roi_ds.GetRasterBand(1).ReadAsArray().astype(np.uint8)
    
    #Check how many traning samples (pixels) we have 
    n_samples = (roi > 0).sum()
    print('The ROI has {n} samples'.format(n=n_samples))
        
    #Check how many Classes in the ROI Array   
    labels = np.unique(roi[roi > 0]) 
    print('The training data include {n} classes: {classes}'.format(n=labels.size, classes=labels))
    
    #Pair the Image array with the ROI Array
    #The Random Forest Classifier needs 2 input Arrays: One (X) containing the samples (training pixel values) and another one (y) containing the Class labels
    X = img[roi > 0] #This extracts the img pixels that have a corresponding roi value (label) - Predictors/Feature
    y = roi[roi > 0] #This creates an roi Array that has the class lables [1,2,3,4] - Response/Labels
    
    print('The X (feature) Array size is: {s}'.format(s=X.shape))
    print('The y (labels) Array size is: {s}'.format(s=y.shape))
    
    return X,y


#-------------------------------------------------------#
# Train and Evaluate the Model (Random Forest in this case)
#-------------------------------------------------------#
    

def TrainModel (X,y):
    """Returns a RF classifier"""
    # Split the data into training and testing sets. Ratio is 80/20%
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)
    
    #Create a Random Forest model with 100 Decision Trees
    model = RandomForestClassifier(n_estimators=100, random_state = 0, class_weight="balanced")

    # Fit our model to training data
    model.fit(X_train, y_train)
    
    ##Evaluate the accuracy of the Model on the Test dataset
    #Predict the Test dataset    
    prediction_test = model.predict(X_test)
    
    #Compute the accuracy score
    accracy_score  = accuracy_score(y_test, prediction_test)
    print('The Prediction acccuracy score is: {Ascore} %'.format(Ascore = accracy_score*100))
    
    #Compute the Classification report
    labels = ['Snow', 'Water', 'No Snow', 'Cloud'] # change depending on your classe names
    cr = classification_report(y_test, prediction_test, target_names=labels)
    print (cr)   
    
    #Compute the Confusion Matrix
    cm = confusion_matrix (y_test, prediction_test)
    #print (cm)
    
    #A better way to compute a Confusion matrix (use Pandas df)
    # Setup a dataframe
    df = pd.DataFrame()
    df['truth'] = y_test
    df['predict'] = prediction_test
    
    # Cross-tabulate predictions
    print(pd.crosstab(df['truth'], df['predict'], margins=True))
    
    #Compute the Feature importance. Importance of each band in the Prediction
    bands = ['B', 'G', 'R', 'NIR', 'SWIR1','SWIR2'] # change depending on your input features
    
    for b, imp in zip(bands, model.feature_importances_):
        print('Band {b} importance: {imp} %'.format(b=b, imp=imp*100))
    
    return model


#-------------------------------------------------------#
# Apply the Model
#-------------------------------------------------------#


def ApplyModel (model):
    """Applies the model to the entire Sentinel-2 image"""
    # Rreshape the full image into long 2d array (nrow * ncol, nband) for classification
    new_shape = (img.shape[0] * img.shape[1], img.shape[2])
    
    img_as_array = img[:, :, :img_ds.RasterCount].reshape(new_shape)
    print('Reshaped from {o} to {n}'.format(o=img.shape,
                                            n=img_as_array.shape))
    
    # Predict for each pixel
    class_prediction = model.predict(img_as_array)
    
    # Reshape the classification back to the original 3D Array format
    class_prediction = class_prediction.reshape(img[:, :, 0].shape)
    
    #Write the output to a new Raster
    #Create a new raster data source
    out_raster_name = os.path.join (workspace, 'outputs','Classification.tif')
    driver = gdal.GetDriverByName('GTiff')
    outDs = driver.Create(out_raster_name, 
                                  ncol, 
                                  nrow, 
                                  1, 
                                  gdal.GDT_Byte)
    
    # Write metadata
    outDs.SetGeoTransform(ext)
    outDs.SetProjection(proj)
    
    # Write raster data sets
    outBand = outDs.GetRasterBand(1)
    outBand.WriteArray(class_prediction)
    
    # Close raster file
    outDs = None 
    
    print ('Classification image created') 
    
    
#-------------------------------------------------------#
# Run the algorithm
#-------------------------------------------------------#
    

#Define paths to input data (imagery and training dataset)
workspace = r'F:\..\RSMachineLearning'
imagery_folder = r'F:\...\S2B_MSIL2A_....SAFE'
roi_shp_path = os.path.join (workspace, 'inputs','training_data.shp')

#Run the functions
def main():
    imgComp = MakeImageComposite (imagery_folder)
    roi_raster = CreateROIraster (imgComp, roi_shp_path)
    X,y = PrepareArrays (roi_raster)
    model = TrainModel (X,y)
    ApplyModel (model)
    print ('Processing Completed!') 

if __name__ == "__main__":
    main()
