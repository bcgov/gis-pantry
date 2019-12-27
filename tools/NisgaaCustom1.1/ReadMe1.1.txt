README.txt
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# Name:                       Advanced Geospatial Analysis
#                            CUSTOM -- Import--Clip--Append
#                                    version 1.1
#
# Author:      James Burton|Government of British Columbia
#              Geospatial Analyst: Sitkine-Skeena District
#
# Created:     December 2019
#
# Introduction:The primary purpose of this tool is to recieve data from the
#              user, clip the data to the study area, compare shapefile names
#              to a preexisting .xlsx and populate a column based on if the
#              layer is present or absent within the study area, or
#              alternatively if the layer was not included in the analysis.
#              Additional layers included in the analysis but do not meet the
#              criteria headings in the xlsx are appended to the bottom of the
#              spreadsheet. Layers are determined to be present or absent
#              through the calculation of total area after being clipped to
#              study area.
#
#              For a more general application of this tool, please see the
#              GENERAL -- Import -- Clip -- Create xlsx tool which include the
#              framework for additional geometery types. This general purpose
#              tool pairs well with the GENERAL -- Weighted Overlay Script.
#
# Specifics:   In order for this tool to preform optimally, please consider the
#              following items:
#                  1. This tool is for use with FGDB shapefiles.
#                  2. Please ensure shapefiles are named 'Noun_HabitatType_etc'.
#                       For example: "Plants_Freshwater" or "Steelhead_Marine"
#                  3.
#
#              To begin, enter your original GDB file path. Be sure to enter
#              this file path within double or single quotation marks
#              (" " or ' ').
#
#              Second, enter your xlsx template file path. Be sure to enter
#              this file path within double or single quotation marks
#              (" " or ' ').
#
#              The program will, upon successful confirmation of the file paths,
#              begin to execute. The program will create a TEMPORARY FOLDER
#              which will house a TEMPORARY GDB. The delete code is included as
#              a safety measure within the CreateTemp function, and if added to
#              the conclusion of the script, will delete the TEMPORARY items.
#
#              The program will confirm the existance of the template report to
#              copy and populate. Version 2 of this code should feature the
#              creation of a blank xlsx in the event no template exists.
#
#              The program will then copy all the polygon shapefiles from the
#              original GDB to the temp GDB. The study area will be isolated
#              from the polygons. The copied shapefiles are ammended to include
#              a new field in the attribute table to display area
#              (in Hectares, as "POLY_AREA").
#
#              Freshwater salmon species ranges are merged together, with the
#              original, idividual layers being discarded after merger.
#
#              All polygon shapefiles, excluding the study area, are clipped to
#              the extent of the study area.
#
#              The xlsx is then opened and three dictionaries are created.
#              Dictionary one is of column one, feature type.
#              Dictionary two is of column two, feature.
#              Dictionary three is column one and two as a shared value for
#              handling the same features in different feature types.
#              All dictionaries are structured as key:value, with the key
#              representing row number and value representing the column(s).
#
#              The program then generates a list of all the exisiting, clipped
#              polygons. The program then compares the shapefile names to a
#              dictionary to generate the row number in which the feature will
#              be identified as "Present" or "Absent" within the xlsx document.
#              The program will then review the Present/Absent column for
#              'No Data' and insert "N/A" to represent that the feature was not
#              included in the analysis. Layers that may not have an exact
#              match to a feature type & feature are appended to the bottom of
#              the xlsx.
#
# Outputs:     **root\ - derived from template report location**
#              root\xxTemp(today's date) folder
#              root\xxTemp(today's date)_folder\MyTempGDB.gdb
#              root\MyReport(today's date).xlsx
#
# Dependancies: Python 2.7, ArcCatalog 10.x to view temp gdb
#               Must have 2 polygon shapefiles (1 study area, 1 for analysis)
#
# Copyright:   (c) bc.gov.ca, James Burton 2019
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# Edit History:
#
# Date:
# Author:
# Modification Notes:
#
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------