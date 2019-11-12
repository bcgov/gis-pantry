
# Script to create a working ogr2ogr CLI string for use with OsGeo4W.
# Make sure "outPath" exists before trying to run this script
# Default output is in BC Albers projection with coordinates to nearest 0.1 metres

# Output data types this script allows: GeoJSON, KML, ESRI Shapefile, and GeoPackage (QGIS' native format)

def ogr2ogrFromBCGW(outType, outPath, outName, user, pword, sqlQuery, outCRS = 3005, coordPrec = 1):
    epsgDict = {3005: "BC Albers", 3741: "NAD83(HARN) / UTM zone 11N", 4326:'WGS 84', 104199:"GCS_WGS_1984_Major_Auxiliary_Sphere"}
    extDict = {"GeoJSON":".json", "KML":".kml", "ESRI Shapefile":".shp", "GPKG":".gpkg"}
    ociString = "OCI:{}/{}@IDWPROD1:junk".format(user,pword)
    message = 'Paste the following into the OSGeo4W shell and hit enter:'
    fullString = message + "\n" + "-"*len(message) + "\n"
    fullString += 'ogr2ogr -a_srs epsg:{} -f "{}" {}\{}{} {} -sql "{}" -progress'.format(outCRS, outType, outPath, outName, extDict[outType], ociString, sqlQuery)

    # Set GeoJSON specific options
    if outType == "GeoJSON":
        fullString += " -lco WRITE_NAME=NO" # prevents the JSON layer from assuming the entire sqlQuery as its name 

    # Set GPKG specific options    
    if outType == "GPKG":
         fullString += " -lco IDENTIFIER='layer1' -lco DESCRIPTION='layer1'" # ensures layer name = "layer1" in the GPKG file. 

    # Set KML specific options    
    if outType == "KML":
        # fullString += " -dsco NameField= '{}'".format(outName) # prevents the KML layer from assuming the entire sqlQuery as its name 
        fullString += " -nln '{}'".format(outName) # prevents the KML layer from assuming the entire sqlQuery as its name 

    # If outCRS is WGS 84, set high coordinate precision (13 decinmal places)
    if any([outCRS != 4326, outType == "KML"]): # 4326 = WGS84 = decimal degrees, which needs as many decimal places as possible . KML driver ourCRS is always 4326
        coordPrec = 13
        lcoPrec = "-lco COORDINATE_PRECISION={}".format(coordPrec) 
    else:
        lcoPrec = ""
    fullString += " " + lcoPrec

    if outCRS in epsgDict:
        if outType != "KML":
            fullString += "\n\nResultant spatial file will have CRS:{} ({})".format(outCRS, epsgDict[outCRS])
        else:
            fullString += "\n\nResultant spatial file (KML) always has CRS:{} ({})".format(4326, epsgDict[4326])

    return str(fullString)


# Usage example - create an ogr2ogr string to output a JSON file for all TSAs in RKB

tDict = {'Arrow TSA':1, 'Boundary TSA':2, 'Cranbrook TSA':5, 'Golden TSA':7, 'Invermere TSA':9, 'Kootenay Lake TSA':13, 'Revelstoke TSA':27 } # for reference

outPath = r"T:\testFolder"
outName = r"RKB_TSAs55"
sqlQuery = r"select * from WHSE_ADMIN_BOUNDARIES.FADM_TSA where TSB_NUMBER is null AND RETIREMENT_DATE IS NULL AND TSA_NUMBER IN (1,2,5,7,9,13,27)"
# sqlQuery = r"select * from WHSE_ADMIN_BOUNDARIES.FADM_TSA where TSB_NUMBER is null AND RETIREMENT_DATE IS NULL AND TSA_NUMBER IN (9)"
# user = "USERNAME"
# pWord = "BCGW_PASSWORD"
user = "GAMOS"
pWord = "Oracle9999"

# ogrLine = ogr2ogrFromBCGW("GPKG", outPath, outName, user, pWord, sqlQuery)   # creates a GeoPackage file (QGIS native format) in BC Albers
# ogrLine = ogr2ogrFromBCGW("GeoJSON", outPath, outName, user, pWord, sqlQuery)  # creates a JSON file in BC Albers
# ogrLine = ogr2ogrFromBCGW("GeoJSON", outPath, outName, user, pWord, sqlQuery,outCRS = 4326)  # creates a JSON file in WGS 84
# ogrLine = ogr2ogrFromBCGW("ESRI Shapefile", outPath, outName, user, pWord, sqlQuery) # creates a Shapefile in BC Albers
ogrLine = ogr2ogrFromBCGW("KML", outPath, outName, user, pWord, sqlQuery) # creates a KML in WGS 84 (KML driver allows only WGS 84 as an output CRS)

print(ogrLine)