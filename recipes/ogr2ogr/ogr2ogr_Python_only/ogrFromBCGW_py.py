
# ogrFromBCGW_BCGOV_FINAL2.py
# gamos 06/12/2019 (DD/MM/YY format)
# Gregory.Amos@gov.bc.ca
# GIS Technician (auxiliary) / Kootenay Boundary Region / Ministry of Forests, Lands and Natural Resource Operations and Rural Development

# Script to create and execute an ogr2ogr CLI string - i.e translate a BCGW subset into one of several geospatial formats

"""CHECK/BE AWARE OF THESE THINGS BEFORE RUNNING SCRIPT:
1. Fill in your BCGW credentials for user, pWord (Line 44)

2. If querying a field by date, it's important to format your SQL statement as follows: FIELD operator DATE_VALUE
ex.1 BLOCK_STATUS_DATE < '15-SEP-19'        ex. 2 UPDATE_DATE >= '01-JAN-00'       
Can use operators including: = > < <= and >=     CANNOT use BETWEEN operator, i.e. BETWEEN 'startDate' AND 'endDate' will not work..
CANNOT have two date queries in the same line:  ex. 3 LAST_CHANGE_DATE >= '11-NOV-18' and LAST_CHANGE_DATE < '01-APR-19'

3. It's safe to disregard the 'ERROR 1: ORA-04043: object no_Table does not exist' message that will print to the console - that's just a way of preventing 
   ogr2ogr from scanning all tables in the BCGW once it connects...

4. If the script fails with 'ERROR 1: Layer 'layer1' does not already exist in the output dataset, and cannot be created by the output driver', 
   this can be corrected by choosing a new outName.

5. Most BCGW datasets are in BC Albers; default output is in BC Albers projection with coordinates to nearest 0.1 metres

6. Layer names are created based on the 'outName' variable, with a maximum length of 20 characters and all spaces replaced by underscores

7. If outputting an ESRI Shapefile, it's normal to see 'Warning 6: Normalized/laundered field name:' This reducess field names to 10 characters long, which is the max length for a shapefile field.
"""

# UPDATE_LOG 05/12/2019
# =====================
# 1. Updated paths for OSGeo4W and bin/ogr2ogr.exe - script now works in all DTS desktops
# 2. No more arcpy import
# 3. Better SQL string handling - SQL strings are written to .sql files in T:\tempQueryFolder, then read back in as an ogr2ogr parameter - works much better.
# 4. Added logic to scrub any Python or Oracle comments in the sqlQuery (to ensure the Oracle SQL dialect translates well to OGR SQL)
# 5. Fixed SQL issues arising from date field 'where' clauses - parses each line in SQL using regular expressions and rebuilds the date comparison using integers.   
# 6. Fixed Geopackage non-compatibility with ArcGIS by restricting length of layer name

import os
import re
import sys
import subprocess

# user, pWord = input("Enter your BCGW username:"), input("Enter your BCGW password:")
# user, pWord = "USERNAME", "PASSWORD"
overWrite = "Y" # choose "Y" to overwrite datasets, "N" to not allow overwrites

# Choose outPath, outName, and outType - outType must be one of 'GeoJSON', 'KML', 'ESRI Shapefile', or 'GPKG'

# # Usage example 1 - create a KML for a single wildfire, with  FIRE_NUMBER as only attribute, write it to a T: folder
# outPath, outName, outType = r"T:\test", r"fireKML_99", "KML"
# sqlQuery = r"""select FIRE_NUMBER, SHAPE from WHSE_LAND_AND_NATURAL_RESOURCE.PROT_HISTORICAL_FIRE_POLYS_SP where FIRE_NUMBER ='N40101'"""

# # Usage example 2 - create an ESRI Shapefile all wildfires in Southeast zone in 2018, preserve all attributes, write it to T: folder
# outPath, outName, outType = r"T:\test", r"fires_2015+", "ESRI Shapefile"
# sqlQuery = r"""select * from WHSE_LAND_AND_NATURAL_RESOURCE.PROT_HISTORICAL_FIRE_POLYS_SP where FIRE_YEAR > 2015 and FIRE_NUMBER like 'N%'"""

# # Usage example 3 - create a GeoPackage file for a TSA in the Kootenay Boundary Region; write it to folder on GeoBC FTP site
# tDict = {'Arrow TSA':1, 'Boundary TSA':2, 'Cranbrook TSA':5, 'Golden TSA':7, 'Invermere TSA':9, 'Kootenay Lake TSA':13, 'Revelstoke TSA':27 } # for reference
# outPath = r"\\ftpgeobc.nrs.bcgov\ftpgeobc\pub\outgoing\GeoBC_Regional\Kootenay_Boundary"
# outName, outType = r'Cranbrook TSA 3', "GPKG"
# sqlQuery = r"""select * from WHSE_ADMIN_BOUNDARIES.FADM_TSA where TSB_NUMBER is null AND RETIREMENT_DATE IS NULL AND TSA_NUMBER = {}""".format(tDict['Cranbrook TSA'])

# # Usage example 4 - create an ESRI Shapefile for several TSAs in Kootenay Boundary Region, write it to a folder on \\spatialfiles.bcgov\work
# tDict = {'Arrow TSA':r'01', 'Boundary TSA':r'02',  'Kootenay Lake TSA':r'13'} # for reference
# outPath = r"\\spatialfiles.bcgov\work\FOR\RSI\DKL\General_User_Data\gamos\Projects\2019\OGR_tests"
# outName, outType = r"a fewRKB TSAs ", "ESRI Shapefile"
# tsaString = "('{}','{}','{}')".format(tDict['Arrow TSA'], tDict['Boundary TSA'], tDict['Kootenay Lake TSA'])
# # sqlQuery = "select * from WHSE_ADMIN_BOUNDARIES.FADM_TSA where TSA_NUMBER IN {} AND TSB_NUMBER is null AND RETIREMENT_DATE IS NULL".format(tsaString)
# sqlQuery = r"""select * from WHSE_ADMIN_BOUNDARIES.FADM_TSA where TSB_NUMBER is null AND RETIREMENT_DATE IS NULL AND TSA_NUMBER IN {}""".format(tsaString)

# # Usage example 5 - look at all salvage logging in RKB since 2015, preserve all attributes, write KML to T: folder
# # Note the 'where' clause involving a date comparison - where BLOCK_STATUS_DATE > '01-JAN-15' - gets re-written to create OGR-friendly SQL.
# outPath, outName, outType = r"T:\test", r"salvage logs since Jan. 2015", "KML"
# sqlQuery = r"""select * from WHSE_FOREST_TENURE.FTEN_CUT_BLOCK_POLY_SVW
# where BLOCK_STATUS_DATE > '01-JAN-15'
# and LIFE_CYCLE_STATUS_CODE IN ('ACTIVE','PENDING')
# and GEOGRAPHIC_DISTRICT_CODE IN ('DSE','DRM')
# and (UPPER(CUT_BLOCK_DESCRIPTION) like '%SALV%' or UPPER(BLOCK_STATUS_CODE) like '%SALV%')"""

# # Usage example 6 - creates a JSON file of highway rest stops in WGS 84 (geographic coordinates), write it to a T: folder
# # Note this outName is too long and will be truncated to 20 characters. The filename will stay full-length.
# outCRS = 4326 # 4326 is the EPSG code for the WGS 84 GCS
# outPath, outName, outType = r"T:\test", r"BC highways rest stops in GCS WGS 84", "GeoJSON"
# sqlQuery = r"""select * from WHSE_IMAGERY_AND_BASE_MAPS.MOT_REST_AREAS_SP"""

# # Usage example 7 - create a Geopackage of all harvest approvals in the DSE and DRM districts within a certain date range,
# # select only specific attributes (includnig the GEOMETRY field) , write it to T: folder, 
# outPath, outName, outType = r"T:\test", r"RKB_harv_approvals_Sept2017_Sept2019", "GPKG"
# sqlQuery = r"""select b.GEOGRAPHIC_DISTRICT_CODE, b.CUT_BLOCK_FOREST_FILE_ID, b.CUT_BLOCK_ID, b.HARVEST_AUTH_CUTTING_PERMIT_ID, b.BLOCK_STATUS_CODE, c.DESCRIPTION,
# b.BLOCK_STATUS_DATE, b.PLANNED_HARVEST_DATE, b.GEOMETRY, b.DISTURBANCE_START_DATE, b.DISTURBANCE_END_DATE, b.GEOMETRY

# from WHSE_FOREST_TENURE.FTEN_CUT_BLOCK_POLY_SVW b
# inner join WHSE_FOREST_TENURE.FTEN_BLOCK_STATUS_CODE c 
# on  b.BLOCK_STATUS_CODE = c.BLOCK_STATUS_CODE
# where b.BLOCK_STATUS_DATE >= '01-SEP-17'
# and b.BLOCK_STATUS_DATE < '01-SEP-19' 
# and c.BLOCK_STATUS_CODE IN ('HB') --maybe include 'S' too
# and b.LIFE_CYCLE_STATUS_CODE IN ('ACTIVE')
# and b.GEOGRAPHIC_DISTRICT_CODE IN ('DSE','DRM') -- that's a comment
# order by BLOCK_STATUS_DATE asc -- that's a paddlin'
# """

# # Usage example 8 - create a Geopackage of all FESBC-funded projects in the Kootenay Boundary Region, write it to T: folder, 
# # include only the specified fields (note the GEOMETRY field must be explicitly included), and apply an SDO_ANYINTERACT spatial
# # filter to select only projects in or touching the RKB 
# # Be patient - this transformation likely takes more than 1 minute to complete.
# outPath, outName, outType = r"T:\test", r"FESBC_proj_in_RKB", "GPKG"
# sqlQuery = r"""select a.OPENING_ID, a.FIA_PROJECT_ID , e.DESCRIPTION, a.SILV_FUND_SOURCE_CODE, 
# (b.DESCRIPTION || '_' || c.DESCRIPTION || '_' || d.DESCRIPTION) as WORK_DONE,
# a.GEOMETRY_EXIST_IND, EXTRACT(year FROM a.ATU_COMPLETION_DATE) as YEAR_COMPLETE,
# a.ACTUAL_TREATMENT_AREA, a.GEOMETRY

# from WHSE_FOREST_VEGETATION.RSLT_ACTIVITY_TREATMENT_SVW a
# join WHSE_FOREST_VEGETATION.RSLT_SILV_BASE_CODE b
# on a.SILV_BASE_CODE = b.SILV_BASE_CODE
# join WHSE_FOREST_VEGETATION.RSLT_SILV_TECHNIQUE_CODE c
# on a.SILV_TECHNIQUE_CODE = c.SILV_TECHNIQUE_CODE
# join WHSE_FOREST_VEGETATION.RSLT_SILV_METHOD_CODE d
# on a.SILV_METHOD_CODE = d.SILV_METHOD_CODE
# join WHSE_FOREST_VEGETATION.RSLT_SILV_FUND_SRCE_CODE e
# on a.SILV_FUND_SOURCE_CODE = e.SILV_FUND_SRCE_CODE
# where SILV_FUND_SOURCE_CODE like 'FES'
# and GEOMETRY_EXIST_IND = 'Y'
# and SDO_ANYINTERACT 
# (a.GEOMETRY, (select regions.SHAPE
# from WHSE_ADMIN_BOUNDARIES.ADM_NR_REGIONS_SP regions
# where ORG_UNIT = 'RKB' )) = 'TRUE'  
# order by FIA_PROJECT_ID"""


###############################################################################################################
def make_wrkSpc(wrkSpc):
    if not os.path.exists(wrkSpc):
        os.mkdir(wrkSpc)
        print("{} created.\n".format(wrkSpc))
    else:
        print("{} exists.\n".format(wrkSpc))

###############################################################################################################
def reSearch(pattern, sequence):
    try:
        thing = re.search(pattern, sequence).group()
    except AttributeError:
        thing = None
    if thing:
        thing = "yep"
    return thing

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
def ogrFromBCGW(outType, outPath, outName, overWrite, user, pword, sqlQuery, outCRS = 3005, coordPrec = 1):
    # CHECK: BCGW info entered OK?
    conditions = [user=="USERNAME", pword=="PASSWORD"]
    # if user=="USERNAME":
    if any(conditions):
        print("Must enter your BCGW username and password; exiting script.")
        sys.exit()

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

    # CHECK: specified outType is valid?
    if outType not in extDict.keys():
        print("outType is not one of {}; exiting script.".format(list(extDict.keys())))
        sys.exit()

    osgeo_bat, ogr_exe = r"{}\OSGeo4W.bat".format(qgisPath), r'{}\bin\ogr2ogr.exe'.format(qgisPath)
    # print("{}\t{}".format(osgeo_bat, ogr_exe))

    ogrList = [] # empty list to be filled with parameters, then passed into subprocess.run() or .call()

    specifySRS, srs_def = '-a_srs','epsg:{}'.format(outCRS)
    f, formatName, fileName = '-f', outType, os.path.join(outPath, outName) + extDict[outType]
    ds = "OCI:{}/{}@IDWPROD1:no_Table".format(user,pword)

    # SQL handling part 1 - scrub any Python or Oracle SQL comments from end of line, as OGR SQL won't accept these parts of Oracle SQL dialect
    def sqlQueryScrubber(sqlQuery):
        newSQL = ""
        listo = sqlQuery.split("\n")
        for line in listo:
            if len(line) > 0 and line[0] == "#" or line[0:2] == "--": # if the line is commented out from the start, skip it 
                pass
            else: 
                line = line.split("--")[0] # i.e. keep everything before the -- Oracle comment
                if len(line) > 0: # if the line has content, add it to the new SQL String
                    line = line.replace('"','\'') # replace any double quotes with single quotes
                    newSQL += line + "\n"

        # SQL handling part 2 - re-build SQL date comparisons into integer comparisons           
        newerSQL = ""             
        for line in newSQL.split("\n"):       
            monthDict = {'JAN':1, 'FEB':2, 'MAR':3, 'APR':4, 'MAY':5,'JUN':6, 'JUL':7, 'AUG':8, 'SEP':9, 'OCT':10, 'NOV':11, 'DEC':12}
            # lineEnd = line.strip()[-11:]
     
            if reSearch(r"BETWEEN", line) == "yep":
                print("\nPROBLEM!\n ogrFromBCGW can't successfully translate a BETWEEN operator for dates. Change the sqlQuery and try again.")
                sys.exit()
            # if not all([reSearch(r"DATE", line) == "yep", reSearch(r"'\d\d-\w\w\w-\d\d'", line) == "yep", reSearch(r"BETWEEN", line) is None]):
            if not all([reSearch(r"DATE", line) == "yep", reSearch(r"'\d\d-\w\w\w-\d\d'", line) == "yep"]): # these conditions show an SQL line has a date field being evaluated against a date value
                newerSQL += line + "\n"
                # print("newerSQL is:\n{}\n".format(newerSQL))
            
            elif all([line.split(" ")[2].isdigit() == False, line.split(" ")[2].isalpha() == False]):
                joiner = line.split(" ")[0] # i.e where b.BLOCK_STATUS_DATE >= '01-JUL-18' >>> [0] = 'where'  
                fieldName = line.split(" ")[1]                                               # [1] = 'b.BLOCK_STATUS_DATE' 
                operator = line.split(" ")[2]                                                # [2] = '>='
                print("\nDate expression found in SQL:")
                print("fieldName is: {}".format(fieldName))
                print("operator is: {}".format(operator))
                print("date is: {}".format(line.split(operator)[1].strip())) # i.e where b.BLOCK_STATUS_DATE > '01-JUL-18' >>>'01-JUL-18'
                day = int(line.split(operator)[1].strip()[1:3])
                month = monthDict[line.split(operator)[1].strip()[4:7]]         
                year = "20" + str(line.split(operator)[1].strip()[8:10])
                # print("{} {} {}".format(day, month, year))

                oDict = {'=':'=', '>':'>', '<':'<', '>=':'>', '<=':'<' }
                newline1 = "EXTRACT(year FROM {}) {} '{}'".format(fieldName, oDict[operator], year)
                newline2 = "or ({0} and EXTRACT(month FROM {1}) {2} '{3}' )".format(newline1.replace(oDict[operator], "="), fieldName, oDict[operator], month)
                newline3 = "{0} and EXTRACT(day FROM {1}) {2} '{3}'".format(newline2.replace(oDict[operator], "="), fieldName, operator, day)
                newerSQL += joiner + " ( " + newline1 + "\n" + newline2 + "\n" + newline3 + ")\n"
        return newerSQL

    sqlQuery = sqlQueryScrubber(sqlQuery)
    msg = "OGR-friendly SQL query is:"
    print("\n" + msg + "\n","="*len(msg))
    print(sqlQuery)

    # SQL handling part 3 - write the SQL to a temporary .sql file first, then read it from the external file (ensures UTF-8 compliance)
    make_wrkSpc(r"T:\tempQueryFolder")
    sqlFile = os.path.join(r"T:\tempQueryFolder","query.sql")  # query.sql will overwrite if running the script repeatedly
    with open(sqlFile, 'w') as thing:
        thing.write(sqlQuery)

    progress = '-progress'
    sql = '-sql'
    sqlQ = r"@{}".format(sqlFile)

    for x in [osgeo_bat, ogr_exe, specifySRS, srs_def, f, formatName, fileName, ds, progress, sql, sqlQ]:
        ogrList.append(x)
    if overWrite == "Y":
        ogrList.append('-overwrite')

    if outType == "GeoJSON": # Set GeoJSON specific options
        # for x in ["-lco","WRITE_NAME=NO","-nln", "layer1"]: # lco = layer creation option - prevents JSON layer from assuming entire sqlQuery as its name
        for x in ["-lco","WRITE_NAME=NO","-nln","{}".format(outName[0:20].replace(" ","_"))]: # -nln = "New Layer Name"; prevents the output layer from assuming the entire sqlQuery as its name
            ogrList.append(x)

    if outType == "GPKG": # Set GPKG specific options
        for x in ["-nln","{}".format(outName[0:20].replace(" ","_"))]: # -nln = "New Layer Name"; prevents the output layer from assuming the entire sqlQuery as its name
            ogrList.append(x)

    if outType == "KML": # Set KML specific options
        # for x in ["-nln","{}".format(outName[0:20].replace(" ","_")), "-dsco", "NameField= '{}'".format(nameField)]: # This would give each KML feature a better name than 'No Name'
        for x in ["-nln","{}".format(outName[0:20].replace(" ","_"))]: # -nln = "New Layer Name"; prevents the output layer from assuming the entire sqlQuery as its name
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
        # rc = subprocess.run(ogrList, check=True)
        try:
            rc = subprocess.run(ogrList, check=True)
        except subprocess.CalledProcessError as error:
            print("\nProblem! : {}\nExiting script.".format(error))
            sys.exit()
    else: # for Python 2 cases..
        # Like subprocess.run(), subprocess.call() works with a list of arguments...
        print("pyVersion = {}; using subprocess.call . Running now...".format(pyVersion))
##        rc = subprocess.call(ogrList)
##        msg = "Success! ogr2ogr ran OK.\n" if rc == 0 else "subprocess.call had a problem running ogr2ogr... return code = {}\n".format(rc)
##        print(msg)
        try:
            rc = subprocess.check_call(ogrList)
        except subprocess.CalledProcessError as error:
            print("""Problem! Limited info available due to Python version being {}; try running in Geospatial Desktop (Python 3) to learn more about the problem.
            Exiting script.\n""".format(pyVersion))
            sys.exit()

    # os.remove(sqlFile) 
    return ogrList

##################################################################################
if 'outCRS' in globals(): # if user has defined an outCRS variable:
    ogrList = ogrFromBCGW(outType, outPath, outName, overWrite, user, pWord, sqlQuery, outCRS)
else: # use the default outCRS = 3005 = BC Albers
    ogrList = ogrFromBCGW(outType, outPath, outName, overWrite, user, pWord, sqlQuery)

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

os.rmdir(r"T:\tempQueryFolder")