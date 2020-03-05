
# ogrFromBCGW_csv_FINAL.py 
# gamos 27/02/2020 (DD/MM/YY format)
# Gregory.Amos@gov.bc.ca
# GIS Technician (auxiliary) / Kootenay Boundary Region / Ministry of Forests, Lands and Natural Resource Operations and Rural Development

# Script to create and execute *multiple* ogr2ogr CLI strings
# Using SQL, a user can grab any data subset from BCGW and save it in a variery of formats
# This script takes all user input via the ogrParams.csv file

"""CHECK/BE AWARE OF THESE THINGS BEFORE RUNNING SCRIPT:
--------------------------------------------------------------------------------------
IT'S VERY IMPORTANT THAT THESE FILES ARE IN THE SAME FOLDER WHEN RUNNING THIS SCRIPT:
1. ogrFromBCGW_csv_FINAL.py
2. ogrParams.csv
--------------------------------------------------------------------------------------

0. Each row in params_FINAL.csv is a set of values you are feeding into the ogrFromBCGW script.
Each column header becomes a key name in the dictionary generated from each row, and row values become the dictionary values.

1. The following columns need to have values for ogrFromBCGW to run: paramName, outPath, outName, outType, sqlQuery
paramName - a simple string like harvestParams
outPath - location to save output to (will be created if it doesn't exist)
outName - name of your output file (no extension, but placeholders are OK)
outType - type of file ex. GPKG, KML
sqlQuery - a query to draw the result from the BCGW. IMPORTANT - TEST IT BEFORE USING IN THIS SCRIPT
ogrReadTheseColumns - this is a comma-seperated text list that tells the script which values to read in. The order doesn't matter

This column is optional; this is what they do in this script:
paramDescription - a description of what output each row helps create

Any remaining columns are customized to the outputs of the script or are meant be passed on to another script that uses the results of this script   
curDate - used to put the run date in file names
harvestSinceWhen, fireStartYear  - these are date and integer values that might feed into the SQL queries for each output, to make the query easily adjustable
dsDict, dataSources, data_OG_dict, oldGrowthLayerNames - these are values that point to data sources and output latyer names for the old growth harvest resultant 

The order of the columns does not matter, as long as the right values are under the right heading.

2. The .csv fileName is contained in the paramFileName variable (set by default to 'ogrParams.csv').
If you change the name of the .csv file, update this variable ( Use Ctrl + F to find it, around Line 500 )

3. As you update the .csv, make sure you keep string formats the same way:
i.e. if a date is expressed as '01-JUL-18', don't change it to 'July 1, 2018'. And don't lose the single quotes.

IF YOU MAKE CHANGES, REMEMBER TO SAVE THE .CSV FILE BEFORE RUNNING THIS SCRIPT !

4. It's safe to disregard the 'ERROR 1: ORA-04043: object no_Table does not exist' message that will print to the console - that's just a way of preventing 
   ogr2ogr from scanning all tables in the BCGW once it connects...

5. If the script fails with 'ERROR 1: Layer 'layer1' does not already exist in the output dataset, and cannot be created by the output driver', 
   this can be corrected by choosing a new outName.

6. Avoid using dashes in GPKG layer names (i.e. roads-non-status) as it makes them unreadable in ArcGIS 

7. Most BCGW datasets are in BC Albers; default output is in BC Albers projection with coordinates to nearest 0.1 metres

8. Layer names are created based on the 'outName' variable, with a maximum length of 20 characters and all spaces replaced by underscores

9. If outputting an ESRI Shapefile, it's normal to see 'Warning 6: Normalized/laundered field name:' This reducess field names to 10 characters long, which is the max length for a shapefile field.

"""

from pathlib import Path
import csv
import logging
import os
import re
import shutil
import sys
import time
import subprocess

# Log file setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # 
# logger.setLevel(logging.INFO) # 

# Create 2D lists to facilitate multiple ogrFromBCGW calls
ogrMultiList, outNamesList, cliStringList= [], [], []

###############################################################################################################
def make_wrkSpc(wrkSpc, rsltDict, outPathList):
    if not os.path.exists(wrkSpc):
        os.mkdir(wrkSpc)
        print("\n{} created.\n".format(wrkSpc))
    else:
        print("\n{} exists.".format(wrkSpc))
        yConditions = [overwrite == "Y", wrkSpc != r"T:\tempQueryFolder", rsltDict['outPath'] not in outPathList] # script must always overwrite the tempQueryFolder
        nConditions = [overwrite == "N", wrkSpc != r"T:\tempQueryFolder"] # script must overwrite the tempQueryFolder
      
        if all (yConditions):
            shutil.rmtree(wrkSpc)
            os.mkdir(wrkSpc)
            print("{} re-created as empty folder.\n".format(wrkSpc))
        elif all(nConditions):
            print("Will not overwrite existing folder; exiting script.\n")
            sys.exit()

###############################################################################################################
def reSearch(pattern, sequence): # A function using regular expressions to find sub-strings
    try:
        thing = re.search(pattern, sequence).group()
    except AttributeError:
        thing = None
    return True if thing else False # ternary expression
        
# Ex. reSearch(r"'\d\d-\w\w\w-\d\d'", line) 

###############################################################################################################
def readCSVtoDict(theCSV): # returns a list of dictionaries drawn from CSV file
    with open(theCSV,'r') as csvFile: # 'r' for read .csv file, 'rb' for read text file
        # filter1 = filterfalse(lambda line: line.startswith('\n'), csvFile) # NEW
        fileReader = csv.DictReader(csvFile) # dialect defaults to comma as delimiter
        # fileReader = csv.DictReader(csvFile, filter1) # NEW - filter1 scrubs blank lines, dialect defaults to comma as delimiter

        dList, nameDict, paramNum = [], {}, 0
        for count, row in enumerate(fileReader): # each row is returned as a dictionary
            # dicto = {k:v for k, v in row.items() if v != ''} # scrub the keys with empty string values
            dicto = {k.strip():v.strip() for k, v in row.items() if v != ''} # grab just key values (no whitespaces) and scrub the keys with empty string values
            # print("{}.  {}\n".format(count, dicto)) # verbose
            
            # for x in row: # this is like 'for key in dict' i.e. will only print the keys, not the values!      
            if any(x.strip() for x in list(row.values())): # if there are any values after stripping strings, then the row has data and should be added to the list
                # print("row {} has values:".format(count))
                dList.append(dicto)
                paramNum += 1
                # print("\t", dicto.values(), "\n\n") # verbose
                nameDict[list(dicto.values())[0]] = count # the first value in the dict for each row is the 'paramName' , add this to the nameDict
            # print("row {}: {}\n\n".format(count, dList)) # verbose, but useful for debugging...
    
    return dList, nameDict, paramNum

# Ex. dList, nameDict = readCSVtoDict("params_harv.csv") # FUNCTION CALL EXAMPLE

###############################################################################################
# Function to parse key:value pairs from the .CSV-derived dictionary into new dictionaries

# def getVariableDicts(paramList, paramName, dList, nameDict): # dList and nameDict are global variables brought into the scope of this function
def getVariableDicts(paramList, paramName, dList, nameDict, paramsFileName): # dList and nameDict are global variables brought into the scope of this function
    dicto = {}
    for key in paramList: # paramList is a Python list
        try:
            dicto[key] = dList[nameDict[paramName]][key].strip() # .strip() takes care of any whitespace inadvertently placed on either side of the value
        except KeyError:
            print ("\nThe '{}' key (i.e this column in {}) seems to be missing a value... check your .csv\n\n".format(key, paramsFileName)), sys.exit()
        # print(dicto.items()) # temp
    return dicto

# ex.  rsltDict = getVariableDicts(['outPath', 'outName', 'curDate', 'sqlQuery'], 'harvestParams', dList, nameDict) # FUNCTION CALL
##############################################################################################
def reStringPosition(pattern, sequence):
    for match in re.finditer(pattern, sequence):
        return match.span()[0], match.span()[1]
# ex. dateIndexStart, dateIndexEnd = reStringPosition(r"'\d\d-\w\w\w-\d\d'", line)

###############################################################################################################
def ogrReadTheseColumns(): # one .csv column contains names of all columns (in a comma-separated text list) that need to be read to generate a given resultant
# that column name is 'ogrReadTheseColumns'
    resultantLists = []  
    for n in range(paramNum):
        listo = dList[int(n)]['ogrReadTheseColumns'].strip()
        # print("{}. {}".format(n, listo))
        resultantLists.append(listo)
    return resultantLists

###############################################################################################################  
# # Function to pull fieldName, operator, day, month, year and lineStartText from an SQL line. Only call it if you've verified the line has a date-like value..
# def parseSQL_DateLine(line, oDict):
#     oDict = {'=':'=', '>':'>', '<':'<', '>=':'>', '<=':'<' }
#     operList = list(oDict.keys())
#     # print(operList)

#     xList = []
#     for x in operList:
#         condition1 = reSearch(x, line) # Checks that the operator is found in the line
#         if condition1 == False: # .. this means that operator is not found. Check next.. 
#             # print("{} not found.".format(x))
#             continue
#         else:    
#             dateIndexStart, dateIndexEnd = reStringPosition(r"'\d\d-\w\w\w-\d\d'", line)
#             # print("dateIndexStart is: {}".format(dateIndexStart)) # Character position of start of date string
#             operIndexStart, operIndexEnd = reStringPosition(x, line)
#             # print("operIndexEnd is: {}".format(operIndexEnd)) # Character position of end of 'operator' string 
#         condition2 = True if dateIndexStart - operIndexEnd <= 5 else False
#         # True = operator is found to the immediate left (within 5 spaces) of the date; False = oper is found in the line but not close to the date string. Check next..  
        
#         if all ([condition1 == True, condition2 == True]):
#             # print("{} in line: {} ;     {} - {} is <= 5:{}".format(x, condition1, dateIndexStart, operIndexEnd, condition2))
#             xList.append(x) # x could be the operator..
   
#     if len(xList) > 0:
#         operator = max(xList, key=len)

#         # Find fieldname - split the SQL line by the operator, take the first half, use .rstrip() to clear the space between datefield and oper, use .lstrip("(") to eliminate any ( that may exist
#         stuff = line.split(operator)[0].rstrip().lstrip("(")  
#         fieldName =''.join(stuff.split(" ")[-1:]) # get string from the last item in the list

#         # Find 'lineStartText' i.e. everything that comes before fieldname in the SQL line
#         lineStartText = line.split(fieldName)[0]
        
#         # Find date - split the SQL line by the operator, take the first half, use .lstrip() to clear the space between oper and date value, use .rstrip(")") to eliminate any ) that may exist
#         stuff = line.split(operator)[1].lstrip().rstrip(")") 
#         date =''.join(stuff.split(" ")[0]) # get string from the last item in the list

#         # Get day, month and year from date
#         monthDict = {'JAN':1, 'FEB':2, 'MAR':3, 'APR':4, 'MAY':5,'JUN':6, 'JUL':7, 'AUG':8, 'SEP':9, 'OCT':10, 'NOV':11, 'DEC':12}
#         day = date.strip()[1:3]
#         month = monthDict[date.strip()[4:7]]
#         curYear = time.strftime("%Y")[2:4] # two-digit current year

#         # Set four-digit year based on past 100 years 
#         year = "20{}".format(str(date.strip()[8:10])) if date.strip()[8:10] <= curYear else "19{}".format(str(date.strip()[8:10]))
#         # if date.strip()[8:10] <= curYear :  
#         #     year =  "20" + str(date.strip()[8:10]) 
#         # else:
#         #     year =  "19" + str(date.strip()[8:10]) 

#         msg = "\nDate expression found in SQL:"                                              
#         print(msg + "\n" + "-"*len(msg))
#         print("lineStartText is: {}".format(lineStartText))  # TEMP
#         print("fieldName is: {}".format(fieldName)) 
#         print("operator is: {}".format(operator))
#         print("date is: {}".format(date))
#         print("day is: {}".format(day))
#         print("month is: {}".format(month))
#         print("year is: {}".format(year))
 
#     else:
#         print("No date expression found in SQL line; exiting script"), sys.exit()
#     # return fieldName, operator, day, month, year
#     return lineStartText, fieldName, operator, day, month, year

###############################################################################################################  
def sqlBracketMismatchCheck(sqlString):
    # Ensure brackets in SQL remain in scope; fix if needed                  
    if sqlString.count(")")  < sqlString.count("(") :
        print("\nSQL parentheses mismatch detected..") 
        sqlString += ")"*(sqlString.count("(") - sqlString.count(")"))
        if sqlString.count("(") == sqlString.count(")") :
            print("SQL parentheses mismatch fixed.") 
    return sqlString

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
# Function to detect if a param value contains any .format() placeholders and if so, fill them properly 

# def fillFormatPlaceholders(ogrItem, fileName, extDict, outType):
def fillFormatPlaceholders(ogrItem, specialList = []): # specialList is used to hold [fileName, extDict, outType] variables, for adding filename extensions
    if reSearch(".*?.format", ogrItem) == True: # looks for '.format' in an ogrItem, i.e. a .csv value
        start = ogrItem.split(".format")[0] 
        start = start.strip("'").strip("\"").strip("\'") 
        print("\nstart is: {}\n".format(start)) # temp
        end = ogrItem.split(".format")[1]
        print("end is: {}\n".format(end)) # temp
        fValList = end[end.index("(") + 1 : end.index(")") ].split(",") # create a list with as many values as there are value parameters

        fValList2 = [n.strip() for n in fValList] # remove any whitespaces around the strings in the list
        # print("fValList2 is: {}\n".format(fValList2)) # use this if you are seeing a KeyError: 'key' arise here, check the rsltDict - it may indicate an error in the .csv
        
        # Write format variables:values as key:value pairs in 'valuesDict'
        valuesDict = {}
        for count, n in enumerate(fValList2):
            if 'time.strftime' in rsltDict[n]: # evaluate the expression if there's a time.strftime ( i.e system date) value for this dictionary key
                # valuesDict[count] = eval(rsltDict[n]) 
                valuesDict['key{}'.format(count)] = eval(rsltDict[n]) # NOTE: eval() requires trusted input - tried to use ast.literal_eval but it's really strict in python 3.7 
            else:
                print(rsltDict[n]) # temp
                valuesDict['key{}'.format(count)] = rsltDict[n]
                # valuesDict[count] = rsltDict[n]

        print(valuesDict.items(), "\n")

        string = start.format(**valuesDict)
        # string = start.format(valuesDict[0], (valuesDict[1].strip("'"))) # not great, assumes a two item list
    else:
        string = ogrItem

    if len(specialList) > 0: # specialList ==  [extDict, outType]:
        print(specialList) # temp
    # if ogrItem == fileName: # if the item in question is the filename param, now is the time to apply the extension
        # string += extDict[outType] 
        string += specialList[0][specialList[1]]
        string = string.replace("'","") # look up dictionary key to get value, scrub single quotes from date in fileName string
     
    # print("{}\nfillFormatPlaceholders function complete.\n".format(string))
    return string

###############################################################################################################
def checkParamsFile(pFile):
    cwd = Path(__file__).parents[0] 
    ogrParamsFile = list(cwd.glob(pFile))[0] # use glob to match a regular expression
    ogrParamsFile = ogrParamsFile.absolute() # ex. Windows_path object

    if ogrParamsFile.exists() == True:
        print("\n.csv file exists, reading it now..")
        ogrParamsFile = str(ogrParamsFile) # convert it from a path object to a string
    else:
        print("file not found, exiting"), sys.exit()
    return ogrParamsFile

###############################################################################################################
def bcgwLoginCheck(user, pWord):
    usernameCheck = reSearch("[a-zA-Z]"*len(user), user) # check username is letters only, upper or lower case
    upperCheck = reSearch(".*?[^A-Z]", pWord) # BCGW password must contain an English uppercase character (a..z) ... NOT EVERYONE HAS UPPERCASE CHARACTER
    lowerCheck = reSearch(".*?[a-z]", pWord) # BCGW password must contain an English lowercase character (a..z)
    digitCheck = reSearch(".*?\d", pWord ) # BCGW password must contain a base 10 digit (0..9)
    lenCheck = len(pWord) in range(8,21) # BCGW password must be between 8 and 20 characters long.

    if not all([x == True for x in [usernameCheck, upperCheck, lowerCheck, digitCheck, lenCheck]]):
        print("Re-enter your BCGW username and password; something's not right. Exiting script.")
        sys.exit()

###############################################################################################################
###############################################################################################################
###############################################################################################################

# If any variable is defined, it should override the default value from the function def below:

# def ogrFromBCGW(outType, outPath, outName, overWrite, user, pword, sqlQuery, outCRS=3005, coordPrec=1, nameField=None):
# def ogrFromBCGW(outPath, outName, overWrite, user, pword, sqlQuery, outType="GPKG", outCRS=3005, coordPrec=1, nameField=None):
# def ogrFromBCGW(outPath, outName, overWrite, makeFriendlySQL, sqlQuery, outType="GPKG", outCRS=3005, coordPrec=1, nameField=None):
# def ogrFromBCGW(user, pWord, outPath, outName, overWrite, makeFriendlySQL, sqlQuery, outType="GPKG", outCRS=3005, coordPrec=1, nameField=None):
def ogrFromBCGW(user, pWord, n, outPath, outName, sqlQuery, outType="GPKG", overWrite = "Y", makeFriendlySQL = "N", outCRS=3005, coordPrec=1, nameField=None):   
    print("\nStarting ogrFromBCGW function...")
    # outCRS=3005 # Can be overwritten later if needed

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

    # Check that specified outType is valid (using regular expressions)
    conditions = [reSearch(k, outType) for k in extDict.keys()] # FUNCTION CALL
    if not True in conditions:
        print("outType is {} {} ; it's not one of {}; exiting script.".format(outType, type(outType), list(extDict.keys())))
        sys.exit()

    osgeo_bat, ogr_exe = r"{}\OSGeo4W.bat".format(qgisPath), r'{}\bin\ogr2ogr.exe'.format(qgisPath)
    # print("{}\t{}".format(osgeo_bat, ogr_exe))

    ogrList = [] # empty list to be filled with parameters, then passed into subprocess.run() or .call()
    specifySRS, srs_def = '-a_srs', 'epsg:{}'.format(outCRS)
    f, formatName, fileName = '-f', outType, os.path.join(outPath, outName)
    ds = "OCI:{}/{}@IDWPROD1:no_Table".format(user,pWord)

    # SQL handling - fill .format() placeholders if any and scrub any Python or Oracle SQL comments from end of line, as OGR SQL won't accept these parts of Oracle SQL dialect
    def sqlQueryScrubber(sqlQuery, makeFriendlySQL):
        sqlQuery = fillFormatPlaceholders(sqlQuery) # FUNCTION CALL
        print(sqlQuery, "\n","\n")
        
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
        newSQL = sqlBracketMismatchCheck(newSQL) # FUNCTION CALL 
        msg = "SQL query is:"
        return newSQL, msg

        # # SQL handling part 2 - re-build SQL date comparisons into integer comparisons  
        # if makeFriendlySQL == "Y":  
        #     oDict = {'=':'=', '>':'>', '<':'<', '>=':'>', '<=':'<' } # dictionary to convert date field operators
        #     newerSQL = ""             
        #     for line in newSQL.split("\n"):    
        #         # monthDict = {'JAN':1, 'FEB':2, 'MAR':3, 'APR':4, 'MAY':5,'JUN':6, 'JUL':7, 'AUG':8, 'SEP':9, 'OCT':10, 'NOV':11, 'DEC':12}
        #         # lineEnd = line.strip()[-11:]
        
        #         if reSearch(r"BETWEEN", line) == True:
        #             print("\nPROBLEM!\n ogrFromBCGW can't successfully translate a BETWEEN operator for dates. Change the sqlQuery and try again.")
        #             sys.exit()
                
        #         # The below conditions show an SQL line has a string including "DATE" (i.e. a date field) being evaluated against a date value
        #         if not all([reSearch(r"DATE", line) == True , reSearch(r"'\d\d-\w\w\w-\d\d'", line) == True]): 
        #             newerSQL += line + "\n" # If these conditions are not met, add the line as is to the new SQL block..
        #         else:
        #             lineStartText, fieldName, operator, day, month, year = parseSQL_DateLine(line, oDict) # FUNCTION CALL

        #             newline1 = "EXTRACT(year FROM {}) {} '{}'".format(fieldName, oDict[operator], year)
        #             newline2 = "or ({0} and EXTRACT(month FROM {1}) {2} '{3}' )".format(newline1.replace(oDict[operator], "="), fieldName, oDict[operator], month)
        #             newline3 = "{0} and EXTRACT(day FROM {1}) {2} '{3}'".format(newline2.replace(oDict[operator], "="), fieldName, operator, day)
        #             newerSQL += lineStartText + " ( " + newline1 + "\n" + newline2 + "\n" + newline3 + ")"
            
            # SQL handling part 3 - check for mismatched / uneven number of brackets
        #     newerSQL = sqlBracketMismatchCheck(newerSQL) # FUNCTION CALL     
        #     msg = "OGR-friendly SQL query is:"
        
        # else:
        #     newerSQL = sqlBracketMismatchCheck(newSQL) # FUNCTION CALL 
        #     msg = "SQL query (date comparison unchanged) is:"
        # return newerSQL, msg
            # newSQL = sqlBracketMismatchCheck(newSQL) # FUNCTION CALL     
            # msg = "OGR-friendly SQL query is:"
        
        # newSQL = sqlBracketMismatchCheck(newSQL) # FUNCTION CALL 
        # msg = "SQL query is:"
        # return newSQL, msg

    sqlQuery, msg = sqlQueryScrubber(sqlQuery, makeFriendlySQL) # FUNCTION CALL 

    print("\n" + msg + "\n","="*len(msg))
    print(sqlQuery)

    # SQL handling - write SQL to a temporary .sql file first, then read it from the external file (ensures UTF-8 compliance)
    make_wrkSpc(r"T:\tempQueryFolder", rsltDict, outPathList) # FUNCTION CALL
    # sqlFile = os.path.join(r"T:\tempQueryFolder","query.sql")  # query.sql will overwrite if running the script repeatedly
    sqlFile = os.path.join(r"T:\tempQueryFolder","query{}.sql".format(n))  # query.sql will overwrite if running the script repeatedly
    with open(sqlFile, 'w') as thing:
        thing.write(sqlQuery)

    progress = '-progress'
    sql = '-sql'
    sqlQ = r"@{}".format(sqlFile)

    # Function to detect placeholders in a fileName, sql statement or any key from .csv file and ensure they get filled before appending to ogrList (and running through ogr2ogr)
    
    ogrItems = [osgeo_bat, ogr_exe, specifySRS, srs_def, f, formatName, fileName, ds, progress, sql, sqlQ]
    for x in ogrItems:
        if not x == fileName:
            string = fillFormatPlaceholders(x) # FUNCTION CALL
        else: 
            specialList = [extDict, outType]
            string = fillFormatPlaceholders(x, specialList) # FUNCTION CALL with optional 'specialList' argument
         
        ogrList.append(string)
    if overWrite == "Y":
        ogrList.append('-overwrite')

    msg = "\nSetting specs for the selected spatial file type: {}".format(outType)
    print("\n{}\n{}".format(msg, "-"*len(msg)))
    lyrName = "{}".format(outName[0:20].replace(" ","_").split("{")[0]) # if there's a placeholder in the outName, avoid ugly { or } in the filename
    # -nln = "New Layer Name"; prevents the output layer from assuming the entire sqlQuery as its name - IMPORTANT!

    if outType == "GPKG": # Set GPKG specific options
       for x in ["-nln", lyrName]:
            ogrList.append(x)

    if outType == "GeoJSON": # Set GeoJSON specific options
        for x in ["-lco","WRITE_NAME=NO","-nln", lyrName]:
            ogrList.append(x)

    if outType == "KML": # Set KML specific options  
        if nameField is not None:
            for x in ["-nln", lyrName, "-dsco", "NameField={}".format(nameField)]: # This would give each KML feature a better name than 'No Name'
                ogrList.append(x)
        else:
            for x in ["-nln", lyrName]:
                ogrList.append(x)

    if outCRS in epsgDict:
        if outType == "KML":
            crsMessage = "Resultant spatial file (KML) automatically converts to CRS:{} ({})".format(4326, epsgDict[4326])
        else:
            crsMessage = "Resultant spatial file will have CRS:{} ({})".format(outCRS, epsgDict[outCRS])
        print(crsMessage)

    make_wrkSpc(outPath, rsltDict, outPathList) # FUNCTION CALL

    # Which Python version you are using determines what subprocess method to use;
    pyVersion = float("{}.{}".format(sys.version_info.major, sys.version_info.minor))
    if pyVersion >= 3.5: # if Python >= 3.5, use subprocess.run
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
        try:
            rc = subprocess.check_call(ogrList)
        except subprocess.CalledProcessError as error:
            print("""Problem! Limited info available due to Python version being {}; try running in Geospatial Desktop (Python 3) to learn more about the problem.
            Exiting script.\n""".format(pyVersion))
            sys.exit()

    newString = ""
    print("\nArguments used:")
    for arg in ogrList:
        print("\t{}".format(arg))
        if ogrList.index(arg) > 0:
            # Startring with argument 1, put a space between arguments in the ogr2ogr string
            if ogrList.index(arg) == ogrItems.index(formatName): # index of the formatName / driver argument
                newString += '"{}" '.format(arg) # OGR requires driver has "" aroudn it 
            else:
                newString += '{} '.format(arg)

    cliStringList.append(newString)
    outNamesList.append(outName)
    ogrMultiList.append(ogrList)

    return ogrList

###############################################################################################################
###############################################################################################################
###############################################################################################################

# Choose params file
paramsFileName = 'ogrParams.csv' # this is the default
# paramsFileName = 'ogrParams_999.csv' 
ogrParamsFile = checkParamsFile(paramsFileName) # FUNCTION CALL - make sure the params file exists

# Get all parameters from the .csv file
dList, nameDict, paramNum = readCSVtoDict(ogrParamsFile) # FUNCTION CALL - each dict in dList is a <class 'collections.OrderedDict'> returned from csv.DictReader
# print(list(nameDict.items())) # useful for debugging...

resultantLists = ogrReadTheseColumns() # FUNCTION CALL

# Get users BCGW info and verify it's in the correct format
print("")
user = input("Enter your BCGW username:")
pWord = input("Enter your BCGW password:")

overwrite = ""
while overwrite not in ["Y","N"]:
    overwrite = input("Do you want to overwrite existing output folders? Type Y or N.")
    overwrite = overwrite.upper()
else:
    msg = "Folders will be overwritten.\n" if overwrite == "Y" else "Folders will not be overwritten.\n"
    print(msg)

# bcgwLoginCheck(user, pWord) # FUNCTION CALL - terms are too strict; do not use this

###############################################################################################################
# Run each set of parameters through the ogr2ogr call

outPathList = [] # needed to know when to overwrite folders
for n in range(paramNum): # paramNum is the number of parameter rows in your .csv file
    paramStr = resultantLists[n].strip() # get string value of the cell i.e. outPath, outName, curDate, sqlQuery, outType
    paramList = [x.strip() for x in paramStr.split(",")]
    name = list(nameDict.keys())[n]
    print(paramList)
    rsltDict = getVariableDicts(paramList, name, dList, nameDict, paramsFileName) # FUNCTION CALL
    outPathList.append(rsltDict['outPath'])
    # print(rsltDict.items()) # optional - Verbose!
    ogrList = ogrFromBCGW(user, pWord, n, rsltDict['outPath'], rsltDict['outName'], rsltDict['sqlQuery'], rsltDict['outType'])

# def ogrFromBCGW(user, pWord, n, outPath, outName, sqlQuery, outType="GPKG", overWrite = "Y", makeFriendlySQL = "N", outCRS=3005, coordPrec=1, nameField=None):   
##################################################################################

msg ="{} ogr strings created and executed successfully.".format(len(cliStringList))
print("\n\n", msg)

for c in cliStringList:
    print("-"*100, "\n{}".format(c))
print("-"*100, "\n")

# os.rmdir(r"T:\tempQueryFolder")