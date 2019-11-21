# ogrFromBCGW_BCGOV_FINAL.py
# gamos 19/11/2019 (DD/MM/YY format)
# Gregory.Amos@gov.bc.ca
# GIS Technician (auxiliary) / Kootenay Boundary Region / Ministry of Forests, Lands and Natural Resource Operations and Rural Development

# Script to create and execute an ogr2ogr CLI string - i.e translate a BCGW subset into one of several geospatial formats

"""CHECK/BE AWARE OF THESE THINGS BEFORE RUNNING SCRIPT:
1. Fill in your BCGW credentials for user, pWord (Line 30 or so)
2. It's safe to disregard the 'ERROR 1: ORA-04043: object no_Table does not exist' message that will print to the console - that's just a way of preventing 
    ogr2ogr from scanning all tables in the BCGW once it connects...
3. Most BCGW datasets are in BC Albers; default output is in BC Albers projection with coordinates to nearest 0.1 metres
4. Output data types this script allows: GeoJSON, KML, ESRI Shapefile, and GeoPackage (QGIS' native format). More will be added..
5. If outputting an ESRI Shapefile, it's normal to see 'Warning 6: Normalized/laundered field name:' This makes fields 10 characters long.
"""

# UPDATE_LOG 19/11/2019
# =====================
# 1. Updated paths for OSGeo4W and bin/ogr2ogr.exe - script now works in all DTS desktops
# 2. No more arcpy import
# 3. Better SQL string handling - SQL strings are written to .sql files in T:\tempQueryFolder, then read back in as an ogr2ogr parameter - works much better.
# 4. Added SQL string scrubber to ensure the SQL dialect translates well to ogr2ogr (scrubs any comments)

import os
import sys
import subprocess

# user, pWord = input("Enter your BCGW username:"), input("Enter your BCGW password:")
# user, pWord = "USER", "PASSWORD"

# Usage example 1 - create an ESRI Shapefile all wildfires in Southeast zone in 2018, preserve all attributes, write it to T: folder
outPath, outName, outType = r"T:\testFolder", r"fires_2015+", "ESRI Shapefile"
sqlQuery = r"""select * from WHSE_LAND_AND_NATURAL_RESOURCE.PROT_HISTORICAL_FIRE_POLYS_SP where FIRE_YEAR > 2015 and FIRE_NUMBER like 'N%'"""

# # Usage example 2 - look at all salvage logging in RKB since 2015, preserve all attributes, write KML to T: folder
# outPath, outName, outType = r"T:\testFolder", r"salvage_logs", "KML"
# sqlQuery = r"""select * from WHSE_FOREST_TENURE.FTEN_CUT_BLOCK_POLY_SVW
# where BLOCK_STATUS_DATE > '01-JAN-15'
# and LIFE_CYCLE_STATUS_CODE IN ('ACTIVE','PENDING')
# and GEOGRAPHIC_DISTRICT_CODE IN ('DSE','DRM')
# and (UPPER(CUT_BLOCK_DESCRIPTION) like '%SALV%' or UPPER(BLOCK_STATUS_CODE) like '%SALV%')"""

# # # Usage example 3 - look at all salvage logging in RKB since 2015, preserve all attributes, write KML to T: folder
# # Clean up SQL for string copied from SQL Developer (including comments)
# outPath, outName, outType = r"T:\testFolder", r"DSE_app_cutblock_since_Nov.2018", "KML"
# sqlQuery = """select *
# from WHSE_FOREST_TENURE.FTEN_CUT_BLOCK_POLY_SVW
# where BLOCK_STATUS_DATE > '01-NOV-18' --comment here
# and LIFE_CYCLE_STATUS_CODE IN ('ACTIVE','PENDING') --another comment here
# and GEOGRAPHIC_DISTRICT_CODE IN ('DSE')
# --and (UPPER(CUT_BLOCK_DESCRIPTION) like '%SALV%' or UPPER(BLOCK_STATUS_CODE) like '%SALV%')
# """

# # Usage example 4 - create a GeoPackage file for a TSA in the Kootenay Boundary Region; write it to folder on GeoBC FTP site
# tDict = {'Arrow TSA':1, 'Boundary TSA':2, 'Cranbrook TSA':5, 'Golden TSA':7, 'Invermere TSA':9, 'Kootenay Lake TSA':13, 'Revelstoke TSA':27 } # for reference
# outPath = r"\\ftpgeobc.nrs.bcgov\ftpgeobc\pub\outgoing\GeoBC_Regional\Kootenay_Boundary"
# outName, outType = r'Cranbrook TSA', "GPKG"
# sqlQuery = r"select * from WHSE_ADMIN_BOUNDARIES.FADM_TSA where TSB_NUMBER is null AND RETIREMENT_DATE IS NULL AND TSA_NUMBER = {}".format(tDict['Cranbrook TSA'])

# # Usage example 5 - NEEDS WORK - creates a JSON file of highway rest stops in WGS 84 (geographic coordinates), write it to a T: folder
# # In this case, script must know the inCRS and outCRS to correctly transform
# outCRS = 4326
# outPath, outName, outType = r"T:\testFolder", r"rest_stops_GC", "GeoJSON"
# sqlQuery = "select * from WHSE_IMAGERY_AND_BASE_MAPS.MOT_REST_AREAS_SP"

# # Usage example 6 - create an ESRI Shapefile for several TSAs in Kootenay Boundary Region, write it to a project folder
# tDict = {'Arrow TSA':r'01', 'Boundary TSA':r'02',  'Kootenay Lake TSA':r'13'} # for reference
# outPath = r"W:\FOR\RSI\DKL\General_User_Data\gamos\Projects\2019\OGR_tests"
# outName, outType = r"zRKB_TSAs_01", "ESRI Shapefile"
# tsaString = "('{}','{}','{}')".format(tDict['Arrow TSA'], tDict['Boundary TSA'], tDict['Kootenay Lake TSA'])
# # sqlQuery = "select * from WHSE_ADMIN_BOUNDARIES.FADM_TSA where TSA_NUMBER IN {} AND TSB_NUMBER is null AND RETIREMENT_DATE IS NULL".format(tsaString)
# sqlQuery = "select * from WHSE_ADMIN_BOUNDARIES.FADM_TSA where TSB_NUMBER is null AND RETIREMENT_DATE IS NULL AND TSA_NUMBER IN {}".format(tsaString)

###############################################################################################################
def make_wrkSpc(wrkSpc):
    if not os.path.exists(wrkSpc):
        os.mkdir(wrkSpc)
        print("{} created.\n".format(wrkSpc))
    else:
        print("{} exists.\n".format(wrkSpc))

###############################################################################################################
def findValueInDict(dicto, value):
        for count, k in enumerate(dicto.keys()):
            print("\t{:>2}. Key: {} \tValue: {}".format(count, k, dicto[k]))
            if value in os.environ[k]:
                print("here it is: value '{}' is in the '{}' key.".format(value, k))
                sys.exit()

###############################################################################################################
def getPackageInfo(package):
    conditions = [hasattr(package, "__name__"), hasattr(package, "__version__"), hasattr(package, "__path__"), hasattr(package, "__file__")]
    if all(conditions):
        print("{} {} path is {} and file is {}".format(package.__name__, package.__version__, package.__path__, (package.__file__)))
    elif all([hasattr(package,"__name__"), hasattr(package, "__version__")]):
        print("{}".format(package.__name__, package.__version__))
    elif hasattr(package, "__name__"):
        print("Package: '{}' exists".format(package.__name__))
    else:
        print("no info available on {} package".format(package))

###############################################################################################################
def ogrFromBCGW(outType, outPath, outName, user, pword, sqlQuery, outCRS = 3005, coordPrec = 1):
    if user=="USERNAME":
        print("Must enter your BCGW username and password; exiting script.")
        sys.exit()

    # print("ArcGIS info:") # this is a proxy to figure out which DTS desktop the user is on
    # print("\t", arcpy.GetInstallInfo()['SourceDir'])
    # print("\t", arcpy.GetInstallInfo()['InstallDir'])
    # print("\t", arcpy.GetInstallInfo()['Version'])

    for p in os.environ["PATH"].split(";"):  # to find the QGIS path, could use os.environ or sys.path, either works.
        if "QGIS" in p:
            for x in p.split("\\"):
                if "QGIS" in x:
                    joinIndex = p.split("\\").index(x) + 1
            qgisPath = "\\".join(p.split("\\")[0:joinIndex])
            print("qgisPath is: {}".format(qgisPath))
            break

    epsgDict = {3005: "BC Albers", 3741: "NAD83(HARN) / UTM zone 11N", 4326:'WGS 84', 104199:"GCS_WGS_1984_Major_Auxiliary_Sphere"}
    extDict = {"GeoJSON":".json", "KML":".kml", "ESRI Shapefile":".shp", "GPKG":".gpkg"}

    osgeo_bat, ogr_exe = r"{}\OSGeo4W.bat".format(qgisPath), r'{}\bin\ogr2ogr.exe'.format(qgisPath)
    # print("{}\t{}".format(osgeo_bat, ogr_exe))

    ogrList = [] # empty list to be filled with parameters, then passed into subprocess.run() or .call()

    specifySRS, srs_def = '-a_srs','epsg:{}'.format(outCRS)
    f, formatName, fileName = '-f', outType, os.path.join(outPath, outName) + extDict[outType]
    ds = "OCI:{}/{}@IDWPROD1:no_Table".format(user,pword)
  
    # SQL handling part 1 - scrub any comments from end of line
    if "--" in sqlQuery: # this is the comment syntax in Oracle SQL Developer
        listo = sqlQuery.split("\n")
        sqlQuery = ""
        for line in listo:
            line = line.split("--")[0]
            sqlQuery+= line + "\n"
    print("Corrected SQL query is:\n{}".format(sqlQuery))
    
    # SQL handling part 2 - write the SQL to a temporary .sql file first, then read it from the external file (ensures UTF-8 compliance)
    make_wrkSpc(r"T:\tempQueryFolder")
    sqlFile = os.path.join(r"T:\tempQueryFolder","query.sql")  # query.sql will overwrite if running the script repeatedly
    with open(sqlFile, 'w') as thing:
        thing.write(sqlQuery)

    progress = '-progress'
    sql = '-sql'
    sqlQ = r"@{}".format(sqlFile)

    for x in [osgeo_bat, ogr_exe, specifySRS, srs_def, f, formatName, fileName, ds, progress, sql, sqlQ]:
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
            crsMessage = "\n\nResultant spatial file (KML) always has CRS:{} ({})".format(4326, epsgDict[4326])
        else:
            crsMessage = "\n\nResultant spatial file will have CRS:{} ({})".format(outCRS, epsgDict[outCRS])
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

    make_wrkSpc(outPath)

    # which Python version you are using determines what subprocess method to use;
    # if Python >= 3.5, use subprocess.run
    pyVersion = float("{}.{}".format(sys.version_info.major, sys.version_info.minor))
    if pyVersion >= 3.5:
        print("pyVersion = {}; using subprocess.run . Running now, see progress indicator below...\n".format(pyVersion))
        rc = subprocess.run(ogrList, check=True)
        # try:
        #     rc = subprocess.run(ogrList, check=True)
        # except subprocess.CalledProcessError as error:
        #     print("\nProblem!")
        #     print(error)

    else: # for Python 2 cases..
        # Like subprocess.run(), subprocess.call() works with a list of arguments...
        print("pyVersion = {}; using subprocess.call . Running now...".format(pyVersion))
##        rc = subprocess.call(ogrList)
##        msg = "Success! ogr2ogr ran OK.\n" if rc == 0 else "subprocess.call had a problem running ogr2ogr... return code = {}\n".format(rc)
##        print(msg)
        try:
            rc = subprocess.check_call(ogrList)
        except subprocess.CalledProcessError as error:
            print("Problem! Limited info available due to Python version being {}; try running in Geospatial Desktop (Python 3) to learn more about the problem.\n".format(pyVersion))
            print(error)

    # os.remove(sqlFile) 
    return ogrList

########################################################################

ogrList = ogrFromBCGW(outType, outPath, outName, user, pWord, sqlQuery)
# print("\nArguments:\n", ogrList)
newString = ""
print("\nArguments used:")
for arg in ogrList:
    print("\t{}".format(arg))
    if ogrList.index(arg) > 0:
        if ogrList.index(arg) == 5: # the driver argument
            newString += '"{}" '.format(arg)
        else:
            newString += '{} '.format(arg)
print("\nogr2ogr string here (you can copy and paste this to the OSGeo4W shell and run it there if you want):\n{}\n\n".format(newString))

 