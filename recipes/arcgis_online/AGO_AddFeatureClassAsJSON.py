###=============================================================================================================================================
### AGO_AddFeatureClassAsJSON.py
###     Created: 2019-08-06 (YYYY-MM-DD format) (Michael.Dykes@gov.bc.ca)
###     Edited: 2020-05-29 (YYYY-MM-DD format) (Gregory.Amos@gov.bc.ca)
###
###     Purpose: Add Content to ArcGIS Online from File Geodatabase (as GeoJSON)
###=============================================================================================================================================

""" This script uploads all feature classes in a given file geodatabase (.gdb) to your ArcGIS Online (AGO) content page.
It requires the ArcGIS Pro Python environment to run (needs access to arcgis.gis module).
The ArcGIS Pro Python environment can be found on the BCGOV Geospatial Desktop."""

# See: ESRI documentation: https://developers.arcgis.com/python/guide/accessing-and-managing-groups/
# See also:                https://github.com/Esri/arcgis-python-api
# This is old, don't use:  https://github.com/Esri/ago-tools/tree/master/samples

from arcgis.gis import GIS # ArcGIS API for Python
import arcpy, os, sys, time
# import getpass

################################################################################
def makeFolder(folder): 
    if not os.path.exists(folder):
        os.mkdir(folder)
        print("{} created.".format(folder))

################################################################################

# Geodatabase Path
gdb = r'W:\FOR\RSI\DKL\General_User_Data\test.gdb' # feature class

# Enter your AGO username and password
username = input("Enter AGO username (it is case-sensitive): ") # Username is case sensitive!
password = input("Enter AGO password : ")

arcpy.env.workspace = gdb
arcpy.env.overwriteOutput = True

# Iterate through geodatabase Feature Classes
outFolder = r"T:\_test"
makeFolder(outFolder) # FUNCTION CALL

for fc in arcpy.ListFeatureClasses():
    print(fc, type(fc))
    count = 1

    # Check feature classes
    if int(arcpy.GetCount_management(fc).getOutput(0)) != 0: # don't upload empty feature classes
    # if int(arcpy.GetCount_management(fc).getOutput(0)) == 0: # upload empty feature classes only

        # Create temporary JSON file:
        # JSON FilePath & FileName & Extension *Note: AGO Doesn't Accept Duplicate FileNames*
        # jsonfilepath = r"S:\Gis\Python\AGO\Python_Host\\" + "json_file" + fc + ".geojson"
        # jsonFilePath = r"W:\FOR\RSI\DKL\General_User_Data\gamos\GREG_JSONs_for_AGO\fc_{}.geojson".format(fc)
        # jsonFilePath = r"T:\_test\fc_{}.geojson".format(fc)
        jsonFilePath = os.path.join(outFolder, "fc_{}_{}.geojson".format(fc, count))

        # Buid Feature Class Path for Input into Geoprocessing Tool
        FeatureClass = str(os.path.join(arcpy.env.workspace, fc))
        featureLayer = arcpy.MakeFeatureLayer_management(FeatureClass,"in_memory/_fl")
        
        # Ensure the JSON file you are uploading to AGO is new (to prevent a "RuntimeError: Item 'xyz' already exists" when executing fc_item.publish() )
        while os.path.exists(jsonFilePath):
            jsonFilePath = os.path.join(outFolder, "fc_{}_{}.geojson".format(fc, count+1))
        print("JSON to write: {}".format(jsonFilePath))

        # Convert FC to GeoJSON
        geojsonfile = arcpy.FeaturesToJSON_conversion(featureLayer, jsonFilePath, geoJSON="GEOJSON")

        # Connect to GovernmentofBC AGO Portal
        # Syntax: arcgis.gis.GIS(url=None, username=None, password=None, key_file=None, cert_file=None, verify_cert=True, set_active=True, client_id=None, profile=None, **kwargs)
        ago_gis = GIS('https://governmentofbc.maps.arcgis.com/',username,password)
        print("Logged in as {}".format(ago_gis.properties.user.username))
        print("Other info:\n{}\n".format(ago_gis.properties.user))

        theGroup = ago_gis.groups.search('title:Invasive Plant Program ', max_groups=10)
        if len(theGroup) == 1:
            targetGroup = theGroup[0] # you want to upload the feature layer to one specific group
            print(targetGroup, type(targetGroup))

        # Item Properties (Dictionary format). Type is Important for AGO to recognize the Data Format
        # Title must not be the same as the name of the feature class (this causes an error), so append the upload date to it.
        itemPropertiesDict = {'title':'{}_{}'.format(fc, time.strftime("%Y_%m_%d")),  
                            'tags':'fc_upload',
                            'type': 'GeoJson'}

        # Set AGO Item Properties and Add Content (Can add 'folder=*foldername*' Parameter to Add Content Directly to Existing AGO Folder)
        # Syntax: add(item_properties, data=None, thumbnail=None, metadata=None, owner=None, folder=None)
        # For more, see: https://developers.arcgis.com/python/api-reference/arcgis.gis.toc.html#contentmanager

        # fc_item = ago_gis.content.add(item_properties=itemPropertiesDict, data=jsonFilePath,  folder=targetGroup) # AttributeError: 'Group' object has no attribute 'upper'
        # fc_item = ago_gis.content.add(item_properties=itemPropertiesDict, group=targetGroup, data=jsonFilePath) # 'group' keyword argument doesn't exists in add()
        # fc_item = ago_gis.content.add(item_properties=itemPropertiesDict, data=jsonFilePath, thumbnail=None, metadata=None, owner=None, folder=targetGroup) # KeyError: 'upper'
        # fc_item = ago_gis.content.add(item_properties=itemPropertiesDict, data=jsonFilePath, folder="Test_folder") # KeyError: 'type'
        print("Check jsonFilePath: {}".format(jsonFilePath))
        fc_item = ago_gis.content.add(item_properties=itemPropertiesDict, data=jsonFilePath) # works, as long as your FC has features; doesn't work for empty FCs

        try:
            fc_layer = fc_item.publish() # You'll get an error code 409 if that item is already in AGO
        except RuntimeError as e:
            print(e)
        except KeyError as e:
            print(e)

        print("{} published to gamos".format(fc))
        # print("{} published to {}".format(fc, targetGroup))

    # Delete JSON File
    os.remove(jsonFilePath)
    print("Deleted temp JSON file: {}".format(jsonFilePath))

print("\nAll AGO uploads complete.")