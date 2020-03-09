
README - how to run ogrFromBCGW_csv_FINAL.py (with .csv inputs)
===========================================================
Last updated: February 27th, 2020

Note: if you got this from GitHub, refer to the readme.md instead - it's much easier to follow!
-----------------------------------

Welcome to the ogrFromBCGW tool! This is a fully open-source script tool (no arcpy, no ESRI) that uses GDAL/OGR to
grab any data subset from BCGW and save it in a variety of spatial formats. It runs on the DTS, on either the Geospatial Desktop or the ArcGIS 10-6 Desktop.

Using SQL to define those datasets, the script creates and executes *multiple* ogr2ogr CLI strings, based on parameters held in a .csv file. Available output formats are:
{"GeoJSON":".json", "KML":".kml", "ESRI Shapefile":".shp", "GPKG":".gpkg"}

The script automatically reads from any of the rows supplied in the default .csv file, ogrParams.csv , to calculate the resultants specified in each row. Editing the .csv rows allows the user to create their own spatial outputs. (The supplied .csv has three example output datasets). 

--------------------------------------------------------------------------------------
IT'S VERY IMPORTANT THAT THESE FILES ARE IN THE SAME FOLDER WHEN RUNNING THIS SCRIPT:
1. ogrFromBCGW_csv_FINAL.py
2. ogrParams.csv
--------------------------------------------------------------------------------------

When the script is finished running, each output spatial files is saved to the 'outPath' folder specified in the .csv file for that row. 

A good practice it to save each results to T:, which is temporary drive regenerated each time you start a new DTS session, in new folders starting with _ (ex. _fires, _harv, _oldGrowthResults) so they are found easily at the top of the T: file folder.
If you wish to keep results saved to T:, you must cut and paste the files to another drive.

This script will not overwrite any exitsing output folders - to run a script mukltiple times, you must either delete the original output folder (i.e. T:\_harv) or provide a new 'outPath' in the .csv file.

EASIEST WAY TO RUN THIS SCRIPT TOOL: cmd.exe
---------------------------------------------
The easiest way to run this code is via cmd.exe in the Geospatial Desktop or ArcGIS 10-6 Desktop.
0. copy the folder containing the required Python scripts to a new location:
   
Copy this folder:
   \\spatialfiles2.bcgov\work\FOR\RSI\DKL\General_User_Data\gamos\Projects\2020\ogrFromBCGW_csv_FINAL

to whatever directory you want to run it from. Suggestion: copy it to T: on your DTS desktop

1. open cmd.exe (type cmd in the Windows search, open cmd)
2. use the 'cd' command to change the directory to where you copied the "ogrFromBCGW_csv_FINAL" folder to:
    ex. cd T:\ogrFromBCGW_csv_FINAL  <hit enter>
3. type in the drive letter you copied the folder to to switch to that drive:  ex. T:    <hit enter>
4. now the important part: choose the right Python path to run the script from.

   Python path on the 10.6 DTS environment is: "E:\sw_nt\QGIS 3.8\apps\Python37\python.exe"
   (Note the lack of underscore in QGIS 3.8 and the different slash direction.)
   Python path on the Geospatial Desktop DTS environment is: "E:/sw_nt/QGIS_3.8/apps/Python37/python.exe"
   The main script is: ogrFromBCGW_csv_FINAL.py

   So, in 10.6, do this (assuming your current working directory is now: T:\ogrFromBCGW_csv_FINAL> ):
   T:\ogrFromBCGW_csv_FINAL>"E:\sw_nt\QGIS 3.8\apps\Python37\python.exe" ogrFromBCGW_csv_FINAL.py

   If you're on the Geospatial Desktop, do this:
   T:\ogrFromBCGW_csv_FINAL>"E:/sw_nt/QGIS_3.8/apps/Python37/python.exe" ogrFromBCGW_csv_FINAL.py

5. The script will start running and quickly prompt you to enter your BCGW username and password.

With the default rows in ogrParams.csv, the script should take about 1 minute to run.  


MODIFYING THE .csv's INPUT VARIABLES
-------------------------------------
The .csv fileName is contained in the Python script in the 'paramFileName' variable (set by default to 'ogrParams.csv').
If you change the name of the .csv file, you'll have to update this variable in the Python script ( Use Ctrl + F to find it, around Line 500 ).

As you update values in the .csv, make sure you keep any date strings expressed as '01-JUL-18' (don't change it to 'July 1, 2018'. And don't lose the single quotes.)

CSV STRUCTURE

Column A | Column B   	   | Column C | Column D | Column E | Column F  | Column G	      | Column H etc..
paramName| paramDescription| outPath  | outName  | outType  | sqlQuery  | ogrReadTheseColumns | custom1 etc...
REQUIRED | OPTIONAL 	   | REQUIRED | REQUIRED | REQUIRED | REQUIRED  | REQUIRED  	      | ALL OPTIONAL 	    

0. Each row in ogrParams.csv is a set of values you are feeding into the ogrFromBCGW_csv_FINAL.py script.
Each column header becomes a key name in the dictionary generated from each row, and row values become the dictionary values.

1. The following are REQUIRED columns for ogrFromBCGW (must have values):
paramName, outPath, outName, outType, sqlQuery, ogrReadTheseColumns

paramName - a simple name for the set of values found in each row
Examples: harvestParams, wildfireParams

outPath - location to save output to (will be created if it doesn't already exist). It's fine to use the same outPath for several output files.
Examples: T:\_test, W:\FOR\RSI\DKL\General_User_Data\gamos\test

outName - name of your output file (no extension, but placeholders are OK)
Examples: miningTenures, DSE_wildfires_{key0}_onwards.format(fireStartYear)
If using format placeholders, must use key0, key1 etc. in the {} 

outType - type of file ex. GPKG, KML . Selecting this will automatically create the file extension.
Examples: GeoJSON, KML, ESRI Shapefile, GPKG

sqlQuery - a query to draw the result from the BCGW. IMPORTANT - TEST IT BEFORE USING IN THIS SCRIPT!
Make sure the entire SQL query string is copied into a single cell. You don't need to surround the SQL string in triple quotes.
 
Query Example 1: 
select owner_name, client_number_id, geometry
from WHSE_MINERAL_TENURE.MTA_ACQUIRED_TENURE_SVW ten
where tenure_type_code in ('M', 'P')

Query Example 2: 
select FIRE_NUMBER, shape, FIRE_YEAR, FIRE_DATE
from WHSE_LAND_AND_NATURAL_RESOURCE.PROT_HISTORICAL_FIRE_POLYS_SP fires
where FIRE_YEAR >= {key0} and FIRE_NUMBER like 'N%'.format(fireStartYear)

Query Example 3: must use a to_date conversion if using a date comparison
select CUT_BLOCK_FOREST_FILE_ID, GEOMETRY 
where GEOGRAPHIC_DISTRICT_CODE IN ('DSE')
and BLOCK_STATUS_DATE >= to_date({key0}, 'DD-MON-YY').format(harvestSinceWhen)

Note on sqlQuery - this is an Oracle SQL query, which you can create and verify as correct using Oracle SQL developer. This is where the power of ogr2ogr is realized - it can create BCGW subsets quite quickly, especially when using Oracle spatial data operator (SDO) statements . 

ogrReadTheseColumns - this is a comma-seperated text list that tells the script which columns to read in from the .csv. The order doesn't matter. The default is: outPath, outName,sqlQuery,outType   (but other column names, if used in the outName or sqlQuery, would need to be included). The order of items doesn't matter.

Example 1: outPath, outName,sqlQuery,outType
Example 2: outPath,  fireStartYear, outName,curDate,sqlQuery,outType


The paramDescription value is optional; it's just a description of what output each row helps create.

Any remaining columns are there to help easily adjust the SQL statement (i.e. harvestSinceWhen or fireStartYear) or are variables required if chaining this script's output into a QGIS script (ex. dsDict, dataSources, etc.).


The order of the columns does not matter, as long as the right values are under the right heading.


2. The following are OPTIONAL columns for ogrFromBCGW: Column H and everything to the right
   These are all column names for custom variables that the script might need to create useful file names or to easily modify an sqlQuery. Columns 'harvestSinceWhen', 'fireYear', 'dsDict' in the default ogrParams.csv are all examples of optional columns.



The .csv fileName is contained in the paramFileName variable (set by default to 'ogrParams.csv').
If you change the name of the .csv file, update this variable ( Use Ctrl + F to find it, around Line 500 )



RUNNING THIS SCRIPT TOOL IN VISUAL STUDIO CODE (on Geospatial Desktop)
-----------------------------------------------------------------------
Visual Studio Code is the default Python scripting environment on the Geospatial Desktop and it's really good.

To ensure all system path variables are OK ( i.e. make sure the QGIS boilerplate .py files will run OK), you'll want to make sure the pythonPath is set to:

DTS 10.6 >>> "E:\sw_nt\QGIS 3.8\apps\Python37\python.exe"
Geospatial Desktop >>> "E:/sw_nt/QGIS_3.8/apps/Python37/python.exe"



There are several ways to do this:

1. Launch VS Code via the vscode-qgis.txt on the desktop of Geospatial Desktop, if you have that file. (If not, you can ask Will Burt for it.)

2. Launch VS Code the normal way, then do File > Open Folder.. and choose the 'ogrFromBCGW_csv_FINAL' folder. Then select the 'Python 3.7.0 64-bit' option at the bottom left corner to set the Python path

2. Launch VS Code the normal way, then edit the settings.json to have the Python path read as follows (the VS Code default is usually >>> "python.pythonPath": "E:\sw_nt\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python3.exe):
Be mindful of forward slashes vs. backslashes.


{
    "python.dataScience.sendSelectionToInteractiveWindow": false,
    "window.zoomLevel": 1,
    "python.pythonPath": "E:/sw_nt/QGIS_3.8/apps/Python37/python.exe",
    "python.disableInstallationCheck": true,

"workbench.colorCustomizations": {
    "editor.selectionBackground": "#135564",
    "editor.selectionHighlightBackground": "#135564",
    "editor.selectionHighlightBorder": "#FFFA",
    "editor.tokenColorCustomizations": {

        "comments": "#8fee58"
    },

}




Questions, comments, etc. 
============================
gregory.amos@gov.bc.ca
GIS Technician (auxiliary) / Kootenay Boundary Region / Ministry of Forests, Lands and Natural Resource Operations and Rural Development





