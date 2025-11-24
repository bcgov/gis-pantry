# Original script downloaded from
# https://community.esri.com/t5/arcgis-online-documents/overwrite-arcgis-online-feature-service-using-truncate-and/ta-p/904457
# Original script author: Jake Skinner, ESRI
# Modified to allow calling overwrite function outside of this script



import time
print("Importing modules: arcpy, os, sys getpass, zipfile, arcgis")
import arcpy, os, sys, getpass
from zipfile import ZipFile
from arcgis.gis import GIS

class AGO(object):
    """
    This class can be used to overwrite existing Feature Services/Feature Layers in ArcGIS Online
    Steps:
    0.Log into AGO, create GIS object that allows us to communicate with AGO (in __init__ method)
    1.export the feature class to a temporary File Geodatabase/assign the type of input
    2.zip the File Geodatabase
    3.upload the zipped File Geodatabase to AGOL
    4.truncate the feature service
    5.append the zipped File Geodatabase to the feature service
    6.delete the uploaded zipped File Geodatabase in AGOL
    7.delete the local zipped File Geodatabase
    8.delete the temporary File Geodatabase
    """
    def __init__(self,username,password):
        self.username=username.upper()
        # Create GIS object
        self.gis = GIS("https://www.arcgis.com", self.username,password)

    def overwrite(self, input_path, featurelayer_id):
        arcpy.env.overwriteOutput = True
        print(f"Overwrite of {input_path} start time: \n"+ time.ctime())
        startTime = time.time()
        
        premiseLayer = self.gis.content.get(featurelayer_id)
        
        def inputType(input_path):
            desc = arcpy.Describe(input_path)
            fcDataType = desc.dataType 
            print("Data type: ", fcDataType) 
            
            if fcDataType in ("FeatureClass","ShapeFile"):
                arcpy.conversion.FeatureClassToFeatureClass(input_path, os.path.join(arcpy.env.scratchFolder, "TempGDB.gdb"), fcName)
                self.fLyr = premiseLayer.layers[0]
            
            elif fcDataType == "Table":
                arcpy.conversion.TableToTable(input_path, os.path.join(arcpy.env.scratchFolder, "TempGDB.gdb"), fcName)
                self.fLyr = premiseLayer.tables[0]
            else:
                print('Input is not a feature class, shapefile or a table. This script is not going to work on this input! Or maybe it will if you change it :)')
                sys.exit(1)

        # Function to Zip FGD
        def zipDir(dirPath, zipPath):
            zipf = ZipFile(zipPath , mode='w')
            gdb = os.path.basename(dirPath)
            for root, _ , files in os.walk(dirPath):
                for file in files:
                    if 'lock' not in file:
                        filePath = os.path.join(root, file)
                        zipf.write(filePath , os.path.join(gdb, file))
            zipf.close()

        print("Creating temporary File Geodatabase")
        arcpy.CreateFileGDB_management(arcpy.env.scratchFolder, "TempGDB")

        # Export feature classes to temporary File Geodatabase
        fcName = os.path.basename(input_path)
        fcName = fcName.split('.')[-1]
        print(f"Exporting {fcName} to temp FGD")
        
        #check the input type, convert to FGD and assign appropriate call for online lyr
        inputType(input_path)

        # Zip temp FGD
        print("Zipping temp FGD")
        zipDir(os.path.join(arcpy.env.scratchFolder, "TempGDB.gdb"), os.path.join(arcpy.env.scratchFolder, "TempGDB.gdb.zip"))

        # Check if FGD exists, if True, delete item
        searchResults = self.gis.content.search(f'title:tempFGD AND owner:{self.username}', item_type='File Geodatabase')
        if len(searchResults) > 0:
            item = searchResults[0]
            item.delete()

        # Upload zipped File Geodatabase
        print("Uploading File Geodatabase")
        fgd_properties={'title':'tempFGD', 'tags':'temp file geodatabase', 'type':'File Geodatabase'}
        fgd_item = self.gis.content.add(item_properties=fgd_properties, data=os.path.join(arcpy.env.scratchFolder, "TempGDB.gdb.zip"))

        # Truncate Feature Service
        print("Truncating Feature Service")
        self.fLyr.manager.truncate()

        # Append features from feature class
        print("Appending features")
        self.fLyr.append(item_id=fgd_item.id, upload_format="filegdb", upsert=False, field_mappings=[])

        # Delete Uploaded File Geodatabase
        print("Deleting uploaded File Geodatabase")
        fgd_item.delete()

        # Delete temporary File Geodatabase and zip file
        print("Deleting temporary FGD and zip file")
        arcpy.Delete_management(os.path.join(arcpy.env.scratchFolder, "TempGDB.gdb"))
        os.remove(os.path.join(arcpy.env.scratchFolder, "TempGDB.gdb.zip"))

        elapsedTime = round((time.time() - startTime) / 60, 2)
        print(f"Overwrite using {input_path} finished in {elapsedTime} minutes")



if __name__ == "__main__":
    #path to the feature class to be used to overwrite online feature service
    input_path="" 
    #itemid of the online feature class to overwrite e.g. "5e3e867ebf4940c4b100cc4dc977b011"
    featurelayer_id ="" 

    username = input("AGO Username: ")
    password = getpass.getpass()
    #instantiate class with your username; you will be prompted to enter password
    ago_obj=AGO(username,password)
    
    ago_obj.overwrite(input_path,featurelayer_id)

