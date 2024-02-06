# --------------------------------------------------------------------------------------------------
# Author: Laurence Perry
# Ministry, Division, Branch: EMLI, MCAD, Regional Operations
# Updated: 2023-11-08
# Description:
#     THIS IS A DEMO SCRIPT INTENDED TO DEMONSTRATE GIS PANTRY STANDARDS. There are many ways to
#     be in compliance with standards, your code need not look exactly the same.
#
#     This script creates reports on the area of selected Parks, Eco Reserves and Protected Areas
#     within selected Landscape Units. Data is acquired from BC Map Hub feature layers and processed
#     using ArcPy and Pandas. Working files and deliverables are generated within user specified
#     project folder. Deliverables are an excel workbook and a geodatabase feature class.
#     User parameters are a project folder, landscape unit names (given in a tuple), and protected
#     area types (also given in a tuple). These can be adjusted in config.py.
#     
# --------------------------------------------------------------------------------------------------

import arcpy
import pandas as pd
from os import makedirs
from os.path import basename
from config import *
from functions import *

# 1 - Create folders and geodatabases
# --------------------------------------------------------------------------------------------------
print("Setting up folders and geodatabases...")

makedirs(data_folder, exist_ok=True)
makedirs(excel_folder, exist_ok=True)

if not arcpy.Exists(working_gbd):
    arcpy.management.CreateFileGDB(data_folder, basename(working_gbd))

if not arcpy.Exists(final_gbd):
    arcpy.management.CreateFileGDB(data_folder, basename(final_gbd))


# 2 - Data acquisition from BC Map Hub Feature Layer REST services
# --------------------------------------------------------------------------------------------------
print("Getting Data...")

# export selected Landscape Unit/Parks data from AGOL feature layers to working geodatabase
get_data_from_rest(LANDSCAPE_UNITS_REST_URL, "landscape_units",
                   f"LANDSCAPE_UNIT_NAME in {landscape_unit_names}")

get_data_from_rest(PROTECTED_AREAS_REST_URL, "protected_areas",
                   f"PROTECTED_LANDS_DESIGNATION in {protected_area_types}")


# 3 - ArcGIS Data Analysis and Processing
# --------------------------------------------------------------------------------------------------
print("Processing Data...")
# Identity of selected Landscape Units with protected areas
arcpy.analysis.Identity("landscape_units", "protected_areas",
                        "lus_w_protected_areas")

# Remove unnecessary fields and calculate area in hectares
keep_fields = [
    "LANDSCAPE_UNIT_NAME", "PROTECTED_LANDS_DESIGNATION",
    "PROTECTED_LANDS_NAME"
]
arcpy.management.DeleteField("lus_w_protected_areas", keep_fields,
                             "KEEP_FIELDS")

arcpy.management.CalculateField("lus_w_protected_areas", "AREA_HA",
                                "!shape.area@hectares!", "PYTHON3")

# copy to final geodatabase
arcpy.conversion.FeatureClassToFeatureClass("lus_w_protected_areas", final_gbd,
                                            "lus_w_protected_areas_final")


# 4 - Pandas Data Analysis
# --------------------------------------------------------------------------------------------------
print("Calculating/Creating Excel Report..")

# Convert lus_w_protected_areas_final to pandas dataframe
arcpy.env.workspace = final_gbd
df = feature_class_to_dataframe("lus_w_protected_areas_final")
df["AREA_HA"] = df["AREA_HA"].astype(float)

# Calculate a new field with the area of protected lands in hectares, ignoring non-protected
# area within the landscape unit. This allows for summing total lu area and total protected area
# separately and calculating the percentage of protected area within the landscape unit.
df["PROTECTED_AREA_HA"] = df.apply(lambda row: row["AREA_HA"]
                                   if row["PROTECTED_LANDS_NAME"] != "" else 0,
                                   axis=1)

# Aggregate areas by landscape unit name, sum protected area and total lu area
df = df.groupby("LANDSCAPE_UNIT_NAME").agg({
    "AREA_HA": "sum",
    "PROTECTED_AREA_HA": "sum"
})

# Calculate percentage of protected area
df["PERCENTAGE_PROTECTED"] = df["PROTECTED_AREA_HA"] / df["AREA_HA"] * 100

# Export final to excel
df.to_excel(f"{excel_folder}\\selected_lus_w_selected_protected_areas.xlsx")
