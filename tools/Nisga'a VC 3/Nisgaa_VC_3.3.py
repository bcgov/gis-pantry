#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# Name:                       Advanced Geospatial Analysis
#                           CUSTOM -- Clip -- Xlxs populate
#                                    version 3.3
#
# Author:      James Burton|Government of British Columbia
#              Geospatial Analyst: Stikine-Skeena District
#
# Created:     January 2020
#
# Introduction:The primary purpose of this tool is to determine  the absence or
#              presence of Nisga'a valued components (VC) within a submitted
#              Area of Interest (AOI). The results are then appended to the agreed
#              upon SER table, which is stored as an XLSX.
#
# Specifics:   The tool is accepts three inputs from the user within ArcMap 10.x
#              or ArcCatalog 10.x.
#              The first input is the name of the report generated through the
#              analysis. This is received as a string.
#
#              The second input is the output location for the report. This is
#              obtained as a file path. It should be noted this location will
#              also house the temporary geodatabase (GDB) generated for the
#              analysis.
#
#              The third input is the AOI's feature class
#              location. This will be located within a GDB.
#              -----------------------------------------------------------------
#
#              Upon succesful input of the required variables, the script will
#              proceed to create a temporary GDB. This GDB will be formated to
#              adhere to ESRI 10.0 format and therefor will be incompatable with
#              ArcMap/ArcCatalog <9.x. The script will then copy the SER table,
#              as an XLSX, and save it to the user specified output location
#              with the user's determined title.
#
#              Upon successful creation of the report and temporary GDB, the
#              script will then proceed by clipping the VC's to the asserted
#              territory's boundaries. These clipped layers are automatically
#              directed to be housed within the temporary GDB.
#
#              Upon completion of clipping the VC's, the script will then
#              access the attribute table of each layer, searching for the
#              specific row to populate within the SER table. If the layer is
#              present within the AOI, the corresponding layer's
#              row will be populated to include "Present". If the layer is not
#              present within the AOI the corresponding row is
#              left blank.
#
#              Once all layers which are present in the AOI have
#              have been classified as present within the report, the script
#              will then review the document and populate the empty cells with
#              the value "Absent" which correlates to the layer's absence within
#              the AOI.
#
#              Following successful completion of the Present/Absent analysis,
#              the script deletes the temporary GDB and subsequently the
#              analysis is concluded.
#
# Outputs:  1. An XLSX report, populated with the layer's absence or presence.
#           2. A temporary GDB(10.0), removed upon completion
#
# Dependancies: Python 2.7, ESRI ArcMap or ArcCatalog 10.x
#
# Copyright:   (c) gov.bc.ca
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# Edit History:
#
# Date:

# Author:
# Modification Notes:
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

## Import modules needed for analysis
import os, sys, arcpy, shutil, openpyxl
from datetime import datetime

## Set local variables, get parameters from user
##print('sys.argv[0] =', sys.argv[0])
pathname = os.path.dirname(sys.argv[0])

Orig_gdb = os.path.join(pathname+'\\Nisgaa_VC.gdb')
Report_name  = arcpy.GetParameterAsText(0)
StudyArea = arcpy.GetParameterAsText(1)
Container = arcpy.GetParameterAsText(2)
TemplateReport = os.path.join(pathname+'\\Nisgaa_VC_Template.xlsx')


## Sets date for temporary folder creation
rightnow= datetime.now()
Today= rightnow.strftime('%Y_%m_%d')

## Copy the template report from archive location
def CopyXlsx():
    global Report_out
    Report_out=os.path.join(Container, Report_name + '.xlsx')
    shutil.copy(TemplateReport, Report_out)

## Function to make temporary folder and gdb
def GetTempFolder():
    global TempContainer
    global TempGDB
    TempContainer=os.path.join(Container+ '\\Temp%s' % Today)
    if os.path.exists(TempContainer):
        shutil.rmtree(TempContainer)
        os.makedirs(TempContainer)
    else:
        os.makedirs(TempContainer)
    TempGDB = arcpy.CreateFileGDB_management(TempContainer, 'TempGDB.gdb', '10.0')

## rprtout is the report/workbook.... rprtsheet is report's/workbook's sheet,
## set to active sheet (only one). Variables are global for use later.
def OpenXl():
    global rprtout
    global rprtsheet
    rprtout = openpyxl.load_workbook(Report_out)
    rprtsheet = rprtout.active

## From the original geodatabase, the polygons are clipped to the study area and
## saved to the temporary geodatabase.
def Clip2Study():
    arcpy.env.workspace = str(Orig_gdb)
    PgFCS1 = arcpy.ListFeatureClasses('', 'polygon')
    for PgFC1 in PgFCS1:
        NewPgFC = str(str(TempGDB) + '\\'+ str(PgFC1))
        arcpy.Clip_analysis(PgFC1, StudyArea, NewPgFC + '_clip','')

## iterates over the clipped polygons. If the shapefile exists within the study
## area, the row number to populate in the xlsx will be retrieved. For polygons
## with no geometry within the study area, that layer will be skipped and
## populated later.
def AbsentPresent():
    Clip2Study()
    arcpy.env.workspace = str(TempGDB)
    PgFCS2 = arcpy.ListFeatureClasses('', 'polygon')
    for PgFC2 in PgFCS2:
        try:
            value = arcpy.da.SearchCursor(PgFC2, ('PolyType',)).next()[0]
            OpenXl()
            rprtcell= rprtsheet.cell(row=int(value), column=3)
            rprtcell.value='Present'
            rprtout.save(Report_out)
        except StopIteration:
            pass

## function to handle blank cells in present/absent column
## if cell contains no data, N/A will be populated in the cell value
def BlankCheck():

    OpenXl()
    row_count = (rprtsheet.max_row)
    i=1
    while i <= row_count:

        if rprtsheet.cell(row = i, column=3).value == None:
            rprtcell= rprtsheet.cell(row=i, column=3)
            rprtcell.value='Absent'
            rprtout.save(Report_out)
        i+=1

CopyXlsx()
GetTempFolder()
AbsentPresent()
BlankCheck()

## deletes temporary folder & geodatabase.
shutil.rmtree(TempContainer, ignore_errors=True)