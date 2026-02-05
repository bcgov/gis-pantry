# Author: Jeremiah Podleski
# Ministry, Division, Branch: WLRS - GeoBC - Atlas Unit
# Created Date: 2024-08
# ------------------------------------------------------------------------------
# SUMMARY

# Calculates coordinates for the ABMS Map Point features. 
# Coordinates include UTM and NAD83 Lat/Long
# It will calculate coordinates for all records if no selection. It will calculate coordinates
# for selected features only if there is a selection.

# REQUIREMENTS // INPUT / OUTPUT NOTES
# INPUT: ABMS Map Point Feature Class or Layer
# Fields with the expected field names that hold the values we will calculate
# A field called "UTM_ZONE" that is pre-populated with the UTM zone of each point
#   + We cannot auto-calculate UTM zone, because maps are currently only allowed one UTM zone even
#     if cross more than one. 
# ------------------------------------------------------------------------------
# IMPROVEMENTS
# Various :)
# ------------------------------------------------------------------------------
# HISTORY

#   Date      Initial/IDIR  Description
# | ----------------------------------------------------------------------------
#   2024-08     jpodlesk    Created script
#   2025-02     hfrost      Updated script to use UTM zone from input table to calculate points
           
# ** IMPORTS
import arcpy
import sys

# ** PARAMETERS

# Get user params from tool *IF* ran from tool...
if len(arcpy.GetParameterAsText(0)) > 0: 
    INPUT_FC = arcpy.GetParameterAsText(0) 
else:
    #! NOTE: enter hard coded values here if running from terminal/notebook...
    INPUT_FC = (r'path\to\dev\data')

# fc info - (Determine: Layer or FC on disk?, selection set?)
if arcpy.Exists(INPUT_FC) and arcpy.Describe(INPUT_FC).dataType == "FeatureClass":
    INPUT_ROW_COUNT = int(arcpy.GetCount_management(INPUT_FC).getOutput(0))
    FC_SELECTION_SET__LIST = 'NONE - IS FEATURE CLASS'

elif arcpy.Exists(INPUT_FC) and arcpy.Describe(INPUT_FC).dataType == "FeatureLayer":
    INPUT_ROW_COUNT = int(arcpy.GetCount_management(INPUT_FC).getOutput(0))
    FC_SELECTION_SET__LIST = arcpy.Describe(INPUT_FC).FIDSet.split(';')

BC_ALBERS_SR = arcpy.SpatialReference(3005) 
NAD83_SR =  arcpy.SpatialReference(4269)

valid_utm_zones = [8, 9, 10, 11]

# existing fields to use
UTM_X_FIELD = 'UTM_EASTING'
UTM_Y_FIELD = 'UTM_NORTHING'
NAD83_X_FIELD = 'LONGITUDE'
NAD83_Y_FIELD = 'LATITUDE'
UTM_ZONE = 'UTM_ZONE'

EXPECTED_FIELDS__SET = {UTM_X_FIELD, UTM_Y_FIELD, NAD83_X_FIELD, NAD83_Y_FIELD, UTM_ZONE}

# ** FUNCTIONS
def jprint(in_string=None):
    '''
    Determines where script is running (pro script tool, terminal, or notebook)
    and uses correct print command.

    This was helpful when first developing in notebooks in ArcPro.
    Replace as desired.
    '''
    if len(arcpy.GetParameterAsText(0)) > 0:
        arcpy.AddMessage(in_string)
    else:
        print(in_string)

# ** MAIN
        
# 1. PREP AND REPORTING
# --------------------------------------------------------------------------
        
# report on input data
jprint('Tool settings...')
jprint(f'Input feature class: {INPUT_FC}')

# check for existing fields and report...
input_field__set = set([field.name for field in arcpy.ListFields(INPUT_FC)])

if EXPECTED_FIELDS__SET.issubset(input_field__set):
    jprint('\nFound all needed fields')
else:
    arcpy.AddError("One or more of the required fields do not exist in the feature class.")
    arcpy.AddError(f"Please ensure that these fields exist in the feature class\n"
                   f"{EXPECTED_FIELDS__SET}")
    sys.exit()

# report on selection and count of the records...
if (FC_SELECTION_SET__LIST) == 'NONE - IS FEATURE CLASS':
    jprint(f'\nInput is a feature class on disk. ALL (( {INPUT_ROW_COUNT} ))'
           ' records will be updated!')
elif (FC_SELECTION_SET__LIST)[0] == '':
    jprint(f"\nThere is no selection.\nThe script will update all (( {INPUT_ROW_COUNT} )) "
           "records in the input feature class...")
else:
    jprint(f'{FC_SELECTION_SET__LIST}')
    jprint(f'\nALERT: {len(FC_SELECTION_SET__LIST)} records are selected.\n'
           'The script will update the selected records...')

# list to store problematic feature IDs
null_utm_zones = []
invalid_utm_zones = []

# find and report any features that do not have UTM zone set...
jprint('\nSearching through coordinates...')
with arcpy.da.SearchCursor(INPUT_FC, ['OBJECTID', UTM_ZONE]) as cursor:
    for row in cursor:
        object_id = row[0]
        utm_zone = row[1]

        # check if UTM coordinates are null and log the issue. Coordinates for these features
        # will not be updated...
        if utm_zone is None:
            arcpy.AddWarning(f'WARNING: UTM zone is null for OBJECTID {object_id}.')
            null_utm_zones.append(object_id)              

        if utm_zone not in valid_utm_zones:
            arcpy.AddWarning(f'WARNING: UTM Zone {utm_zone} is not an accepted value for'
                             f'OBJECTID {object_id}.')
            invalid_utm_zones.append(object_id)             

# 2. UPDATE COORDINATE FIELDS
# --------------------------------------------------------------------------
    
# update coordinates with cursor...
jprint('\nUpdating coordinates...')
with arcpy.da.UpdateCursor(INPUT_FC, 
                           ["OBJECTID", "SHAPE@", UTM_X_FIELD, UTM_Y_FIELD,
                            NAD83_X_FIELD, NAD83_Y_FIELD, UTM_ZONE]) as cursor:
    # Iterate over each feature in the input feature class
    count = 0
    for row in cursor:
        UTM_ZONE_VALUE = row[6]
        object_id = row[0]

        # check if OBJECTID is in the lists of problematic ids
        if object_id in invalid_utm_zones or object_id in null_utm_zones:
            jprint(f'Skipping OBJECTID {object_id} due to invalid or null UTM zone.')
            continue 

        try: 
        # get feature geometry... (Data is in BC_Albers so shape.centroid is in BC Albers)
            shape = row[1]
            bc_albers_centroid = shape.centroid

            # spatial refs
            if UTM_ZONE_VALUE == 8:
                UTM_SR = arcpy.SpatialReference(26908)  
            elif UTM_ZONE_VALUE == 9:
                UTM_SR = arcpy.SpatialReference(26909)  
            elif UTM_ZONE_VALUE == 10:
                UTM_SR = arcpy.SpatialReference(26910)  
            elif UTM_ZONE_VALUE == 11:
                UTM_SR = arcpy.SpatialReference(26911)
            else:
                raise ValueError(f'Invalid UTM Zone attribute: {UTM_ZONE_VALUE}. Please fix.')
                        
            # project centroid to UTM, and get x,y...
            utm_centroid = arcpy.PointGeometry(bc_albers_centroid, BC_ALBERS_SR).projectAs(UTM_SR)
            utm_x = utm_centroid.firstPoint.X
            utm_y = utm_centroid.firstPoint.Y

            # project centroid to NAD 83 lat and long, and get x,y...
            nad83_centroid = arcpy.PointGeometry(bc_albers_centroid, BC_ALBERS_SR).projectAs(NAD83_SR)
            nad83_x = nad83_centroid.firstPoint.X
            nad83_y = nad83_centroid.firstPoint.Y

            # Update the row with the UTM and NAD83 coordinates
            row[2] = utm_x
            row[3] = utm_y
            row[4] = nad83_x
            row[5] = nad83_y

            # Update the cursor
            cursor.updateRow(row)
            count += 1
        except IndexError as e:
            print(f'IndexError while processing OBJECTID {row[0]}: {str(e)}')
            continue
        except Exception as e:
            print(f'Error processing OBJECTID {row[0]}: {str(e)}')
            continue 

print(f'{count} rows processed successfully.')

# 3. WRAP-UP
# --------------------------------------------------------------------------
        
jprint('\nWhoooooooooosh........!')
jprint("\nScript finished without errors")
jprint(f'{count} rows updated.')