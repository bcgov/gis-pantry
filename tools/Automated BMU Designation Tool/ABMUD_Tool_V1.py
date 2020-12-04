################################################################################
#####################   NEW BEETLE MANAGEMENT UNIT AUTO TOOL ###################
################################################################################
## First Release
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# Name:    Automated Invasive Beetle Management Unit Tactic Designation Tool
#
# Keywords:                      It's complicated.
#                                   version 1.1
#
# Author:      James Burton|Government of British Columbia
#              Geospatial Analyst: Skeena-Stikine District
#
# Created:     September-November 2020
#
# Introduction: The tool is designed to create a spreadsheet with the current 
# year's BMU Tactic designation. As invasive beetle management is an evolving
#  and constantly adative role within he Government, this tool should reduce 
# a week's worth of analysis usually conducted by the Invasive Beetle Manager 
# for the region. 
# Traditionally, every year beetle management tactic updates require an analysis
# of the region's BMUs to determine if new management tactics need to be applied.
# The following is a textual flow chart of the process.
#
# BMUs are unioned to the year's THLB, with any THLB factor <Null> or 0 dropped.
# The area is then calculated and added to the report.
#
# BMUs are unioned to the year's relevant FHF hazard with any record with a 
# rating less than Moderate being dropped. These unioned remaining shapes are 
# dissolved, and the total area of the hazard within the THLB is calculated.
#
# BMUs are unioned to the contractors DAOS data. Spot and Patch data must be 
# formated to be the same and placed in the containment folder. Spots greater 
# than 1 HA become spots, then are unioned to the BMU and area totals for spot 
# and patch are added to the report. A ratio is calculated. 
# 
# The roads are then clipped to the region and buffered 1km (for a 2km width). 
# These ploygons are then used to clip the infestations above to derive a total 
# of percentage of the infestation areas in proximity to the roads. Those with 
# a higher accessibility index are identified. The tool the reviews all the 
# ratios and caculates tactic recomendations based upon Luke Weyman's tactic 
# matrix, 2020. 
#
# Specifics:   Some spatial items are not processed in the script. This is due 
# to the size and/or location of the file coupled with time constraints. 
# 
# First order of business, make THLB layer.
# Using updated VRI, select all records above a hundred years old. Recommend 
# you clip VRI to region first.. dissolve the 100 year plus for a singular 
# polygon.
# Using updated THLB, select anything not null or == 0. Clipping to the region 
# helps. 
# Now clip THLB to VRI 100+ dissolved layer. 
# Union it to the BMUs in your region.
# Save this as xTHLB_AOI_100_only_BMU.shp in the container folder.
# The program adds area field and calculates HA.
# 
# Get the updated FHF Hazard. This usually comes as a provincial table and
# requires a join to the VRI spatial. Join it to your VRI clipped to region,
# or select by location against region, your choice. Select Haz_Class1 Moderate,
# High, Very High, invert selection, delete records. Union it to the BMU.
# Save it as xAOI_VRI_Haz_[fhf]_Dis_THLB_Clip_BMU.shp
#
# The BMUs were edited by hand to edit BMU names that occured twice, such 
# as Babine East in two TSAs.
# This shape is saved as xBMU.shp in the container.
# 
# Roads are the digital road atlas, clipped to region, buffered 1km unioned 
# to the BMU and saved as xRoads_1km_BMU.shp.
# 
# Don't forget to remove any FIDs == -1 after the unions.
# Don't forget to link to the templates.
#  
#
# Outputs:     IBM_out, IBS_out = BMU tactic remomendation xlsx.
#
# Dependancies: Python 2.7, ArcCatalog 10.x to view temp gdb
#               Must have above noted spatials and xlsx inputs.
#
# Copyright:   (c) bc.gov.ca, James Burton 2020
#-------------------------------------------------------------------------------
# Potential edits: 
# Solve working with VRI data issues.
# Combine output xlsx docs.
# add more fields to report?
#-------------------------------------------------------------------------------
# Edit History:
#
# Date: 
# Author: 
#
# Date:
# Author:
# Modification Notes:
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#------------------ Import Libraries -------------------------#

import os, sys, arcpy, shutil, openpyxl
from datetime import datetime

#------------------ Start program timer -------------------------#

## set date/time
rightnow= datetime.now()
Today= rightnow.strftime('%Y_%m_%d')

## starts program timer
t0= time.clock()

#------------------ Set Variables= -------------------------#

## Set path name vairables, pull the necessary data.

RawData = r'W:\FOR\RNI\DSS\General_User_Data\users\jamburto\GIS Stuff\DAOS_Clean'
IBMTemplate = os.path.join(RawData+'\\IBM_Template.xlsx')
IBSTemplate = os.path.join(RawData+'\\IBS_Template.xlsx')
xBMU = os.path.join(RawData+'\\xBMU.shp')
xRoads = os.path.join(RawData+'\\xSkeena_Roads_1km_BMU.shp')
xSpruce= os.path.join(RawData+'\\xSkeena_Spruce_60_BMU.shp')
xPine= os.path.join(RawData+'\\xSkeena_Pine_60_BMU.shp')

## set the spreadsheet template, identify first row, set column values

real_row = 3
TSA_col =1
BMU_col=2
A_col=3
THLB_col=4
Ratio1_col = 5
Ratio1_text_col=6
Rd_col=7
Index_col=8
Spot_col=9
Patch_col=10
Ratio2_col=11
Ratio2_text_col=12
Tactic_col=13
OverRide=14

## for road analysis
AllPoints = 'AllPoints'
#------------------ Set Up  -------------------------#

def SetUp():
    ## set variables
    global TempContainer
    global TempGDB
    global outWorkspace
    global IBM_Report_out
    global IBS_Report_out
    global IBMrprtcell
    global IBSrprtcell

    ## Sets the temporary container to be located in the raw data folder under the name Temp_[Today's date]
    TempContainer=os.path.join(RawData+ '\\Temp%s' % Today)

    ## Program checks if the Temp folder exists already
    if os.path.exists(TempContainer):

        ## If temp folder exists, remove the existing one and make a new one. This happens during script construction and should not normally
        ## be a problem if you run the tool once a day
        ## Script will fail at this point if temp gdb timestamps are still active. No solution to that.
        shutil.rmtree(TempContainer)
        os.makedirs(TempContainer)

    else:
        ## Normal function is to make the temp folder
        os.makedirs(TempContainer)

    ## Creates a temporary GDB in the temp folder.
    TempGDB = arcpy.CreateFileGDB_management(TempContainer, 'TempGDB.gdb', '10.0')

    ## Creates a vairable for quick programming to access the new temp gdb for arcpy env workspace
    outWorkspace = str(TempGDB)

    IBM_Report_out=os.path.join(TempContainer, 'IBM_out.xlsx')
    IBS_Report_out=os.path.join(TempContainer,'IBS_out.xlsx' )

    ## copy template report and save template as FHF report out
    shutil.copy(IBMTemplate, IBM_Report_out)
    shutil.copy(IBSTemplate, IBS_Report_out)


###################################################################
#------------------ XLSX Quick Functions -------------------------#
###################################################################

## Open xlsx reports specific to FHF
def OpenXlIBM():

    ## identify global variables for IBM report
    global IBMrprtout
    global IBMrprtsheet

    ## set the variables
    IBMrprtout = openpyxl.load_workbook(IBM_Report_out)
    IBMrprtsheet = IBMrprtout.active

## Open xlsx reports specific to FHF
def OpenXlIBS():

    ## identify global variables for IBS report
    global IBSrprtout
    global IBSrprtsheet

    ## set the variables
    IBSrprtout = openpyxl.load_workbook(IBS_Report_out)
    IBSrprtsheet = IBSrprtout.active

#------------------------------------------------------------------------------#

## quick function to populate given row/column for IBM report
def IBM_RPRT_Val(val,realrow,col):
    OpenXlIBM()
    IBMrprtcell=IBMrprtsheet.cell(row=realrow,column=col)
    IBMrprtcell.value=val
    IBMrprtout.save(IBM_Report_out)

## quick function to populate given row/column for IBS report
def IBS_RPRT_Val(val,realrow,col):
    OpenXlIBS()
    IBSrprtcell=IBSrprtsheet.cell(row=realrow,column=col)
    IBSrprtcell.value=val
    IBSrprtout.save(IBS_Report_out)

#------------------------------------------------------------------------------#

## populates zero's in IBM report. Was designed to run after math complete but plans changed.
def IBM_zero_hero(col):

    ## printing action text for debugging.
    #print " ---- adding some zero's to IBM report ---- "

    ## open IBM report
    OpenXlIBM()

    ## count rows in IBM report based
    row_count = (IBMrprtsheet.max_row)

    ## sets row at three which is one row under header.
    r=3

    ## while row counter is less than total rows
    while r <= row_count:

        ## if the cell is null, add a zero to specified row and column, save report, add one more to row counter and repeat
        if IBMrprtsheet.cell(row = r, column=col).value == None:
            IBMrprtcell= IBMrprtsheet.cell(row=r, column=col)
            IBMrprtcell.value=0
            IBMrprtout.save(IBM_Report_out)
        r+=1

## populates zero's in IBS report. was designed to run after math complete but plans changed.
def IBS_zero_hero(col):

    ## printing action text for debugging.
    #print " ---- adding some zero's to IBS report ---- "

    ## open IBS report
    OpenXlIBS()

    ## count rows in IBS report based on BMU rows length
    row_count = (IBSrprtsheet.max_row)

    ## set row counter to three which is under header
    r=3

    ## while row counter is less than or equal to total rows
    while r <= row_count:

        ## if cell is null, ada a zero to specifed row and column, save report and repeat
        if IBSrprtsheet.cell(row = r, column=col).value == None:
            IBSrprtcell= IBSrprtsheet.cell(row=r, column=col)
            IBSrprtcell.value=0
            IBSrprtout.save(IBS_Report_out)
        r+=1

#------------------------------------------------------------------------------#

def addmeM(realrow,col):
    global CumuSum
    OpenXlIBM()
    IBMrprtcell= IBMrprtsheet.cell(row=realrow, column=col)
    CumuSum1=IBMrprtcell.internal_value
    CumuSum = int(CumuSum1)
    IBMrprtout.save(IBM_Report_out)
def addmeS(realrow,col):
    global CumuSum
    IBSrprtcell= IBSrprtsheet.cell(row=realrow, column=col)
    CumuSum1=IBSrprtcell.internal_value
    CumuSum = int(CumuSum1)
    IBSrprtout.save(IBS_Report_out)
#------------------ throw down some zeros -------------------------#

def ZeroValues():
        ## set all zeros in numeric fields.
    IBM_zero_hero(A_col)
    IBM_zero_hero(THLB_col)
    IBM_zero_hero(Ratio1_col)
    IBM_zero_hero(Rd_col)
    IBM_zero_hero(Spot_col)
    IBM_zero_hero(Patch_col)
    IBM_zero_hero(Ratio2_col)
    IBS_zero_hero(A_col)
    IBS_zero_hero(THLB_col)
    IBS_zero_hero(Ratio1_col)
    IBS_zero_hero(Rd_col)
    IBS_zero_hero(Spot_col)
    IBS_zero_hero(Patch_col)
    IBS_zero_hero(Ratio2_col)


#------------------ Report Ratio's -------------------------#

def IBM_Spot_Patch_Ratio(col1,col2,ratio_col,text_col):
    OpenXlIBM()
    row_count = (IBMrprtsheet.max_row)
    r=3
    while r <= row_count:
        IBMrprtcell= IBMrprtsheet.cell(row=r, column=col1)
        spotNUM=IBMrprtcell.internal_value
        IBMrprtcell= IBMrprtsheet.cell(row=r, column=col2)
        patchNUM=IBMrprtcell.internal_value
        if patchNUM == 0 and spotNUM ==0:
            IBMrprtcell= IBMrprtsheet.cell(row=r, column=text_col)
            IBMrprtcell.value='Null'
            r+=1
        elif spotNUM == 0:
            IBMrprtcell= IBMrprtsheet.cell(row=r, column=text_col)
            IBMrprtcell.value='Low'
            r+=1
        elif patchNUM ==0 and spotNUM >0:
            IBMrprtcell= IBMrprtsheet.cell(row=r, column=text_col)
            IBMrprtcell.value='High'
            IBMrprtcell= IBMrprtsheet.cell(row=r, column=ratio_col)
            IBMrprtcell.value=1
            r+=1
        else:
            ratioNUM=round(spotNUM/patchNUM,2)
            IBMrprtcell= IBMrprtsheet.cell(row=r, column=ratio_col)
            IBMrprtcell.value=ratioNUM
            IBMrprtout.save(IBM_Report_out)
            if ratioNUM <= 0.25:
                IBMrprtcell= IBMrprtsheet.cell(row=r, column=text_col)
                IBMrprtcell.value='Low'
            elif ratioNUM > 0.25 and ratioNUM <= 1:
                IBMrprtcell= IBMrprtsheet.cell(row=r, column=text_col)
                IBMrprtcell.value='Moderate'
            else:
                IBMrprtcell= IBMrprtsheet.cell(row=r, column=text_col)
                IBMrprtcell.value='High'

            r+=1
    IBMrprtout.save(IBM_Report_out)

def IBS_Spot_Patch_Ratio(col1,col2,ratio_col,text_col):
    OpenXlIBS()
    row_count = (IBSrprtsheet.max_row)
    r=3
    while r <= row_count:
        IBSrprtcell= IBSrprtsheet.cell(row=r, column=col1)
        spotNUM=IBSrprtcell.internal_value
        IBSrprtcell= IBSrprtsheet.cell(row=r, column=col2)
        patchNUM=IBSrprtcell.internal_value

        if patchNUM == 0 and spotNUM ==0:
            IBSrprtcell= IBSrprtsheet.cell(row=r, column=text_col)
            IBSrprtcell.value='Null'
            r+=1
        elif spotNUM ==0:
            IBSrprtcell= IBSrprtsheet.cell(row=r, column=text_col)
            IBSrprtcell.value='Low'
            r+=1
        elif patchNUM ==0 and spotNUM >0:
            IBSrprtcell= IBSrprtsheet.cell(row=r, column=text_col)
            IBSrprtcell.value='High'
            IBSrprtcell= IBSrprtsheet.cell(row=r, column=ratio_col)
            IBSrprtcell.value=1
            r+=1
        else:
            ratioNUM=round(spotNUM/patchNUM,2)
            IBSrprtcell= IBSrprtsheet.cell(row=r, column=ratio_col)
            IBSrprtcell.value=ratioNUM
            IBSrprtout.save(IBS_Report_out)
            if ratioNUM <= .25:
                IBSrprtcell= IBSrprtsheet.cell(row=r, column=text_col)
                IBSrprtcell.value='Low'
            elif ratioNUM > 0.25 and ratioNUM <= 1:
                IBSrprtcell= IBSrprtsheet.cell(row=r, column=text_col)
                IBSrprtcell.value='Moderate'
            else:
                IBSrprtcell= IBSrprtsheet.cell(row=r, column=text_col)
                IBSrprtcell.value='High'
            r+=1
    IBSrprtout.save(IBS_Report_out)


def ABPercent():
    print"doing AB percent"
    OpenXlIBM()
    row_count = (IBMrprtsheet.max_row)
    r = real_row
    while r <= row_count:
        realrow=r

        IBMrprtcell= IBMrprtsheet.cell(row=realrow, column=A_col)
        A_Total=IBMrprtcell.internal_value

        IBMrprtcell= IBMrprtsheet.cell(row=realrow, column=THLB_col)
        B_Total=IBMrprtcell.internal_value

        if B_Total==0:
            IBM_RPRT_Val('Null',realrow,Ratio1_text_col)

        elif A_Total==0:
            IBM_RPRT_Val('No Area',realrow,Ratio1_text_col)

        else:
            AB_ratio=round(A_Total/B_Total*100,2)
            if AB_ratio<2:
                IBM_RPRT_Val('Poor',realrow,Ratio1_text_col)
                IBM_RPRT_Val(AB_ratio,realrow,Ratio1_col)

            elif ABPercent >=2 and AB_ratio <4:
                IBM_RPRT_Val('Moderate',realrow,Ratio1_text_col)
                IBM_RPRT_Val(AB_ratio,realrow,Ratio1_col)

            else:
                IBM_RPRT_Val('High',realrow,Ratio1_text_col)
                IBM_RPRT_Val(AB_ratio,realrow,Ratio1_col)
        r+=1
    OpenXlIBS()
    row_count = (IBSrprtsheet.max_row)
    r = real_row
    while r <= row_count:
        realrow=r

        IBSrprtcell= IBSrprtsheet.cell(row=realrow, column=A_col)
        A_Total=IBSrprtcell.internal_value

        IBSrprtcell= IBSrprtsheet.cell(row=realrow, column=THLB_col)
        B_Total=IBSrprtcell.internal_value


        if B_Total==0:
            IBS_RPRT_Val('Null',realrow,Ratio1_text_col)

        elif A_Total==0:
            IBS_RPRT_Val('No Area',realrow,Ratio1_text_col)

        else:
            AB_ratio=round(A_Total/B_Total*100,2)
            if AB_ratio<2:
                IBS_RPRT_Val('Poor',realrow,Ratio1_text_col)
                IBS_RPRT_Val(AB_ratio,realrow,Ratio1_col)

            elif ABPercent >=2 and AB_ratio <4:
                IBS_RPRT_Val('Moderate',realrow,Ratio1_text_col)
                IBS_RPRT_Val(AB_ratio,realrow,Ratio1_col)

            else:
                IBS_RPRT_Val('High',realrow,Ratio1_text_col)
                IBS_RPRT_Val(AB_ratio,realrow,Ratio1_col)
        r+=1


def RoadPercent():
    print"doing road percent"
    OpenXlIBM()
    row_count = (IBMrprtsheet.max_row)
    r = real_row
    while r <= row_count:
        realrow=r

        IBMrprtcell= IBMrprtsheet.cell(row=realrow, column=Spot_col)
        spotTotal=IBMrprtcell.internal_value

        IBMrprtcell= IBMrprtsheet.cell(row=realrow, column=Patch_col)
        patchTotal=IBMrprtcell.internal_value

        IBMrprtcell=IBMrprtsheet.cell(row=realrow,column=Rd_col)
        roadTotal=IBMrprtcell.internal_value

        infestTotal=spotTotal+patchTotal
        if infestTotal==0:
            IBM_RPRT_Val('Null',realrow,Index_col)
        elif roadTotal==0:
            IBM_RPRT_Val('No Area',realrow,Index_col)
        else:
            roadPercent=round(roadTotal/infestTotal*100,2)
            if roadPercent<50:
                IBM_RPRT_Val('Poor',realrow,Index_col)
                IBM_RPRT_Val(roadPercent,realrow,Rd_col)
            elif roadPercent >=50 and roadPercent <80:
                IBM_RPRT_Val('Moderate',realrow,Index_col)
                IBM_RPRT_Val(roadPercent,realrow,Rd_col)
            else:
                IBM_RPRT_Val('High',realrow,Index_col)
                IBM_RPRT_Val(roadPercent,realrow,Rd_col)
        r+=1
    OpenXlIBS()
    row_count = (IBSrprtsheet.max_row)
    r = real_row
    while r <= row_count:
        realrow=r
        IBSrprtcell= IBSrprtsheet.cell(row=realrow, column=Spot_col)
        spotTotal=IBSrprtcell.internal_value
        IBSrprtcell= IBSrprtsheet.cell(row=realrow, column=Patch_col)
        patchTotal=IBSrprtcell.internal_value
        IBSrprtcell=IBSrprtsheet.cell(row=realrow,column=Rd_col)
        roadTotal=IBSrprtcell.internal_value
        infestTotal=spotTotal+patchTotal
        if infestTotal==0:
            IBS_RPRT_Val('Null',realrow,Index_col)
        elif roadTotal==0:
            IBS_RPRT_Val('No Area',realrow,Index_col)
        else:
            roadPercent=round(roadTotal/infestTotal*100,2)
            if roadPercent<50:
                IBS_RPRT_Val('Poor',realrow,Index_col)
                IBS_RPRT_Val(roadPercent,realrow,Rd_col)
            elif roadPercent >=50 and roadPercent <80:
                IBS_RPRT_Val('Moderate',realrow,Index_col)
                IBS_RPRT_Val(roadPercent,realrow,Rd_col)
            else:
                IBS_RPRT_Val('High',realrow,Index_col)
                IBS_RPRT_Val(roadPercent,realrow,Rd_col)
        r+=1

#------------------ Get BMU Data -------------------------#

def BaseData():

    ## selected region will be referred to as Area Of Interest(AOI) for geoprocessing purposes. This will be a global variable to be called
    ## in following functions.

    ## set variables, some local some global
    global AOI
    global xBMU_sel
    xBMU_FC = os.path.join(outWorkspace, 'xBMU')
    xBMU_LYR = 'xBMU_lyr'
    region = 'Skeena'
    AOI='xAOI'
    xBMU_sel='xBMU_selection'

    global BMU_list

    ## set variables
    BMU_list =[]

    ## Set SQL expression
    SQL=str(" REG_NAME = '"+region+"'")

    ## Set workspace to raw data
    arcpy.env.workspace=str(RawData)

    ## Copy raw BMU to temp
    arcpy.CopyFeatures_management(xBMU, xBMU_FC)

    ## set workspace to our temporary GDB
    arcpy.env.workspace=str(TempGDB)

    ## Copy our BMU FC to a layer
    arcpy.MakeFeatureLayer_management(xBMU_FC,xBMU_LYR)

    ## from out BMU layer, select the region using SQL expression from above
    arcpy.SelectLayerByAttribute_management(xBMU_LYR,'NEW_SELECTION', SQL)

    ## copy the layer and save it as BMU selection FC
    arcpy.CopyFeatures_management(xBMU_LYR, xBMU_sel)

    ## delete first BMU FC to save space
    arcpy.Delete_management(xBMU_FC)

    ## dissolve the BMU selection to create an Area of Interest shape. Arcpy dissolve doesn't work the same as interactive dissolve FYI.
    arcpy.Dissolve_management(xBMU_sel,AOI)

    ## set first row for report population porpuses
    real_row=3

    ## set column for report population
    col=1

    ## find TSA names from BMU selection FC
    with arcpy.da.SearchCursor(xBMU_sel, 'TSA_NAME') as cursor:
            for row in cursor:
                realrow=real_row
                ## get cursor value, ensured as a string, for report population
                field_value=str(cursor)

                ## drop first characters of cursor string, plop into temp variable
                field_val_temp = field_value.strip("(u'")

                ## drop last characters of cursor string, back into original cursor vairable.
                field_value= field_val_temp.strip("'),")

                ## open IBM report
                OpenXlIBM()

                IBM_RPRT_Val(field_value,realrow,col)

                ## open IBS report
                OpenXlIBS()

                IBS_RPRT_Val(field_value,realrow,col)

                ## add 1 to row iterator which will then add the next value to the right cell
                real_row+=1

    ## reset row counter
    real_row=3

    ## reset column value
    col=2

    ## print action for debugging
    #print " ---- adding BMU's to IBM & IBS report ---- "

    ## find BMU names in BMU selection FC
    with arcpy.da.SearchCursor(xBMU_sel, 'BMU_NAME') as cursor:
            for row in cursor:
                realrow=real_row
                ## get cursor value, ensured as a string, for report population
                field_value=str(cursor)

                ## drop first characters of cursor string, plop into temp variable
                field_val_temp = field_value.strip("(u'")

                ## drop last characters of cursor string, back into original cursor vairable.
                field_value= field_val_temp.strip("'),")

                ## add stripped BMU value to BMU list
                BMU_list.append(field_value)

                ## open IBM report
                OpenXlIBM()

                ## populate the BMU name to appropriate report's row and column
                IBM_RPRT_Val(field_value,realrow,col)

                ## open IBM report
                OpenXlIBS()

                ## populate the BMU name to appropriate report's row and column
                IBS_RPRT_Val(field_value,realrow,col)

                ## add 1 to row iterator which will then add the next value to the right cell
                real_row+=1

    ZeroValues()

#------------------ Get Report Data -------------------------#

def GetReportData():
    ## print report data gathering propmt for de-bugging purposes
    print 'Prepping raw data ---------------------------------------------------'

    ## set global variables
    global Raw_Poly_List
    global Raw_Point_List
    global WorkingPoint
    global WorkingPoly
    global year

    ## set workspace to raw data folder
    arcpy.env.workspace = str(RawData)

    ## create list of all raw point and and poly DAOS data
    Raw_Poly_List = arcpy.ListFeatureClasses('','polygon')
    Raw_Point_List = arcpy.ListFeatureClasses('','point')

    ## my limited experience created variables of list lengths
    Point_List_Len = len(Raw_Point_List)
    Poly_List_Len = len(Raw_Poly_List)

    ## removes 1 from point list length sum to match with actual list value if you don't get it stop reading the script..
    Feature_list_sum = int(Point_List_Len)-1

    ## sets workspace to our temp GDB
    outWorkspace = str(TempGDB)

    ## Sets the DAOS feature counter
    DAOS_Counter=0

    ## iterates over polygon features to find last polygon and point SHPs in raw data for report analysis
    for PgSHP in Raw_Poly_List:

        ## if the polygon SHP starts with prefix 'x', skip it and do not count towards DAOS counter
        if PgSHP.startswith('x'):
            ## prints prompt for user to understand the SHP was skipped
            print 'Passing '+ PgSHP+', not counted towards the DAOS Counter'

        ## Probably redundant in final script, BMU script version one needed to skip this due to topo errors
        elif PgSHP == 'DAOS_Poly_2016.shp':
            print 'Not Clipping DAOS Poly 2016 but adding 1 to the DAOS Poly Counter'
            DAOS_Counter+=1

        ## this is the magic part. If DAOS counter equals the feature list sum we gonna do some work!
        elif DAOS_Counter == Feature_list_sum:

            ## back to our raw data folder
            arcpy.env.workspace = str(RawData)

            ## creating a year variable
            year = str(2014+DAOS_Counter)

            ## create our temp feature variables for Point and Poly
            TempPoint =os.path.join(outWorkspace,str('Temp_Point_'+year))
            TempPoly = os.path.join(outWorkspace,str('Temp_Poly_'+year))

            ## create our working point and poly feature
            WorkingPoint =os.path.join(outWorkspace, Raw_Point_List[DAOS_Counter].strip(".shp"))
            WorkingPoly = os.path.join(outWorkspace, PgSHP.strip(".shp"))

            ## copy raw SHP to temp GDB as temp feature
            arcpy.CopyFeatures_management(PgSHP, TempPoly)
            arcpy.CopyFeatures_management(Raw_Point_List[DAOS_Counter], TempPoint)

            ## getting back into our temp GDB
            arcpy.env.workspace = str(TempGDB)

            ## clip temp point and poly to AOI to creating working point/poly feature
            arcpy.Clip_analysis(TempPoint,AOI,WorkingPoint)
            arcpy.Clip_analysis(TempPoly,AOI,WorkingPoly)

            ## delete the temp point poly feature class to save room
            arcpy.Delete_management(TempPoint)
            arcpy.Delete_management(TempPoly)

            ## parse the working poly feature to remove irrelevant FHF types
            with arcpy.da.UpdateCursor(WorkingPoly, "FHF") as cursor:
                for row in cursor:
                    if row[0] != 'IBM' and row[0] != 'IBS':
                        cursor.deleteRow()

            ## parse the working point feature to remove irreleevant FHF types
            with arcpy.da.UpdateCursor(WorkingPoint, "FHF") as cursor:
                for row in cursor:
                    if row[0] != 'IBM' and row[0] != 'IBS':
                        cursor.deleteRow()
            ## add one more to Daos Counter for no reason..........
            DAOS_Counter+=1

        ## if DAOS counter and point list sum actual do no match, repeat the loop and add 1 to counter
        else :
            DAOS_Counter+= 1

#------------------ Spot Patch Magiv -------------------------#

def Spot_Patch_Magic():
    ## print action promtp for debugging
    print "Starting Spot/Patch Magic!!!!--------------------------------------------------------------------------"

    ## ensure we are working in the right place!
    arcpy.env.workspace = str(TempGDB)

    ## gonna need some variables
    buffered_points = 'Buffered_Points'
    buffd_dissd_points = 'Buffered_Dissolved_Points'
    pnt_lyr = 'Working_Point_Layer'
    inExplosion = 'buff_points_99'
    outExplosion = 'buff_points_100'
    ScrubbedPoints = ('DAOS_Points_clean_'+year)
    ScrubbedTempPoly = ('DAOS_Poly_almost_clean_'+year)
    ScrubbedPoly = ('DAOS_Poly_clean_'+year)
    outPolyBMU_union = 'DAOS_PolyBMU'
    outPointBMU_union = 'DAOS_PointBMU'
    outPolyBMU_sum = "DAOS_Poly_BMU_area_sum"
    outPointBMU_sum = 'DAOS_Point_BMU_area_sum'


    ## Add field for first portion of Buffer Factor, Calculate Buffer Factor Trees x 2 (meters)
    arcpy.AddField_management (WorkingPoint, 'Buff_Factor', "TEXT",5)
    arcpy.CalculateField_management (WorkingPoint, 'Buff_Factor', "!NUM_TREES!*2", 'PYTHON')

    ## Add field for second portion of Buffer Factor so Buffer Field is a string, calculate Buffer Factor Field
    arcpy.AddField_management (WorkingPoint, 'Buffer_Field', "TEXT")
    arcpy.CalculateField_management (WorkingPoint, 'Buffer_Field', "!Buff_Factor!+' meters'", 'PYTHON')

    ## Implement Buffer using calculated buffer factor
    arcpy.Buffer_analysis (WorkingPoint, buffered_points, 'Buffer_Field', "FULL", '', "NONE", '','')

    ## Dissolve buffered points to alleviate overlapping areas, maintain beetle type and year
    arcpy.Dissolve_management(buffered_points,buffd_dissd_points,["FHF","YEAR"])

    ## Delete buffered points
    arcpy.Delete_management(buffered_points)

    ## Add field for Area of buffered points
    arcpy.AddField_management (buffd_dissd_points, 'Area_HA', "FLOAT")

    ## Explode dissolved shapes to create independent areas
    arcpy.MultipartToSinglepart_management (buffd_dissd_points, outExplosion)

    ## Delete dissolved buffer FC
    arcpy.Delete_management(buffd_dissd_points)

    ## Calculate the area of stand alone buffered FC points
    arcpy.CalculateField_management(outExplosion,"Area_HA","!shape.area@hectares!","PYTHON","#")

    ## duplicate the bufffered points
    arcpy.CopyFeatures_management(outExplosion, inExplosion)

    ## duplicate the bufffered points
    arcpy.CopyFeatures_management(outExplosion, AllPoints)

    ## filter out points less than 1 HA
    with arcpy.da.UpdateCursor(inExplosion, "Area_HA") as cursor:
        for row in cursor:
            if row[0] >= 1:
                cursor.deleteRow()

    ## filter out points that are greater than 1 HA
    with arcpy.da.UpdateCursor(outExplosion, "Area_HA") as cursor:
        for row in cursor:
            if row[0] <= 1:
                cursor.deleteRow()

    ## Create layer of point FC for select by location process
    arcpy.MakeFeatureLayer_management(WorkingPoint, pnt_lyr)

    ## Find points that lie within buffered points' area greater than 1 HA, invert selection
    arcpy.SelectLayerByLocation_management(pnt_lyr,'intersect',outExplosion,'','NEW_SELECTION', 'INVERT')

    ## Copy selected points that are not in 1 HA for actual point count which has been dropped from the analysis
    arcpy.CopyFeatures_management(pnt_lyr, ScrubbedPoints)

    ## Delete original point layer in lieu of new scrubbbed point FC
    arcpy.Delete_management(WorkingPoint)

    ## Merge buffered points greater than 1HA to incoming clipped DAOS Poly
    arcpy.Merge_management([WorkingPoly,outExplosion],ScrubbedTempPoly)

    ## Delete the exploded buffered points greater than 1HA
    arcpy.Delete_management(outExplosion)
    ## delete working DAOS poly in favour of new combined points >1HA and DAOS poly
    arcpy.Delete_management(WorkingPoly)

    ## reset the area field to 0 for buffered poins <1HA and for new DAOS poly
    arcpy.CalculateField_management(ScrubbedTempPoly,"Area_HA",0,"PYTHON","#")
    arcpy.CalculateField_management(inExplosion,"Area_HA",0,"PYTHON","#")

    ## set the year field to current year for buffered poins <1HA and for new DAOS poly in case it was ommited from the original dataset
    arcpy.CalculateField_management(ScrubbedTempPoly,"YEAR",year,"PYTHON","#")
    arcpy.CalculateField_management(inExplosion,"YEAR",year,"PYTHON","#")

    ## Dissolve new Poly FC to avoid overlapping features being counted twice
    arcpy.Dissolve_management(ScrubbedTempPoly,ScrubbedPoly,["FHF","YEAR","Area_HA"])

    ## Delete the temp poly to save space
    arcpy.Delete_management(ScrubbedTempPoly)

    ##Join BMU names to daos poly and points
    arcpy.Union_analysis([ScrubbedPoly, xBMU_sel], outPolyBMU_union)
    arcpy.Union_analysis([inExplosion,xBMU_sel], outPointBMU_union)

    ## delete previous input data to reduce space
    arcpy.Delete_management(ScrubbedPoly)
    arcpy.Delete_management(inExplosion)

    ## Delete records based on omited year value associated with BMU
    with arcpy.da.UpdateCursor(outPolyBMU_union, "YEAR") as cursor:
        for row in cursor:
            if row[0] == 0:
                cursor.deleteRow()

    ## Delete records
    with arcpy.da.UpdateCursor(outPointBMU_union, "YEAR") as cursor:
        for row in cursor:
            if row[0] == 0:
                cursor.deleteRow()

    ## Calculate the area
    arcpy.CalculateField_management(outPolyBMU_union,"Area_HA","!shape.area@hectares!","PYTHON","#")

    ## dissolve BMU poly union for sum of poly area in bmu
    arcpy.Dissolve_management(outPolyBMU_union, outPolyBMU_sum, "YEAR;FHF;TSA_NAME;BMU_NAME", "Area_HA SUM", "MULTI_PART", "DISSOLVE_LINES")

    ## dissolve points in bmu for point sum area in bmu (points are the less than 1ha)
    arcpy.Dissolve_management(outPointBMU_union, outPointBMU_sum, "YEAR;FHF;TSA_NAME;BMU_NAME;Area_HA", "", "MULTI_PART", "DISSOLVE_LINES")

    ## Calculate the area
    arcpy.CalculateField_management(outPointBMU_sum,"Area_HA","!shape.area@hectares!","PYTHON","#")

    ##delete the items dissolved above to reduce space
    arcpy.Delete_management(outPolyBMU_union)
    arcpy.Delete_management(outPointBMU_union)

    ## set the real row back to 3
    real_row = 3
    ## reset the column value
    print 'starting point area things'
    ## using the point's BMU sum area, parse the table for input to report
    with arcpy.da.SearchCursor(outPointBMU_sum, ['FHF','TSA_NAME','BMU_NAME','Area_HA']) as cursor:
        for row in cursor:

            ## set the BMU name to match BMU list values.
            BMUa = str(cursor[2].strip("u"))
            FHFa =str(cursor[0].strip("u"))

            ## identify the area input value
            cumulativeSum=round(cursor[3],2)

            ## if IBM record, open IBM report and match BMU name to right row, populate report.
            if FHFa == 'IBM':
                ii=0
                while len(BMU_list)>ii:
                    if BMU_list[ii]==BMUa:
                        realrow= real_row+ii
                        addmeM(realrow,Spot_col)
                        sum13=cumulativeSum+CumuSum
                        IBM_RPRT_Val(sum13,realrow,Spot_col)
                        ii+=1
                    else:
                        ii+=1

            ## if IBS record, open IBS report and match BMU ame to right row, populate field.
            else:
                ii=0
                while len(BMU_list)>ii:
                    if BMU_list[ii]==BMUa:
                        realrow= real_row+ii
                        addmeM(realrow,Spot_col)
                        sum13=cumulativeSum+CumuSum
                        IBS_RPRT_Val(sum13,realrow,Spot_col)
                        ii+=1
                    else:
                        ii+=1

    ## reset column value
    print 'starting poly area things'
    ## using Poly BMU sum area, parse table for input values
    with arcpy.da.SearchCursor(outPolyBMU_sum, ['FHF','TSA_NAME','BMU_NAME','SUM_Area_HA']) as cursor:

        for row in cursor:
            BMUa = str(cursor[2].strip("u"))
            FHFa=str(cursor[0].strip("u"))
            cumulativeSum=round(cursor[3],2)
            if FHFa == 'IBM':
                ii=0
                while len(BMU_list)>ii:
                    if BMU_list[ii]==BMUa:
                        realrow= real_row+ii
                        addmeM(realrow,Patch_col)
                        sum13=cumulativeSum+CumuSum
                        IBM_RPRT_Val(sum13,realrow,Patch_col)
                        ii+=1
                    else:
                        ii+=1
            else:
                ii=0
                while len(BMU_list)>ii:
                    if BMU_list[ii]==BMUa:
                        realrow= real_row+ii
                        addmeM(realrow,Patch_col)
                        sum13=cumulativeSum+CumuSum
                        IBS_RPRT_Val(sum13,realrow,Patch_col)
                        ii+=1
                    else:
                        ii+=1
    print 'done area things'
    IBM_Spot_Patch_Ratio(Spot_col,Patch_col,Ratio2_col,Ratio2_text_col)
    IBS_Spot_Patch_Ratio(Spot_col,Patch_col,Ratio2_col,Ratio2_text_col)

#------------------ THLB Process -------------------------#

def xTHLB():

    xTHLB= os.path.join(RawData+'\\xTHLB_AOI_100_only_BMU.shp')
    print ' starting THLB things-------------------'
    arcpy.env.workspace=str(TempGDB)
    arcpy.CopyFeatures_management(xTHLB, 'xTHLB')
    arcpy.AddField_management ('xTHLB', 'Area_HA', "FLOAT")
    arcpy.CalculateField_management('xTHLB',"Area_HA","!shape.area@hectares!","PYTHON","#")
    with arcpy.da.SearchCursor('xTHLB', ['TSA_NAME','BMU_NAME','Area_HA']) as cursor:
        for row in cursor:
            BMUa=cursor[1]
            cumulativeSum=round(cursor[2],2)
            ii=0
            while len(BMU_list)>ii:
                                ##print 'bmu listings'
                if BMU_list[ii] == BMUa:
                        ##print 'ibm and IBS writing'
                        OpenXlIBM()
                        realrow=real_row+ii
                        IBMrprtcell=IBMrprtsheet.cell(row=realrow,column=THLB_col)
                        IBMrprtcell.value=cumulativeSum
                        IBMrprtout.save(IBM_Report_out)
                        OpenXlIBS()
                        IBSrprtcell=IBSrprtsheet.cell(row=realrow,column=THLB_col)
                        IBSrprtcell.value=cumulativeSum
                        IBSrprtout.save(IBS_Report_out)

                        ii+=1

                else:
                                    ##print 'trying to match again'
                    ii+=1

    print ' done thlb thing.'

#------------------ IBM_Haz -------------------------#

def xHaz():

    xHaz_IBM_in= os.path.join(RawData+'\\xAOI_VRI_Haz_IBM_Dis_THLB_Clip_BMU.shp')
    xHaz_IBM = os.path.join(outWorkspace+'\\xHaz_IBM')
    xHaz_IBS_in= os.path.join(RawData+'\\xAOI_VRI_Haz_IBS_Dis_THLB_Clip_BMU.shp')
    xHaz_IBS=os.path.join(outWorkspace,'xHaz_IBS')
    xHaz_IBM_BMU='xHaz_IBM_BMU'
    xHaz_IBS_BMU='xHaz_IBS_BMU'
    xHaz_IBM_dis = 'IBM_Hazard_Dissolve'

    print ' starting IBM Hazard------------------'
    arcpy.env.workspace=str(TempGDB)
    arcpy.CopyFeatures_management(xHaz_IBM_in, xHaz_IBM_BMU)
    arcpy.env.workspace=str(TempGDB)
    ##arcpy.Clip_analysis('xHaz_IBM', xTHLB_100############, 'xHaz_IBM2'
    #arcpy.Union_analysis([xHaz_IBM,xBMU_sel],xHaz_IBM_BMU)
    # Process: Union
    ##arcpy.Dissolve_management(xHaz_IBM,xHaz_IBM_dis)
    #arcpy.Union_analysis(['xHaz_IBM','xBMU_selection'], xHaz_IBM_BMU )
    arcpy.AddField_management (xHaz_IBM_BMU, 'Area_HA', "FLOAT")

##    ##arcpy.Delete_management('xHaz_IBM')
##    with arcpy.da.UpdateCursor(xHaz_IBM_BMU, ['FID_xHaz_IBM','FID_xBMU_selection']) as cursor:
##        for row in cursor:
##            if row[0] == -1 :##or row[1] ==  -1 :
##                cursor.deleteRow()

    arcpy.CalculateField_management(xHaz_IBM_BMU,"Area_HA","!shape.area@hectares!","PYTHON","#")
    with arcpy.da.SearchCursor(xHaz_IBM_BMU, ['TSA_NAME','BMU_NAME','Area_HA']) as cursor:
        for row in cursor:
            BMUa=cursor[1]
            cumulativeSum=round(cursor[2],2)
            ii=0
            while len(BMU_list)>ii:
                                ##print 'bmu listings'
                if BMU_list[ii] == BMUa:
                        ##print 'ibm and IBS writing'
                    OpenXlIBM()
                    realrow=real_row+ii
                    addmeM(realrow,A_col)
                    sum13=cumulativeSum+CumuSum
                    IBM_RPRT_Val(sum13,realrow,A_col)
                    ii+=1
                else:
                    ii+=1

    print ' starting IBS Hazard------------------'
    arcpy.CopyFeatures_management(xHaz_IBS_in, xHaz_IBS_BMU)
    ##arcpy.Clip_analysis('xHaz_IBM', xTHLB_100############, 'xHaz_IBM2'
    ##arcpy.Union_analysis(['xHaz_IBS','xBMU_selection'],xHaz_IBS_BMU)
    arcpy.AddField_management (xHaz_IBS_BMU, 'Area_HA', "FLOAT")
##
##    ##arcpy.Delete_management('xHaz_IBM')
##    with arcpy.da.UpdateCursor(xHaz_IBS_BMU, ['FID_xHaz_IBS','FID_xBMU_selection']) as cursor:
##        for row in cursor:
##            if row[0] == -1 :##or row[1] ==  -1 :
##                cursor.deleteRow()

    arcpy.CalculateField_management(xHaz_IBS_BMU,"Area_HA","!shape.area@hectares!","PYTHON","#")
    ##arcpy.Delete_management('xHaz_IBM')
    with arcpy.da.SearchCursor(xHaz_IBS_BMU, ['TSA_NAME','BMU_NAME','Area_HA']) as cursor:
        for row in cursor:
            BMUa=cursor[1]
            cumulativeSum=round(cursor[2],2)
            ii=0
            while len(BMU_list)>ii:
                                ##print 'bmu listings'
                if BMU_list[ii] == BMUa:
                        ##print 'ibm and IBS writing'
                    OpenXlIBS()
                    realrow=real_row+ii
                    addmeS(realrow,A_col)
                    sum13=cumulativeSum+CumuSum
                    IBS_RPRT_Val(sum13,realrow,A_col)
                    ii+=1
                else:
                    ii+=1

    print 'done haz pine'

def RoadIntersections():
    print ' starting pine sticks -------------'

    xRoads_FC = os.path.join(outWorkspace, 'xRoads')
    ## Set workspace to raw data
    arcpy.env.workspace=str(RawData)
    ## Copy raw BMU to temp
    arcpy.CopyFeatures_management(xRoads, xRoads_FC)
    arcpy.env.workspace=str(TempGDB)
    arcpy.Merge_management(['DAOS_Poly_BMU_area_sum','DAOS_Point_BMU_area_sum'],'DAOS_all')
    arcpy.CalculateField_management('DAOS_all',"Area_HA",0,"PYTHON","#")
    arcpy.Dissolve_management('DAOS_all','DAOS_Dissolve',["FHF","YEAR","Area_HA",'BMU_NAME'])
    #arcpy.Delete_management('DAOS_all')
    arcpy.Clip_analysis('DAOS_Dissolve',xRoads_FC,'INFEST_near_Roads')
    arcpy.CalculateField_management('INFEST_near_Roads',"Area_HA","!shape.area@hectares!","PYTHON","#")
    with arcpy.da.SearchCursor('INFEST_near_Roads', ['FHF','BMU_NAME','Area_HA']) as cursor:
        for row in cursor:
            BMUa=cursor[1]
            FC_area_value = round(cursor[2],2)
            ##cumulativeSum=float(cursor[2])
            ii=0
            while len(BMU_list)>ii:
                if BMU_list[ii] == BMUa:
                    realrow=real_row+ii
                    if cursor[0] == 'IBM':
                        addmeM(realrow,Rd_col)
                        cumulativeSum=FC_area_value+CumuSum
                        IBM_RPRT_Val(cumulativeSum,realrow,Rd_col)
                        ii+=1
                    else:
                        addmeS(realrow,Rd_col)
                        cumulativeSum=FC_area_value+CumuSum
                        IBS_RPRT_Val(cumulativeSum,realrow,Rd_col)
                        ii+=1
                else:
                    ii+=1


def FinalizeResults(a,b,c,x):
    OpenXlIBM()
    row_count = (IBMrprtsheet.max_row)
    r=3
    while r <= row_count:
        IBMrprtcell= IBMrprtsheet.cell(row=r, column=c)
        Ratio2=IBMrprtcell.internal_value
        IBMrprtcell= IBMrprtsheet.cell(row=r, column=b)
        IndexRatio=IBMrprtcell.internal_value
        IBMrprtcell= IBMrprtsheet.cell(row=r, column=a)
        Ratio1=IBMrprtcell.internal_value
        if Ratio2 == 'Null':
            IBMrprtcell= IBMrprtsheet.cell(row=r, column=x)
            IBMrprtcell.value='Monitor'
            r+=1
        else:
            if IndexRatio == 'No Area' or IndexRatio == 'Poor':
                IBMrprtcell= IBMrprtsheet.cell(row=r, column=x)
                IBMrprtcell.value='Monitor'
                r+=1
            elif Ratio2 == 'Low':
                IBMrprtcell= IBMrprtsheet.cell(row=r, column=x)
                IBMrprtcell.value='Salvage'
                r+=1
            elif Ratio2 == 'Moderate':
                IBMrprtcell= IBMrprtsheet.cell(row=r, column=x)
                IBMrprtcell.value='Holding'
                r+=1
            else:
                IBMrprtcell= IBMrprtsheet.cell(row=r, column=x)
                IBMrprtcell.value='Supression'
                r+=1
        IBMrprtout.save(IBM_Report_out)
    OpenXlIBS()
    row_count = (IBSrprtsheet.max_row)
    r=3
    while r <= row_count:
        IBSrprtcell= IBSrprtsheet.cell(row=r, column=c)
        Ratio2=IBSrprtcell.internal_value
        IBSrprtcell= IBSrprtsheet.cell(row=r, column=b)
        IndexRatio=IBSrprtcell.internal_value
        IBSrprtcell= IBSrprtsheet.cell(row=r, column=a)
        Ratio1=IBSrprtcell.internal_value
        if Ratio2 == 'Null':
            IBSrprtcell= IBSrprtsheet.cell(row=r, column=x)
            IBSrprtcell.value='Monitor'
            r+=1
        else:
            if IndexRatio == 'No Area' or IndexRatio == 'Poor':
                IBSrprtcell= IBSrprtsheet.cell(row=r, column=x)
                IBSrprtcell.value='Monitor'
                r+=1
            elif Ratio2 == 'Low':
                IBSrprtcell= IBSrprtsheet.cell(row=r, column=x)
                IBSrprtcell.value='Salvage'
                r+=1
            elif Ratio2 == 'Moderate':
                IBSrprtcell= IBSrprtsheet.cell(row=r, column=x)
                IBSrprtcell.value='Holding'
                r+=1
            else:
                IBSrprtcell= IBSrprtsheet.cell(row=r, column=x)
                IBSrprtcell.value='Supression'
                r+=1
        IBSrprtout.save(IBS_Report_out)

SetUp()
BaseData()
GetReportData()
Spot_Patch_Magic()
xTHLB()
xHaz()
RoadIntersections()
ABPercent()
RoadPercent()

FinalizeResults(6,8,12,13)


t1 = time.clock() - t0
print('Time elapsed: ', (t1 - t0)) # CPU minutes elapsed (floating point)
print 'Done :)'