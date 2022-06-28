
# Using ogr to retrieve data from BCGOV databases
Last updated: March 23, 2021

__ogrFromDB__ is a Python script package to create and execute multiple ogr2ogr CLI strings. You can find the script and parameters .csv file
[here](../ogrFromDB/).

It is an easy and fast way to convert spatial data from any BC Government Oracle database (i.e. BCGW and more)
and save it in a variety of output formats:
['GeoJSON', 'KML', 'LIBKML', 'ESRI Shapefile', 'GPKG', 'CSV']

The script works on the GTS Kamloops Desktop - Geospatial, but may not work on other GTS Desktops

(The info below is all written in Lines 12 - 72 of ogrFromDB_csv.py)

This script takes all user input via the ogrParams.csv file, which is pre-loaded with an example SQL query on a BCGW table (current year fire polygons in Southeast Fire Centre)

CHECK/BE AWARE OF THESE THINGS BEFORE RUNNING SCRIPT:
--------------------------------------------------------------------------------------
IT'S VERY IMPORTANT THAT THESE FILES ARE IN THE SAME FOLDER WHEN RUNNING THIS SCRIPT:
1. ogrFromDB_csv.py
2. ogrParams.csv
--------------------------------------------------------------------------------------

0. Each row in ogrParams.csv is a set of values you are feeding into the ogrFromDB_csv script.
Each column header becomes a key name in the dictionary generated from each row, and row values become the dictionary values.

1. The following columns MUST have values for ogrFromBCGW to run: paramName, outPath, outName, outType, sqlQuery
paramName - a simple string like harvestParams. IT'S VERY IMPORTANT THAT THIS IS UNIQUE FOR EACH ROW !
outPath - location to save output to (will be created if it doesn't exist). Cannot have a .format operator in it.
outName - name of your output file (no extension, but placeholders are OK)
outType - type of file ex. GPKG, KML
sqlQuery - a query to draw the result from the BCGW. IMPORTANT - TEST IT BEFORE USING IN THIS SCRIPT
ogrReadTheseColumns - this is a comma-seperated text list that tells the script which values to read in. The order doesn't matter

This column is optional; this is what they do in this script:
paramDescription - a description of what output each row creates

Any remaining columns are customized to the outputs of the script,
or are meant be passed on to another script that uses the results of this script:
curDate - used to put the run date in file names
harvestSinceWhen, fireStartYear  - these are date and integer values that might feed into the SQL queries for each output, to make the query easily adjustable
dsDict, dataSources, data_OG_dict, oldGrowthLayerNames - these are values that point to data sources and output latyer names for the old growth harvest resultant

The order of the columns does not matter, as long as the right values are under the right heading.

2. The .csv fileName is contained in the 'paramsFileName' variable (Line ~540 in this script), 
which is set by default to 'ogrParams.csv'
If you change the name of the .csv file, update this variable.

3. As you update the .csv, make sure you keep string formats the same way:
i.e. if a date is expressed as '01-JUL-18', don't change it to 'July 1, 2018'. And don't lose the single quotes.

IF YOU MAKE CHANGES, REMEMBER TO SAVE THE .CSV FILE BEFORE RUNNING THIS SCRIPT !

4. It's safe to disregard the 'ERROR 1: ORA-04043: object no_Table does not exist' message that will print to the console - that's just a way of preventing
   ogr2ogr from scanning all tables in the BCGW once it connects...

5. If the script fails with 'ERROR 1: Layer 'layer1' does not already exist in the output dataset, and cannot be created by the output driver',
   this can be corrected by entering a new 'outName' value in the ogrParams.csv file.

6. Avoid using dashes in GPKG layer names (i.e. roads-non-status) as it makes them unreadable in ArcGIS

7. Most BCGW datasets are in BC Albers; default output is in BC Albers projection (EPSG: 3005) with coordinates to nearest 0.1 metres

8. For KML files, the nameField (name of each placemark as seen in Google Earth) can be set using the nameField parameter
   in the 'ogrFromDB' function call (Line ~600 in this script).  nameField=None is the default parameter, but in this script it's currently set to "FIRE_NUMBER"

9. Layer names are created based on the 'outName' value in the ogrParams.csv file;
with a maximum default length of 30 characters, and all spaces replaced by underscores.
To increase or decrease the maximum characters length, change the 'nameLengthMax' variable (Line ~470 in this script)

10. If outputting an ESRI Shapefile, it's normal to see 'Warning 6: Normalized/laundered field name:' This reducess field names to 10 characters long, which is the max length for a shapefile field.



