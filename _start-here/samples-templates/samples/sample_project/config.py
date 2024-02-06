# --------------------------------------------------------------------------------------------------
# Config for main.py
# --------------------------------------------------------------------------------------------------

# PARAMETERS
# --------------------------------------------------------------------------------------------------
project_folder = r"" # local project folder
landscape_unit_names = ("")  # tuple of valid LU names
protected_area_types = ("")  # tuple of valid PA types

# Other config
# --------------------------------------------------------------------------------------------------

# derived parameters
data_folder = f"{project_folder}\\data"
working_gbd = f"{data_folder}\\working.gdb"
final_gbd = f"{data_folder}\\final.gdb",
excel_folder = f"{project_folder}\\excel"

# constants
LANDSCAPE_UNITS_REST_URL = "https://maps.gov.bc.ca/arcgis/rest/services/whse/bcgw_pub_whse_land_use_planning/MapServer/7"  #https://governmentofbc.maps.arcgis.com/home/item.html?id=71fae301572f4ae7b1135d40a69caa31
PROTECTED_AREAS_REST_URL = "https://services6.arcgis.c@om/ubm4tcTYICKBpist/arcgis/rest/services/British_Columbia_Parks_Ecological_Reserves_and_Protected_Areas/FeatureServer/0"  # https://governmentofbc.maps.arcgis.com/home/item.html?id=6773e6a38f2749808679c7c712e2f79b

# arcpy envs
arcpy.env.overwriteOutput = True
arcpy.env.workspace = working_gbd
