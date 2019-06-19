#=========================================================================================================
# Script Name
#=========================================================================================================
# Date              : 2016-05-24
#
# Author            : Erin Philip (BCTS Okanagan - Columbia erin.n.philip@goc.bc.ca)
#
# Purpose           : This script is used to assist with Route Card Analysis, it is used in conjuction 
#                     with a created MXD in the GEO environment. It looks at the block of interest and 
#                     its spatial relationship with other layers that are outlined in the Look Up Table.
#
# Arguements        : This script must be run through the Route Card Toolbox with an open mxd.
#
#
# History           :   (2016-05-24) - Erin Philip
#                                      Created. Runs inside GEO. Use of Tags in map document to determine UBI
#
#                   :   (2017-03-29) - Erin Philip
#                                      Updated to run outside of GEO
#                                      Updated to run on roads and blocks based on a selection,
#                                      it will only allow a single feature to run through tool
# Chagnes
# - Added a road functionaility
# - Moved all scripting to single script
# - Moved out of GEO
# - Script is now run by a selection rather than GEO, no more than one feature can be run at a time.
# - Added a dynamic legend rather than specifying in the tables and script
# - Added new supporting data items to the script controls (All block or road specific inputs)
#
# June 6, 2017
# - Updated the 'Contained' module outside of the loop where it removes items based on the 'nooverlaplayers'
# - Contained Logic changed to be reverse. In the Module it automatically gives it a 'Y' until the block or road
#   is contained by something then it is given a 'N'
#
#=========================================================================================================
                 
#=========================================================================================================
#=========================================================================================================
#  Process Status and Return Codes:
#      -1   - Unexpected error
#       0   - Completed Successful Run
#       1   - In progress
#       100 - Invalid Arguments
#       101 - ESRI License Error
#
#=========================================================================================================

#*********************************************************************************************************
#  Program Initialization
#*********************************************************************************************************

#---------------------------------------------------------------------------------------------------------
#  Python and System Modules
#-----------
#  Importing all modules that will be used for the script
#---------------------------------------------------------------------------------------------------------

from __future__ import division

print '-- Importing Modules'

import sys
import string
import os
import math
import stat
import time
import collections
from collections import OrderedDict

#---------------------------------------------------------------------------------------------------------
#  Arguement Input
#-----------
#  Pull arguements from the tool parameters window. 
#---------------------------------------------------------------------------------------------------------

print '-- Getting Run Parameters'

# Python script location (automatically populated)
PYTHON_SCRIPT   = sys.argv[0]
RCTYPE = sys.argv[1]
# Post flag arguement is used to label the output with a "Final" or "Preliminary" label
POSTFLAG   = sys.argv[2]
if POSTFLAG == 'true':
    STATUS = "Final"
else:
    STATUS = "Preliminary"
OWNER = sys.argv[3]


#---------------------------------------------------------------------------------------------------------
#  Standard/Global Variables/Constants
#---------------------------------------------------------------------------------------------------------
print '-- Setting Global Variables'


START_TIME       = time.ctime(time.time())
START_TIME_SEC   = time.time()
START_TIME_SQL   = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
BEEP             = chr(7)

# Global Variables
#   The Processing_Variables is the collection of messaging and script specific information needed
#   throughout this program.  It is constantly updated, and generally includes all paths and configuration
#   information.  For parameters that are passed in to the script, they should generally be assigned
#   to a Processing_Variable through the Initialize() routine.

Processing_Variables = {}
RunStatus = {}


#---------------------------------------------------------------------------------------------------------
#  Set up the ArcGIS Geoprocessing Environment
#---------------------------------------------------------------------------------------------------------

import arcpy
from arcpy import env 

#locate the mxd to work in. (set to be the mxd that is open)
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd,'*')[0]

#Set the workspace to be in memory so no extra data is created.
arcpy.env.workspace = 'in_memory'
arcpy.env.overwriteOutput = True

#*********************************************************************************************************
#  Routines
#*********************************************************************************************************
#---------------------------------------------------------------------------------------------------------
# WriteOutputToScreen(Output_Comment, Header_Style):
#
#   Prints the Output_Comment to the screen with the appropriate formatting
#       0 : "******" Used for Error Sections
#       1 : "======" Used for the Program's Header and Footer
#       2 : "------" Used for New Sections
#       3+:          No delimitation
#   
#---------------------------------------------------------------------------------------------------------
def WriteOutputToScreen(Output_Comment, Header_Style):
    if Header_Style == 0:
        # Errors get beeps, too!
        print BEEP * 3 + "\n" * 2 + "*" * 79 + "\n" * 2
    if Header_Style == 2:
        print "\n" + "-" * 79 + "\n"
    if Header_Style == 1:
        print "\n" + "=" * 79 + "\n"
        
    #print Output_Comment
    arcpy.AddMessage(Output_Comment)
    
    if Header_Style == 0:
        print "\n" * 2 + "*" * 79 + "\n" * 2
    if Header_Style == 1:
        print "\n" + "=" * 79 + "\n"
#---------------------------------------------------------------------------------------------------------
#
#       Test if we need to do stuff, and do it if necessary.
#          Return 0 - nothing to do
#                 1 - successful
#                -1 - unknown failure
#
#---------------------------------------------------------------------------------------------------------
def Message(Message, MessageLevel):
    # Based on the logging level, add messages to the message queues.
    #   Text Run Log   : Implimented
    #   Console        : Implimented
    #   GeoProcessor   : Implimented
    #   Processing Log : Implimented (with e-mail)
    #   SQL Database   : Not Implimented ####
    #   FGDB           : Implimented
    
    #   0    : Fatal Errors
    #   1    : Top Level Program
    #   2    : Main routines and events
    #   3    : Warnings
    #   4    : General Information
    #   5    : Debug level detail


    
    # Send to the screen
    if MessageLevel <= Processing_Variables['Log_Level']:
        WriteOutputToScreen(Message, MessageLevel)    
    
    # Send to the GeoProcessor Message Queue
    #### At ArcGIS 9.3 SP1 there is a bug that also causes any GeoProcessor messages to be echoed to the console.
    #    Added the ToolBoxRun parameter to allow the script to add messages to the GeoProcessor Messaging properly
    if MessageLevel < 4 and MessageLevel <= Processing_Variables['Log_Level'] and Processing_Variables['ToolBoxRun'] == 'TRUE':
        if MessageLevel == 0:
            arcpy.AddError(Message)
        if MessageLevel == 1 or MessageLevel == 2:
            arcpy.AddMessage(Message)
        if MessageLevel == 3:
            arcpy.AddWarning(Message)

    # Send to the FGDB Processing Log
    if MessageLevel < 4 and MessageLevel <= Processing_Variables['Log_Level'] and 'Log_FGDB_Table' in Processing_Variables:
        rows = arcpy.InsertCursor(Processing_Variables['Log_FGDB_Table'])

        row = rows.NewRow()
        row.SetValue("Script_Name", PYTHON_SCRIPT)
        row.SetValue("Event_Time", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        row.SetValue("Message_Level", MessageLevel)
        row.SetValue("Message", Message)
        row.SetValue("Start_Time", START_TIME_SQL)

        rows.InsertRow(row)
        del row
        del rows
    

    return(1)
#=========================================================================================================
#  Standard Routines
#=========================================================================================================
#---------------------------------------------------------------------------------------------------------
# Initialize()
#
#       Set up all of the paths and variables that we need to run this script.
#          Return 0 - nothing to do
#                 1 - successful
#                -1 - unknown failure
#
#---------------------------------------------------------------------------------------------------------
def Initialize():
    print '    - Initializing Script'

    
    Processing_Variables['ToolBoxRun'] = 'FALSE'
    # Processing_Variables['SendRunLogToEmail'] = ['mneal@cloverpoint.com', 'chaos_mike@hotmail.com']
    Processing_Variables['Log_Level'] = 4
    Processing_Variables['PROCESS_INFO']   = "RUNNING " + PYTHON_SCRIPT
    Processing_Variables['PROCESS_STATUS'] = 1
    Processing_Variables['PROCESS_LOG'] = []

    Message('Executing: ' + PYTHON_SCRIPT, 1)
    Message('    Start Time: ' + START_TIME, 2)
    Message('    Python ' + sys.version, 4)

    Processing_Variables['Script_Directory_Path'] = os.path.split(PYTHON_SCRIPT)[0]
    Processing_Variables['Script_Name'] = os.path.split(PYTHON_SCRIPT)[1]
    Processing_Variables['Log_Directory_Path'] = Processing_Variables['Script_Directory_Path'] + r'\log'
    Processing_Variables['Project_Base_Path']      = os.path.split(Processing_Variables['Script_Directory_Path'])[0]
    Processing_Variables['Supporting_Data_Directory_Path'] = Processing_Variables['Script_Directory_Path'] + r'\Supporting Data'
    Processing_Variables['Supporting_Data_GDB'] = Processing_Variables['Supporting_Data_Directory_Path'] + r'\SupportingData.gdb'


    #-----------------------------------------------------------------------------------------------------
    #  Script Controls
    #-----------------------------------------------------------------------------------------------------
    Processing_Variables['LUT_ScriptControls'] = Processing_Variables['Supporting_Data_GDB'] + '\\LUT_ScriptControls'
    
    Processing_Variables['Variables'] = {}
    for row in arcpy.da.SearchCursor(Processing_Variables['LUT_ScriptControls'],['Script_Variable','Variable_Value']):
        Processing_Variables['Variables'][row[0]] = row[1]

       
    #-----------------------------------------------------------------------------------------------------
    #  Script Specific Variables/Constants
    #-----------------------------------------------------------------------------------------------------   
    #String Variables
    Processing_Variables['UNIQUEID'] = ''
    Processing_Variables['Status'] = STATUS
    Processing_Variables['Owner'] = OWNER
    Processing_Variables['RCTYPE'] = RCTYPE
    Processing_Variables['SearchBuffer'] = ''
    Processing_Variables['ShapeOfInterest'] = ''
    
    Processing_Variables['OpArea'] = ''
    Processing_Variables['LandscapeUnit'] = ''
    Processing_Variables['LegalLocation'] = ''
    Processing_Variables['PolygonSelection'] = ''
    Processing_Variables['UniqueIDField'] = ''
    Processing_Variables['TitleFields'] = ''

    #Path Variables
    Processing_Variables['ProcessingLookupTable'] = Processing_Variables['Supporting_Data_GDB'] + '\\LUT_Processing'
    Processing_Variables['LegendLookupTable'] = Processing_Variables['Supporting_Data_GDB'] + '\\LUT_Legend'
    Processing_Variables['LegalArea'] = Processing_Variables['Supporting_Data_GDB'] + '\\LegalAreas'
    
    Processing_Variables['OutputLocation'] = Processing_Variables['Variables']['OutputLocation']

    #Lists
    Processing_Variables['ShapeArea'] = []
    Processing_Variables['SearchBufferArea'] = []
    Processing_Variables['ExistingBEC'] = []
    Processing_Variables['whacodes'] = []
    Processing_Variables['ungulatecodes'] = []
    Processing_Variables['bands'] = []
    Processing_Variables['NoOverlap'] = []
    Processing_Variables['LayerList'] = []

    #Dictionaries
    Processing_Variables['Applicable'] = {}
    Processing_Variables['SelectionLayers'] = {}
    Processing_Variables['AttributeInformation'] = {}
    Processing_Variables['CannedStatement'] = {}
    Processing_Variables['layerdict'] = {}
    Processing_Variables['Title']  = {}

    return(1)
#---------------------------------------------------------------------------------------------------------
# Reset MXD()
#
#       Test if we need to create the workspace file geodatabases, and then do it if necessary.
#          Return 0 - nothing to do
#                 1 - successful
#                -1 - unknown failure
#
#---------------------------------------------------------------------------------------------------------
def ResetMXD():
    Processing_Variables['PROCESS_STATUS'] = 0
    Processing_Variables['PROCESS_INFO']  = "Reset MXD"  
    Message('    - Reset MXD', 2)

    for layer in arcpy.mapping.ListLayers(mxd,):
        if layer.name in ["ShapeOfInterest","SearchBuffer","Road of Interest","Block of Interest"]:
            arcpy.mapping.RemoveLayer(df, layer) 
        if "Meter Search Buffer" in layer.name:
            arcpy.mapping.RemoveLayer(df, layer) 

    return(Processing_Variables['PROCESS_STATUS'])
#---------------------------------------------------------------------------------------------------------
# SelectBlocks()
#
#       Test if we need to create the workspace file geodatabases, and then do it if necessary.
#          Return 0 - nothing to do
#                 1 - successful
#                -1 - unknown failure
#
#---------------------------------------------------------------------------------------------------------
def SelectBlocks():
    Processing_Variables['PROCESS_STATUS'] = 0
    Processing_Variables['PROCESS_INFO']   = "SelectBlocks"  

    Message('    - Selecting Blocks', 2)

    desc = arcpy.Describe(Processing_Variables['Variables']['InputBlockFeatureClass'])
    if len(desc.FIDSet.split(';')) > 1:
        Message("   - Error with Blocks Selection - Stopping Tool",0)
        sys.exit(100)
    elif str(desc.FIDSet) == "" :
        Message("   - No Block Selected - Stopping Tool",0)
        sys.exit(100)

    arcpy.Select_analysis(Processing_Variables['Variables']['InputBlockFeatureClass'],r'in_memory\ShapeOfInterest')

    Processing_Variables['ShapeOfInterest'] = r'in_memory\ShapeOfInterest'
    Processing_Variables['UniqueIDField'] = Processing_Variables['Variables']['InputBlockField']

    cursorfieldlist = Processing_Variables['Variables']['InputBlockTitleFields'].split(',')
    for row in arcpy.da.SearchCursor(Processing_Variables['ShapeOfInterest'],cursorfieldlist):
        for item in cursorfieldlist:
            Processing_Variables['Title'][item] = row[cursorfieldlist.index(item)]

    Processing_Variables['TitleFields'] = Processing_Variables['Variables']['InputBlockTitleFields']
    
    return(Processing_Variables['PROCESS_STATUS'])
#---------------------------------------------------------------------------------------------------------
# SelectRoads()
#
#       Test if we need to create the workspace file geodatabases, and then do it if necessary.
#          Return 0 - nothing to do
#                 1 - successful
#                -1 - unknown failure
#
#---------------------------------------------------------------------------------------------------------
def SetupRoads():
    Processing_Variables['PROCESS_STATUS'] = 0
    Processing_Variables['PROCESS_INFO']   = "Select Roads"  

    Message('    - Selecting Roads', 2)
    
    desc = arcpy.Describe(Processing_Variables['Variables']['InputRoadFeatureClass'])
    if len(desc.FIDSet.split(';')) > 1:
        Message("   - Error with Roads Selection - Stopping Tool",0)
        sys.exit(100)
    elif str(desc.FIDSet) == "" :
        Message("   - No Road Selected - Stopping Tool",0)
        sys.exit(100)
    #Create a feature class of selected road feature
    arcpy.CopyFeatures_management(Processing_Variables['Variables']['InputRoadFeatureClass'],r'in_memory\RoadSelect')

    #buffer all roads into 
    arcpy.Buffer_analysis(r'in_memory\RoadSelect',r"in_memory\ShapeOfInterest",'10 Meters',dissolve_option = 'ALL')

    Processing_Variables['ShapeOfInterest'] = r'in_memory\ShapeOfInterest'          
    Processing_Variables['UniqueIDField'] = Processing_Variables['Variables']['InputRoadField']


    cursorfieldlist = Processing_Variables['Variables']['InputRoadTitleFields'].split(',')   
    for row in arcpy.da.SearchCursor(r'in_memory\RoadSelect',cursorfieldlist):
        for item in cursorfieldlist:
            Processing_Variables['Title'][item] = row[cursorfieldlist.index(item)]

    Processing_Variables['TitleFields'] = Processing_Variables['Variables']['InputRoadTitleFields']

    return(Processing_Variables['PROCESS_STATUS'])
#---------------------------------------------------------------------------------------------------------
# PrepMXD()
#
#       Test if we need to create the workspace file geodatabases, and then do it if necessary.
#          Return 0 - nothing to do
#                 1 - successful
#                -1 - unknown failure
#
#---------------------------------------------------------------------------------------------------------
def PrepMXD():
    Processing_Variables['PROCESS_STATUS'] = 0
    Processing_Variables['PROCESS_INFO']   = "Prepping MXD"  

    Message('    - Prepping MXD', 2)

    #Create the Search Buffer, add to map and apply symbology from a premade lyr file.
    BufferDistance = Processing_Variables['Variables']['SearchBufferDistance'] + ' Meters'
    arcpy.Buffer_analysis(r'in_memory\ShapeOfInterest',r"in_memory\SearchBuffer",BufferDistance)
    Processing_Variables['SearchBuffer'] = r"in_memory\SearchBuffer"
   
    addbuffer = arcpy.mapping.Layer(Processing_Variables['SearchBuffer'])
    arcpy.mapping.AddLayer(df, addbuffer)
    arcpy.ApplySymbologyFromLayer_management("SearchBuffer", Processing_Variables['Supporting_Data_Directory_Path'] + r'\SearchBuffer.lyr')

    addlayer = arcpy.mapping.Layer(Processing_Variables['ShapeOfInterest'])
    arcpy.mapping.AddLayer(df, addlayer)
    arcpy.ApplySymbologyFromLayer_management("ShapeOfInterest",Processing_Variables['Supporting_Data_Directory_Path'] + r'\ShapeOfInterest.lyr')

    # Grab the spatial shapes from the Search Buffer and Shape of Interest for future analysis
    with arcpy.da.SearchCursor(Processing_Variables['ShapeOfInterest'],["SHAPE@"]) as cursor:
        for row in cursor:
            Processing_Variables['ShapeArea'].append(row[0])

    with arcpy.da.SearchCursor(Processing_Variables['SearchBuffer'],["SHAPE@"]) as cursor:
        for row in cursor:
            Processing_Variables['SearchBufferArea'].append(row[0])

    #Turn off all layers except the UBI of interest Layer
    for layer in arcpy.mapping.ListLayers(mxd):
        if layer.name in ["ShapeOfInterest",'SearchBufferDistance']:
            pass
        else:
            layer.visible = False

    #Set the extent in which you set the Processing Extent
    ext = addbuffer.getExtent()
    df.extent = ext
    if df.scale < int(Processing_Variables['Variables']['DataframeScale']):
        df.scale = int(Processing_Variables['Variables']['DataframeScale'])
    else:
        df.scale = round(df.scale,-3) + 1000

    newXMax = ext.XMax + int(Processing_Variables['Variables']['ExtentDistance'])
    newXMin = ext.XMin - int(Processing_Variables['Variables']['ExtentDistance'])
    newYMax = ext.YMax + int(Processing_Variables['Variables']['ExtentDistance'])
    newYMin = ext.YMin - int(Processing_Variables['Variables']['ExtentDistance'])

    #Set Processing Extent
    arcpy.env.extent = arcpy.Extent(newXMin,newYMin,newXMax,newYMax)

    return(Processing_Variables['PROCESS_STATUS'])
#---------------------------------------------------------------------------------------------------------
# DetermineRequirements()
#
#       Test if we need to create the workspace file geodatabases, and then do it if necessary.
#          Return 0 - nothing to do
#                 1 - successful
#                -1 - unknown failure
#
#---------------------------------------------------------------------------------------------------------
def DetermineRequirements():
    #find what legal values are we constrained by.
    Processing_Variables['PROCESS_STATUS'] = 0
    Processing_Variables['PROCESS_INFO']   = "PreppingMXD"  

    Message('    - Determining What Card to Run', 2)

    for row in arcpy.da.SearchCursor(Processing_Variables['LegalArea'],['LegalArea',"SHAPE@"]):
        for shape in Processing_Variables['ShapeArea']:
            if shape.within(row[1]) or row[1].overlaps(shape):
                Processing_Variables['LegalLocation'] = row[0]

    return(Processing_Variables['PROCESS_STATUS'])
#---------------------------------------------------------------------------------------------------------
# SelectLayers()
#
#       Select all layers that exist in the Processing Lookup table to make processing faster. Write to memory
#
#---------------------------------------------------------------------------------------------------------
def SelectLayers():
    Processing_Variables['LayerList'] = []
    #Create a selection of all layers within the LUT Processing Table to make processing faster
    Message('    - Analyzing Layers in the Defined Extent',2)
    for row in arcpy.da.SearchCursor(Processing_Variables['ProcessingLookupTable'],['Layer_List',Processing_Variables['LegalLocation']]):
        if row[1] > 0:
            for item in str(row[0]).replace("None",'').split(';'):
                try:
                    item = item.split(':')[0]
                except:
                    item = item
                Processing_Variables['LayerList'].append(item)

    layercount = 0
    for layer in arcpy.mapping.ListLayers(mxd):
        if layer.name not in Processing_Variables['LayerList']:
            pass
        else:
            layercount += 1
            count = arcpy.GetCount_management(layer)
            if str(count) == '0':
                Processing_Variables['NoOverlap'].append(layer.name)
            else:
                arcpy.Select_analysis(layer,'in_memory\\Selection_' + str(layercount))
                oldname = str(layer.name)
                newname = 'Selection_' + str(layercount)
                Processing_Variables['SelectionLayers'][oldname] = newname

#----------------------------------------------------------------------------------------------------
#
#
#----------------------------------------------------------------------------------------------------
def containsoverlap(layer,label,cursorfieldlist,Buffer_Meters):
    concatattribute = ''
    
    with arcpy.da.SearchCursor(layer,cursorfieldlist) as cursor:
        for row in cursor:
            if str(row[0]) ==  "None":
                pass
            else:
                for area in Processing_Variables['ShapeArea']:
                    if row[0].overlaps(area) or row[0].contains(area) or area.contains(row[0]):
                        Processing_Variables['Applicable'][label] = 'Y'
                        if len(cursorfieldlist) > 1:
                            for num in range(1,len(cursorfieldlist)):
                                concatattribute = concatattribute + ' ' + str(row[num])
    try:
        Processing_Variables['AttributeInformation'][label].append(concatattribute)
    except:
        Processing_Variables['AttributeInformation'][label] = [concatattribute]

    if Processing_Variables['Applicable'][label][:1] not in ['X','Y']:
        with arcpy.da.SearchCursor(layer,cursorfieldlist) as cursor:
            for row in cursor:
                for area in Processing_Variables['ShapeArea']:
                    buff = area.buffer(Buffer_Meters)
                    if row[0].overlaps(buff) or row[0].touches(buff) or buff.contains(row[0]):
                            Processing_Variables['Applicable'][label] = 'X -' + str(Buffer_Meters)
                            break

    else:
        pass

    return
#----------------------------------------------------------------------------------------------------
#
#
#----------------------------------------------------------------------------------------------------
def overlaptouching(layer,label,cursorfieldlist,Buffer_Meters):
    concatattribute = ''

    with arcpy.da.SearchCursor(layer,cursorfieldlist) as cursor:
        for row in cursor:
            if str(row[0]) ==  "None":
                pass
            else:
                for area in Processing_Variables['ShapeArea']:
                    if row[0].overlaps(area) or row[0].touches(area) or area.contains(row[0]) and row[0].euqals(area) == False:
                        Processing_Variables['Applicable'][label] = 'Y'
                        if len(cursorfieldlist) > 1:
                            for num in range(1,len(cursorfieldlist)):
                                concatattribute = concatattribute + ' ' + row[num]
    try:
        Processing_Variables['AttributeInformation'][label].append(concatattribute)
    except:
        Processing_Variables['AttributeInformation'][label] = [concatattribute]
    
    if Processing_Variables['Applicable'][label][:1] not in ['X','Y']:
        with arcpy.da.SearchCursor(layer,cursorfieldlist) as cursor:
            for row in cursor:
                for area in Processing_Variables['ShapeArea']:
                    buff = area.buffer(Buffer_Meters)
                    if row[0].overlaps(buff) or row[0].touches(buff) or buff.contains(row[0]):
                            Processing_Variables['Applicable'][label] = 'X -' + str(Buffer_Meters)
                            break
    else:
        pass

    return
#----------------------------------------------------------------------------------------------------
#
#
#----------------------------------------------------------------------------------------------------
def contained(layer,label,cursorfieldlist):
    concatattribute = ''

    #Must make it a Yes, will change to N IF they are contained in each other.
    Processing_Variables['Applicable'][label] = 'Y'
    with arcpy.da.SearchCursor(layer,cursorfieldlist) as cursor:
        for row in cursor:
            if str(row[0]) ==  "None":
                pass
            else:
                for area in Processing_Variables['ShapeArea']:
                    if row[0].contains(area):
                        Processing_Variables['Applicable'][label] = 'N'
                        break
                    else:
                        pass
                                     

    return
#----------------------------------------------------------------------------------------------------
#
#
#----------------------------------------------------------------------------------------------------
def pointline(layer,label,cursorfieldlist,Buffer_Meters):
    concatattribute = ''

    with arcpy.da.SearchCursor(layer,cursorfieldlist) as cursor:
        for row in cursor:
            if str(row[0]) ==  "None":
                pass
            else:
                for area in Processing_Variables['ShapeArea']:
                    if area.contains(row[0]) or area.touches(row[0]):
                        Processing_Variables['Applicable'][label] = 'Y'
                        if len(cursorfieldlist) > 1:
                            for num in range(1,len(cursorfieldlist)):
                                concatattribute = concatattribute + ' ' + row[num]
    try:
        Processing_Variables['AttributeInformation'][label].append(concatattribute)
    except:
        Processing_Variables['AttributeInformation'][label] = [concatattribute]
    
    if Processing_Variables['Applicable'][label][:1] not in ['X','Y']:
        with arcpy.da.SearchCursor(layer,cursorfieldlist) as cursor:
            for row in cursor:
                for area in Processing_Variables['ShapeArea']:
                    buff = area.buffer(Buffer_Meters)
                    if buff.contains(row[0]) or buff.touches(row[0]) or row[0].crosses(buff):
                        Processing_Variables['Applicable'][label] = 'X -' + str(Buffer_Meters)
                        break
                else:
                    pass
    return
#---------------------------------------------------------------------------------------
#
#
#----------------------------------------------------------------------------------------------------
def BECDefinedAreas(label, query,queryfield,layer):
    #Search through overlapping BEC layers to find the values that intersect with the block/road
    if len(Processing_Variables['ExistingBEC']) < 1:
        with arcpy.da.SearchCursor(layer,[queryfield,'SHAPE@']) as cursor:
            for row in cursor:
                for area in Processing_Variables['ShapeArea']:
                    if row[1].overlaps(area) or row[1].contains(area):
                       Processing_Variables['ExistingBEC'].append(row[0].replace(' ',''))
    # The above code created a list of all bec that overlaps with the block. 
    #Loop through the list and see if it falls into any of the required values in the LUT_PRocessing Table. 
    # If a value has a * that means that it is looking for any BEC value that has that Zone and Subzone and Variant. 
    for zone in query:
        if '*' in zone:
            for bec in Processing_Variables['ExistingBEC']:
                if zone.replace('*','') in bec:
                    Processing_Variables['Applicable'][label] = 'BA'
                    return()
        else:
            if zone in Processing_Variables['ExistingBEC']:
                Processing_Variables['Applicable'][label] = 'BA'
                return()
    return ()
#----------------------------------------------------------------------------------------------------
#
#
#----------------------------------------------------------------------------------------------------
def WildlifeHabitatAreas(label,query,queryfield,layer):
    if len(Processing_Variables['whacodes']) < 1:
        Message("Analyzing: Wildlife Habitat Areas",4)
        with arcpy.da.SearchCursor(layer,[queryfield,'SHAPE@']) as cursor:
            for row in cursor:
                for area in Processing_Variables['ShapeArea']:
                    if row[1].overlaps(area) or area.contains(row[1]) or row[1].contains(area):
                       Processing_Variables['whacodes'].append(row[0])

    concatattribute = ''
    for zone in Processing_Variables['whacodes']:
        if zone in query:
            Processing_Variables['Applicable'][label] = 'Y'
            concatattribute = concatattribute + ' ' + str(zone)
        else:
            pass
    try:
        Processing_Variables['AttributeInformation'][label].append(concatattribute)
    except:
        Processing_Variables['AttributeInformation'][label] = [concatattribute]
    return()
#----------------------------------------------------------------------------------------------------
#
#
#----------------------------------------------------------------------------------------------------
def UngulateWinterRange(label,query,queryfield,layer):

    if len(Processing_Variables['ungulatecodes']) < 1:
        # Message("Analyzing: Ungulate Winter Range",4)
        with arcpy.da.SearchCursor(layer,[str(queryfield),'SHAPE@']) as cursor:
            for row in cursor:
                for area in Processing_Variables['ShapeArea']:
                    if row[1].overlaps(area) or area.contains(row[1]) or row[1].contains(area):
                       Processing_Variables['ungulatecodes'].append(row[0])
    concatattribute = ''
    for zone in Processing_Variables['ungulatecodes']:
        if zone in query:
            Processing_Variables['Applicable'][label] = 'Y'
            concatattribute = concatattribute + ' ' + str(zone)
        else:
            pass
    try:
        Processing_Variables['AttributeInformation'][label].append(concatattribute)
    except:
        Processing_Variables['AttributeInformation'][label] = [concatattribute]

    return()
#----------------------------------------------------------------------------------------------------
#
# The following requires special processing and cannot be run in the above processess
#
#----------------------------------------------------------------------------------------------------
def SpecialProcessing(label,layer,cursorfieldlist,BufferDistance):
    concatattribute = ''

    #---------------------------------------------------------------------------------------------------------
    #Landscape Level Biodiversity
    if label in  ["Landscape Level Biodiversity: Adjacent to Another Harvested Cutblock (100m Buffer Analysis)","Landscape Level Biodiversity: Adjacent to Another Planned Cutblock (100m Buffer Analysis)"]:
        with arcpy.da.SearchCursor(layer,cursorfieldlist) as cursor:
            for row in cursor:
                if str(row[cursorfieldlist.index("SHAPE@")]) ==  "None":
                    pass
                else:
                    for area in Processing_Variables['ShapeArea']:
                        if row[0].equals(area):
                            pass
                        else:
                            buff = area.buffer(BufferDistance)
                            if row[0].overlaps(buff) or row[0].touches(buff) or buff.contains(row[0]):
                                Processing_Variables['Applicable'][label] = 'Y'
                                if len(cursorfieldlist) > 1:
                                    for num in range(1,len(cursorfieldlist)):
                                        concatattribute = concatattribute + ' ' + row[num]
        try:
            Processing_Variables['AttributeInformation'][label].append(concatattribute)
        except:
            Processing_Variables['AttributeInformation'][label] = [concatattribute]

        

    #---------------------------------------------------------------------------------------------------------
    #MaxCutblockSize
    elif label == "Landscape Level Biodiversity: Max Cutblock Size":
        if Processing_Variables['RCTYPE'] == "Block":
            totalarea = 0
            #Search for NAR area, if the SU is PROD status.
            with arcpy.da.SearchCursor(layer,["CUTB_SEQ_NBR","NAR","SUTY_TYPE_ID"]) as cursor:
                for row in cursor:
                    if row[0] == Processing_Variables['UNIQUEID'] :
                        if row[2] in ['PROD']:
                            totalarea += float(str(row[1]).replace("None",'0'))

            if totalarea > 40:
                Processing_Variables['Applicable'][label] = 'Applicable (NAR)' + str(totalarea) + ' ha.'
            else:
                Processing_Variables['Applicable'][label] = 'Not Applicable (NAR)  ' + str(totalarea) + ' ha.'
            
            # if NAR NUM does not work for the block, then go by Gross Area.
            if totalarea == 0:
                with arcpy.da.SearchCursor(Processing_Variables['ShapeOfInterest'],["GROSS_AREA"]) as cursor:
                    for row in cursor:
                        totalarea += float(str(row[0]).replace("None",'0'))
                if int(totalarea) > 40:
                    Processing_Variables['Applicable'][label] = 'Applicable (Gross Area) ' + str(totalarea) + ' ha.'
                else:
                    Processing_Variables['Applicable'][label] = 'Not Applicable (Gross Area)  ' + str(totalarea) + ' ha.'   

        elif Processing_Variables['RCTYPE'] == "Road":           
            Processing_Variables['Applicable'][label] = "I dont know what to do with roads yet."

    
    #---------------------------------------------------------------------------------------------------------
    #Consultative Areas
    elif label == 'Consultative Areas':
        with arcpy.da.SearchCursor(layer,['SHAPE@',"BOUNDARY_NAME","CONTACT_ORG"]) as cursor:
            for row in cursor:
                if str(row[0]) ==  "None":
                    pass
                else:
                    for area in Processing_Variables['ShapeArea']:
                        buff = area.buffer(BufferDistance)
                        if row[0].overlaps(buff) or buff.contains(row[0]) or row[0].contains(buff):
                            if row[1] == row[2]:
                                name = '    ' + row[1]
                            else:
                                name = '    ' + row[1] + ': ' + row[2]
                            Processing_Variables['Applicable'][label] = 'Y'
                            Processing_Variables['Applicable'][name] = 'Y'


    #---------------------------------------------------------------------------------------------------------  
    #Grizzly Bear
    elif label in ['Grizzly Bear Habitat','Grizzly Bear Habitat RMZ']:      
        def grizhabitat():
            with arcpy.da.SearchCursor('LRMP Grizzly Bear RMZ',['SHAPE@']) as cursor:
                for row in cursor:
                    for area in Processing_Variables['ShapeArea']:
                        if row[0].overlaps(area) or row[0].contains(area) or area.contains(row[0]):
                            Processing_Variables['Applicable']['Grizzly Bear Habitat RMZ'] = 'Y'

            

        def grizsuitability():
            env.workspace = 'in_memory'
            arcpy.Intersect_analysis(["LRMP Grizzly Bear Suitability",Processing_Variables['ShapeOfInterest']],'in_memory\\GrizzlySuitIntersect')
            value = {"High":1,"High-Mod":2,"Moderate":3,"Low":4,"Very Low":5, "Nil":6, "Unrated":7}
            highestrating = 90
            with arcpy.da.SearchCursor('in_memory\\GrizzlySuitIntersect',['SUIT']) as cursor:
                for row in cursor:
                    try:
                        if value[row[0]] < highestrating:
                            highestrating = value[row[0]]
                    except:
                        pass
            try:
                numtocode = {1:"H",2:"H-M",3:'M',4:'L',5:'VL', 6:'Nil',7:'N/R'}   
                Processing_Variables['Applicable']['Grizzly Bear Habitat'] = 'Y'
                Processing_Variables['AttributeInformation']['Grizzly Bear Habitat'] = "Highest Ranking Value: " + numtocode[highestrating]
            except:
                Processing_Variables['Applicable']['Grizzly Bear Habitat'] = 'N'                
                return(Processing_Variables['Applicable'],Processing_Variables['AttributeInformation'])

        #run grizzly bear
        grizhabitat()
        # If griz habitat is applicable run the suitability.
        if Processing_Variables['Applicable']['Grizzly Bear Habitat RMZ'] == 'Y':
            grizsuitability()
        else:
            Processing_Variables['Applicable']['Grizzly Bear Habitat'] = 'N'

    return
#----------------------------------------------------------------------------------------------------
#
# The following requires special processing and cannot be run in the above processess
#
#----------------------------------------------------------------------------------------------------
def SpecialProcessingNoLayer(label):    
    
    #---------------------------------------------------------------------------------------------------------
    #Hydrological
    if label == 'Hydrological':
        for item in ["Fisheries Sensative Watershed",'Community Watersheds']:
            try:
                if Applicable[item] == 'Y':
                    Processing_Variables['Applicable'][label] = 'Y'
                    return()
            except:
                pass

    return
#========================================================================================================
#  Initial Routines
#========================================================================================================
def OrganizeRouteCardItems():
    Processing_Variables['PROCESS_STATUS'] = 0
    Processing_Variables['PROCESS_INFO']   = "PreppingMXD"  

    Message('    - Running Analysis', 2)

    #Sort Processing Table in the order that items have been assigned.
    Processing_Variables["Applicable"] = OrderedDict()
    arcpy.Sort_management (Processing_Variables['ProcessingLookupTable'], 'in_memory\\sorttable', [[Processing_Variables['LegalLocation'],"ASCENDING"]])

    itemlist = []
    cursorfieldlist = ["Item","Processing","Layer_List","Query_Values","Query_Field","CannedStatement","BufferDistance"]
    cursorfieldlist.append(Processing_Variables['LegalLocation'])
    for row in arcpy.da.SearchCursor('in_memory\\sorttable',cursorfieldlist):
        if row[cursorfieldlist.index(Processing_Variables['LegalLocation'])] > 0:
        #Create the list of all items taht should be used based on the location.
            item = row[cursorfieldlist.index("Item")]
            Processing = row[cursorfieldlist.index("Processing")]
            Layer_List = str(row[cursorfieldlist.index("Layer_List")]).replace("None",'').split(';')
            Query_Values = str(row[cursorfieldlist.index("Query_Values")]).replace("None",'').split(',')
            Query_Field = row[cursorfieldlist.index("Query_Field")]
            Buffer_Meters = float(row[cursorfieldlist.index("BufferDistance")])
            # LegendGroup = row[cursorfieldlist.index("LegendGroup")]
            Processing_Variables['CannedStatement'][item] = row[cursorfieldlist.index("CannedStatement")]
            # LegendElement = row[cursorfieldlist.index("LegendElement")]
            itemlist.append([item,Processing,Layer_List,Query_Values,Query_Field,Buffer_Meters])
            Processing_Variables['layerdict'][item] = [Layer_List]

    for i in itemlist:
        label = i[0]
        processingunit = i[1]
        if processingunit == 'title':
            output = ''
        elif processingunit == 'nonspatial':
            output = 'ZZZ'
        else:
            output = 'N'
        Processing_Variables['Applicable'][label] = output

    ungulatecount = 0
    whacount = 0
    bandcount = 0

    #Start the Processing Options
    for i in itemlist:
        label = i[0]
        processingunit = i[1]
        buffdist = i[5]
        if processingunit in ('title','nonspatial'):
            pass
        else:
            layerslist = i[2]
            for layer in layerslist:
                cursorlist = ['SHAPE@']
                # Message( "Analyzing: "+ label,2)
                # if there is information that is wanted from the layer, extract fields of interest.
                if ':' in layer:
                    #fields split must occur before the layer split because we are reassigning layer
                    fields =  layer.split(':')[1].split(',')
                    layer = layer.split(':')[0]

                    if len(fields) > 0:
                        for f in fields:
                            if f == '':
                                pass
                            else:
                                cursorlist.append(f)
                # Skip values that have already been determined
                if Processing_Variables['Applicable'][label] in ['BA']:
                    pass

                # Contained if outside of the regular functions due to the fact that we need to bypass the "NoOverlap" Section.
                if processingunit == "contained":
                    contained(layer,label,cursorlist)

                if layer in Processing_Variables['NoOverlap']:
                    pass

                else:
                    #send to  analysis where the layer is predefined and hardcoded into the script
                    if processingunit == "special_processing_no_layer":
                        SpecialProcessingNoLayer(label)
                    if processingunit == "default_to_yes":
                        Processing_Variables['Applicable'][label] = 'Y'
                        
                    #define layer for analysis
                    try:
                        selectname = Processing_Variables['SelectionLayers'][layer]
                        selectionlayer = 'in_memory\\' + selectname
                    except:
                        selectionlayer = layer

                    if processingunit == "special_processing":
                        SpecialProcessing(label,selectionlayer,cursorlist,buffdist)
                    
                    if processingunit == 'contains_overlap_layers':
                        containsoverlap(selectionlayer,label,cursorlist,buffdist)

                    if processingunit == 'highestvalue':
                        containsoverlap(selectionlayer,label,cursorlist)

                    if processingunit == 'polygon_coverages':
                        polygoncoverages(selectionlayer,label)

                    if processingunit == 'point_line_layers':
                        pointline(selectionlayer,label,cursorlist,buffdist)

                    if processingunit == 'overlap_touching_layers':
                        overlaptouching(selectionlayer,label,cursorlist)

                    if processingunit == 'BEC':
                        query = i[3]
                        field = i[4]
                        BECDefinedAreas(label,query,field,selectionlayer)

                    if processingunit == 'ungulate_winter_range':
                        if ungulatecount > 0 and len(Processing_Variables['ungulatecodes']) < 1:
                            Processing_Variables['Applicable'][label] = 'N'
                        else:
                            ungulatecount += 1
                            query = i[3]
                            field = i[4]
                            UngulateWinterRange(label,query,field,selectionlayer)

                    if processingunit == 'wildlife_habitat_areas':
                        if whacount > 0 and len(Processing_Variables['whacodes']) < 1:
                            Processing_Variables['Applicable'][label] = 'N'
                        else:
                            whacount += 1
                            query = i[3]
                            field = i[4]
                            WildlifeHabitatAreas(label,query,field,selectionlayer)

#=========================================================================================================
#  Output Routines
#=========================================================================================================
def WriteToExcel():
    Message('   Create Excel Output',2)

    import xlwt

    wb = xlwt.Workbook()
    ws = wb.add_sheet('Route Card Tool Assessment')
    ws.set_portrait(False)

    #Set Excel Styles
    xlwt.add_palette_colour("custom_colour", 0x21)
    xlwt.add_palette_colour("darkergreen", 0x22)
    wb.set_colour_RGB(0x21, 216, 228, 188)
    wb.set_colour_RGB(0x22, 196, 215, 155)


    BigTitle = xlwt.easyxf('font: name Times New Roman, color-index black, bold on; pattern: pattern solid, fore_colour darkergreen; align: wrap on;')
    BlackBoldStyle = xlwt.easyxf('font: name Times New Roman, color-index black, bold on; pattern: pattern solid, fore_colour custom_colour; align: wrap on;')
    RedSyle = xlwt.easyxf('font: name Times New Roman, color-index red; align: wrap on; borders: left thin, right thin, top thin, bottom thin, bottom_colour gray25, left_colour gray25, right_colour gray25, top_colour gray25;')
    BlackStyle = xlwt.easyxf('font: name Times New Roman, color-index black; align: wrap on;borders: left thin, right thin, top thin, bottom thin, bottom_colour gray25, left_colour gray25, right_colour gray25, top_colour gray25;')
    BlackStyleNoBorder = xlwt.easyxf('font: name Times New Roman, color-index black; align: wrap on;')
    OrangeStyle = xlwt.easyxf('font: name Times New Roman, color-index orange; align: wrap on; borders: left thin, right thin, top thin, bottom thin, bottom_colour gray25, left_colour gray25, right_colour gray25, top_colour gray25;')
    BlueStyle = xlwt.easyxf('font: name Times New Roman, color-index blue; align: wrap on; borders: left thin, right thin, top thin, bottom thin,bottom_colour gray25, left_colour gray25, right_colour gray25, top_colour gray25;')
    GreyStyle = xlwt.easyxf('font: name Times New Roman, color-index gray50; align: wrap on;borders: left thin, right thin, top thin, bottom thin,bottom_colour gray25, left_colour gray25, right_colour gray25, top_colour gray25;')
    GreyStyleBottomOnly = xlwt.easyxf('font: name Times New Roman,height 260, color-index gray50; align: wrap on; borders: bottom thin, bottom_colour gray25;')

    #Set the column Widths

    ws.col(0).width = 256 * 5
    ws.col(1).width = 256 * 37
    ws.col(2).width = 256 * 15
    ws.col(3).width = 256 * 20
    ws.col(4).width = 256 * 60
    ws.col(5).width = 256 * 8

    #--------------------------------------
    # START: Headers and Titles Below
    #--------------------------------------
    outputname = ''
    for item in Processing_Variables['TitleFields'].split(','):
        outputname += str(Processing_Variables['Title'][item]) + "_"

    ws.write_merge(0,0,1,3,'FRPA Planning Route Card - ' + str(Processing_Variables['LegalLocation']),GreyStyleBottomOnly)
    ws.write_merge(2,2,1,4,outputname.replace('_',' '),BigTitle)
    
    ws.row(5).height_mismatch = True
    ws.row(5).height = 760
    ws.write_merge(5,5,1,4,"OBJECTIVE: Planning Route Card is a due diligence checklist for the Planning Forester to identify legal and non-legal commitments associated with proposed block/road development, to track completion of assessments/analyses, to identify roles and responsibilities, and provide a communication tools between the Planning Foresters, Practices Foresters, and layout contractors.",BlackStyleNoBorder)


    #--------------------------------------
    # END: Headers and Titles Below
    #--------------------------------------
    # write (Row, Column, information, style)
    rownum = 7
    applicablecolumn = 2
    commentcolumn = 4
    otherColumn = 3
    titlecolumn = 1
    
    # Add BEC Values to Output
    rownum = rownum + 1
    becs = str(Processing_Variables['ExistingBEC']).replace('[','').replace(']','').replace('u\'','').replace('\'','')
    ws.write(rownum,titlecolumn, 'Biogeoclimatic Zone', GreyStyle)
    ws.write_merge(rownum,rownum,applicablecolumn,commentcolumn,becs, GreyStyle)
    
    # Message(Processing_Variables['Applicable'],2)
    for value in Processing_Variables['Applicable']:
        comment = ''
        
        if Processing_Variables['Applicable'][value][:1] not in ['','Z',"N","X"]:
            if value in Processing_Variables['CannedStatement'].keys():
                comment = str(Processing_Variables['CannedStatement'][value]).replace("None",'')

        if Processing_Variables['Applicable'][value][:1] not in ['','Z',"N","X"]:
            if value in Processing_Variables['AttributeInformation'].keys():
                if "Highest Ranking Value" in Processing_Variables['AttributeInformation'][value]:
                    pass
                else:
                    for string in list(set(Processing_Variables['AttributeInformation'][value])):
                        comment = comment + chr(10) + string

        otherassessment = ' '
        if Processing_Variables['Applicable'][value][:3] == "App":
            style = RedSyle
            ynvalue = Processing_Variables['Applicable'][value]
        elif Processing_Variables['Applicable'][value][:3] == "Not":
            style = BlackStyle
            ynvalue = Processing_Variables['Applicable'][value]
        elif Processing_Variables['Applicable'][value] == '':
            rownum += 1
            style = BlackBoldStyle
            ynvalue = "Applicable (Y/N)"
            otherassessment = "Additional Assessments Needed (Y/N)"
            comment = "Comments"
        elif Processing_Variables['Applicable'][value] == "Y":
            Processing_Variables['Applicable'][value] = "Y"
            style = RedSyle
            ynvalue = Processing_Variables['Applicable'][value]
        elif Processing_Variables['Applicable'][value] == "N":
            Processing_Variables['Applicable'][value] = "N"
            style = BlackStyle
            ynvalue = Processing_Variables['Applicable'][value]
        elif Processing_Variables['Applicable'][value] == "ZZZ":
            Processing_Variables['Applicable'][value] = "Non Spatial"
            style = BlackStyle
            ynvalue = Processing_Variables['Applicable'][value]
        elif Processing_Variables['Applicable'][value][:1] == "X":
            dist = Processing_Variables['Applicable'][value].split('-')[1]
            Processing_Variables['Applicable'][value] = "Within " + str(dist).replace('.0','') +"m of Block"  
            style = OrangeStyle
            ynvalue = Processing_Variables['Applicable'][value]
        elif Processing_Variables['Applicable'][value] == "BA":
            Processing_Variables['Applicable'][value] = "BEC Applicable" 
            style = BlueStyle
            ynvalue = Processing_Variables['Applicable'][value]
        else:
            style = GreyStyle
            ynvalue = Processing_Variables['Applicable'][value]

        rownum += 1

        #write the cells
        ws.write(rownum,titlecolumn, value, style)
        ws.write(rownum,applicablecolumn, ynvalue , style)
        ws.write(rownum,otherColumn, otherassessment , style)
        ws.write(rownum,commentcolumn,comment, style)

    #Add Disclaimer Statement
    rownum += 2
    ws.row(rownum).height_mismatch = True
    ws.row(rownum).height = 1100
    ws.write_merge(rownum,rownum,1,4,'The Planning Route Card (PRC) is a guidance tool listing constraints applicable at time of preparation.  The PRC does not prescribe management practices.  It is incumbent on the Site Plan author and signatory to ensure management practices and decisions are consistent with the intent of the applicable legislation, higher level plans, Forest Stewardship Plan, Statutory Decision Maker direction, best management practices, and general wildlife measures outlined in GAR Orders. The content of the PRC alone cannot be used for justification of, or as a rationale for management decisions contained in any professional documents.', BlackStyle)
    
    #Add Signature Area
    rownum += 1
    ws.write(rownum,1,'Planning Forester Signoff', BlackStyle)
    ws.write_merge(rownum,rownum,2,3,'Prepared By:' + Processing_Variables['Owner'], BlackStyle)
    ws.write(rownum,4,'Date:', BlackStyle)

    #Add Map Attachment Block.
    rownum += 2
    ws.write_merge(rownum,rownum,1,4,'Attach 1:10,000 letter size map showing block with overlaps and forward to Practices Forester', BlackStyle)


    #Need to change where items will be saved.
    
    outputfile = Processing_Variables['OutputLocation'] + '\\' + outputname.replace('.0','') + Processing_Variables['Status'] + "_RouteCard.xls"
    wb.save(str(outputfile))

#-----------------------------------------------------------------------------------------------------
def Layout():
    Message('   Create Final Map Output',2)    
    mxd = arcpy.mapping.MapDocument("CURRENT")

    Processing_Variables['LayerList'] 
    #find all layers that have a "hit" so they can be made visible.
    visiblelayers = []
    for item in Processing_Variables['Applicable']:
        if Processing_Variables['Applicable'][item][:1] in ['Y','B',"A"]:
    ##            if item in Processing_Variables['layerdict'].keys():
    ##                for l in Processing_Variables['layerdict'][item]:
    ##                    if ':' in l:
    ##                    #fields split must occur before the layer split because we are reassigning layer
    ##                        fields =  l.split(':')[1].split(',')
    ##                        layer = l.split(':')[0]
    ##                    else:
    ##                        layer = l
    ##                    for lyr in layer:
    ##                        visiblelayers.append(lyr)
            #FOR SOME REASON LAYERS IN MXD NOT GETTING TURNED ON AND OUTPUT PDF IS EMPTY.  PROBABLY HAS TO DO WITH LUT_PROCESSING EDITING USING EXCEL VIA XTOOLS
            #THIS IS A TEMPORARY PATCH TO GET IT WORKING AGAIN UNTIL I CAN FIGURE OUT HOW TO FIX THE LUT
            for l in Processing_Variables['LayerList']:
                if ':' in l:
                #fields split must occur before the layer split because we are reassigning layer
                    fields = l.split(':')[1].split(',')
                    layer = l.split(':')[0]
                    visiblelayers.append(layer)
                else:
                    visiblelayers.append(l)


    # Message(visiblelayers,2)
    #Clear selected layers and remove the UBI of Interest layer in memory Turn on any applicable layers.
    for layer in arcpy.mapping.ListLayers(mxd):
        if layer.supports("TRANSPARENCY"):
            if layer.transparency > 0:
                layer.transparency = 0
        if layer.name in visiblelayers:
            layer.visible = True
        if layer.name == "SearchBuffer":
            layer.name = str(Processing_Variables['Variables']['SearchBufferDistance']) + ' Meter Search Buffer' 
            layer.visible = True
        if layer.name == "ShapeOfInterest":
            layer.name = Processing_Variables['RCTYPE'] + ' of Interest'
            layer.visible = True
        if 'TOC FN' in layer.name or layer.name[:14] == "SensativeData_":
            layer.visible = False
        else:
            pass
            
    prevtext = {}
    for lyt in arcpy.mapping.ListLayoutElements(mxd,'TEXT_ELEMENT'):
        if lyt.name == 'Required':
            pass
        elif lyt.name in Processing_Variables['Title'].keys():
            prevtext[lyt.name] = lyt.text
            lyt.text = lyt.text + " " + str(Processing_Variables['Title'][lyt.name])
        elif lyt.name == 'Owner':
            lyt.text = Processing_Variables['Owner']
        else:
            prevtext[lyt.name] = lyt.text
            lyt.text = " "


    outputname = ''
    for item in Processing_Variables['TitleFields'].split(','):
        outputname += str(Processing_Variables['Title'][item]) + "_"
    arcpy.mapping.ExportToPDF(mxd, Processing_Variables['OutputLocation'] + '\\' + outputname.replace('.0','') + Processing_Variables['Status'] +"_Map.pdf", picture_symbol = "VECTORIZE_BITMAP")


    #Reset all title elements and extent!
    for lyt in arcpy.mapping.ListLayoutElements(mxd,'TEXT_ELEMENT'):
        if lyt.name in prevtext.keys():
            lyt.text = prevtext[lyt.name]

    extlayer = arcpy.mapping.Layer(Processing_Variables['LegalArea'])
    ext = extlayer.getExtent()
        
    newXMax = ext.XMax 
    newXMin = ext.XMin
    newYMax = ext.YMax
    newYMin = ext.YMin

    #Set Processing Extent
    arcpy.env.extent = arcpy.Extent(newXMin,newYMin,newXMax,newYMax)

    # mxd.save()

#*********************************************************************************************************
#  Main Program
#*********************************************************************************************************

#---------------------------------------------------------------------------------------------------------
# Run Main for ArcGIS 10.1
#
#   Main Method manages the overall program
#---------------------------------------------------------------------------------------------------------
def runMain():

    Initialize()
    ResetMXD()
    if RCTYPE == 'Block':
        SelectBlocks()
    elif RCTYPE == 'Road':
        SetupRoads()
    PrepMXD()
    DetermineRequirements()
    SelectLayers()
    OrganizeRouteCardItems()
    WriteToExcel()
    Layout()

    return Processing_Variables['PROCESS_STATUS']

#*********************************************************************************************************

#  Execution
#*********************************************************************************************************

runMain()

#---------------------------------------------------------------------------------------------------------
#  Clean-up
#---------------------------------------------------------------------------------------------------------


END_TIME       = time.ctime(time.time())
END_TIME_SEC   = time.time()

END_TIME_SQL   = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

EXECUTION_TIME = END_TIME_SEC - START_TIME_SEC

if EXECUTION_TIME < 120:

    EXECUTION_TIME_STRING = str(int(EXECUTION_TIME)) + ' seconds.'
elif EXECUTION_TIME < 3600:
    EXECUTION_TIME_STRING = str(round(EXECUTION_TIME / 60, 1)) + ' minutes.'
else:
    EXECUTION_TIME_STRING = str(round(EXECUTION_TIME / 3600, 2)) + ' hours.'



#*********************************************************************************************************
#  End of Program
#*********************************************************************************************************
