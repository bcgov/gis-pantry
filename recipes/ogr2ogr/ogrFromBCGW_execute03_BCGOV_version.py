# ogrFromBCGW_execute_BCGOV_version.py
# gamos 14/11/2019 (DD/MM/YY format)
# Gregory.Amos@gov.bc.ca
# GIS Technician (auxiliary) / Kootenay Boundary Region / Ministry of Forests, Lands and Natural Resource Operations and Rural Development


# Script to create and execute an ogr2ogr CLI string - i.e translate a BCGW subset into one of several geospatial formats

# CHECK THESE THINGS BEFORE RUNNING SCRIPT:
# 1. Make sure "outPath" exists 
# 2. Fill in your BCGW credentials for user, pWord (Line 21)

# Most BCGW datasets are in BC Albers; default output is in BC Albers projection with coordinates to nearest 0.1 metres

# Output data types this script allows: GeoJSON, KML, ESRI Shapefile, and GeoPackage (QGIS' native format)

import os
import sys
import subprocess

user, pWord = "USERNAME", "BCGW_PASSWORD"

# # Usage example 1 - create a KML for a single wildfire, with  FIRE_NUMBER as only attribute, write it to a T: folder
# outPath, outName, outType = r"T:\testFolder", r"fireKML_99", "KML" 
# sqlQuery = "select FIRE_NUMBER, SHAPE from WHSE_LAND_AND_NATURAL_RESOURCE.PROT_HISTORICAL_FIRE_POLYS_SP where FIRE_NUMBER ='N40101'"

# # Usage example 2 - create an ESRI Shapefile all wildfires in Southeast zone in 2018, preserve all attributes, write it to T: folder
# outPath, outName, outType = r"T:\testFolder", r"fires_2018", "ESRI Shapefile" 
# sqlQuery = "select * from WHSE_LAND_AND_NATURAL_RESOURCE.PROT_HISTORICAL_FIRE_POLYS_SP where FIRE_YEAR = 2018 and FIRE_NUMBER like 'N%'"

# # Usage example 3 - create a GeoPackage file for a TSA in the Kootenay Boundary Region; write it to folder on GeoBC FTP site 
# tDict = {'Arrow TSA':1, 'Boundary TSA':2, 'Cranbrook TSA':5, 'Golden TSA':7, 'Invermere TSA':9, 'Kootenay Lake TSA':13, 'Revelstoke TSA':27 } # for reference
# outPath = r"\\ftpgeobc.nrs.bcgov\ftpgeobc\pub\outgoing\GeoBC_Regional\Kootenay_Boundary"
# outName, outType = r'Cranbrook TSA', "GPKG"
# sqlQuery = r"select * from WHSE_ADMIN_BOUNDARIES.FADM_TSA where TSB_NUMBER is null AND RETIREMENT_DATE IS NULL AND TSA_NUMBER = {}".format(tDict['Cranbrook TSA'])

# # Usage example 4 - IN PROGRESS - creates a JSON file of highway rest stops in WGS 84 (geographic coordinates), write it to a T: folder
# In this case, script must know the in CRS and outCRS to correctly transform
# outCRS = 4326
# outPath, outName, outType = r"T:\testFolder", r"rest_stops_GC", "GeoJSON"
# sqlQuery = "select * from WHSE_IMAGERY_AND_BASE_MAPS.MOT_REST_AREAS_SP"

# Usage example 5 - IN PROGRESS - example of ogr2ogr trickines with SQL statements...
# create an ESRI Shapefile for several TSAs in Kootenay Boundary Region, write it to a project folder 
# tDict = {'Arrow TSA':r'01', 'Boundary TSA':r'02',  'Kootenay Lake TSA':r'13'} # for reference
# outPath = r"W:\FOR\RSI\DKL\General_User_Data\gamos\Projects\2019\OGR_tests"
# outName, outType = r"zRKB_TSAs_01", "ESRI Shapefile"
# tsaString = "('{}','{}','{}')".format(tDict['Arrow TSA'], tDict['Boundary TSA'], tDict['Kootenay Lake TSA'])
# # sqlQuery = "select * from WHSE_ADMIN_BOUNDARIES.FADM_TSA where TSA_NUMBER IN {} AND TSB_NUMBER is null AND RETIREMENT_DATE IS NULL".format(tsaString)
# sqlQuery2 = "select * from WHSE_ADMIN_BOUNDARIES.FADM_TSA where TSB_NUMBER is null AND RETIREMENT_DATE IS NULL AND TSA_NUMBER IN {}".format(tsaString)
# print(sqlQuery)


def ogrFromBCGW(outType, outPath, outName, user, pword, sqlQuery, outCRS = 3005, coordPrec = 1):
    epsgDict = {3005: "BC Albers", 3741: "NAD83(HARN) / UTM zone 11N", 4326:'WGS 84', 104199:"GCS_WGS_1984_Major_Auxiliary_Sphere"}
    extDict = {"GeoJSON":".json", "KML":".kml", "ESRI Shapefile":".shp", "GPKG":".gpkg"}

    ogrList = []
    osgeo_bat, ogr_exe = r"E:\sw_nt\QGIS_3.4\OSGeo4W.bat", r'E:\sw_nt\QGIS_3.4\bin\ogr2ogr.exe'
    specifySRS, srs_def = '-a_srs','epsg:{}'.format(outCRS)
    f, formatName, fileName = '-f', outType, os.path.join(outPath, outName) + extDict[outType]
    ds = "OCI:{}/{}@IDWPROD1:junk".format(user,pword)
    # sql, sqlQuery, progress  = '-sql', sqlQuery,'-progress'
    progress, sql, sqlQuery  = '-progress', '-sql', sqlQuery

    for x in [osgeo_bat, ogr_exe, specifySRS, srs_def, f, formatName, fileName, ds, progress, sql, sqlQuery]:
        ogrList.append(x)
    # OLD: fullString = r'ogr2ogr -a_srs epsg:{} -f "{}" {}\{}{} {} -sql "{}" -progress'.format(outCRS, outType, outPath, outName, extDict[outType], ociString, sqlQuery)

    if outType == "GeoJSON": # Set GeoJSON specific options
        for x in ["-lco","WRITE_NAME=NO"]: # lco = layer creation option - prevents JSON layer from assuming entire sqlQuery as its name 
            ogrList.append(x)

    if outType == "GPKG": # Set GPKG specific options
        for x in ["-lco","IDENTIFIER='layer1'","-lco","DESCRIPTION='layer1'"]: # ensures layer name = "layer1" in the GPKG file.
            ogrList.append(x) 

    if outType == "KML": # Set KML specific options 
        # fullString += " -dsco NameField= '{}'".format(outName) # prevents the KML layer from assuming the entire sqlQuery as its name 
        for x in ["-nln","{}".format(outName)]: # -nln = "New Layer Name"; prevents the KML layer from assuming the entire sqlQuery as its name
            ogrList.append(x) 

    # If outCRS is WGS 84, set high coordinate precision (13 decimal places)
    # if any([outCRS != 4326, outType == "KML"]): # 4326 = WGS84 = decimal degrees, which needs as many decimal places as possible . KML driver ourCRS is always 4326
    #     coordPrec = 13
    #     for x in ["-lco","COORDINATE_PRECISION={}".format(coordPrec)]:
    #         ogrList.append(x)       

    if outCRS in epsgDict:
        if outType == "KML":
            crsMessage = "\n\nResultant spatial file (KML) always has CRS:{} ({})\n".format(4326, epsgDict[4326])
        else:
            crsMessage = "\n\nResultant spatial file will have CRS:{} ({})\n".format(outCRS, epsgDict[outCRS]) 
        print(crsMessage)
    
    # Error trapping section; needs work!
    # try:
    #     subprocess.run(ogrList)
    # # except "ERROR 1: ORA-00972": # this is an error you get when cmd.exe cannot interpret your SQL statement; often a value is wrong
    # except subprocess.CalledProcessError as e:
    #     print(str(e.output))
    #     # print("weird error")
    #     sys.exit()
    # return ogrList

    subprocess.run(ogrList)
    return ogrList

########################################################################

ogrList = ogrFromBCGW(outType, outPath, outName, user, pWord, sqlQuery)
print("\nArguments:\n", ogrList)