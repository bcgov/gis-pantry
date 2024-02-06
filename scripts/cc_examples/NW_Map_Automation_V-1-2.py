'''
Author: Kevin de Souza
Updated: 2023Apr28
Description:
    An Arcmap tool to be used as a part of the statusing process. This tool Automates the production of maps categorized by their corresponding overlapping layers
    found in the IOR. This tool was developed in python 2.7 for the Northwest Mining Region.
    
'''

import os
import arcpy 
import datetime
from arcpy import env
from getpass import getuser
from shutil import rmtree

from bisect import bisect 


arcpy.env.overwriteOutput = True
mxd = arcpy.mapping.MapDocument(r"\\path\to\map_templates\NW\NorthWest_StatusTemplate_TEST.mxd")


mine_name = arcpy.GetParameterAsText(0)
NoWID = arcpy.GetParameterAsText(1)
pdf_path = arcpy.GetParameterAsText(2)
username = arcpy.GetParameterAsText(3)
bcgwpassword = arcpy.GetParameter(4)


def login(username, bcgwpassword):
    ''' 
    A login prompt to get the users username and password for both MTOPROD and BCGW,
    create database connections for each and log into the databases
    '''
    arcpy.AddMessage("Checking to see if database directory directory exists")
    if os.path.exists(os.path.join(r"\\path\to\scratchDB", getuser())):
        arcpy.AddMessage("Directory Exists")
        pass

    else:
        arcpy.AddMessage("Directory didn't exist")
        os.makedirs(os.path.join(r"\\path\to\scratchDB", getuser()))
        arcpy.AddMessage(os.path.join(r"\\path\to\scratchDB", getuser()))
    
    arcpy.AddMessage("Passed directory check")
    arcpy.AddMessage(os.path.join(r"\\path\to\scratchDB", getuser()))

    try:
        arcpy.AddMessage("Logging into BCGW...")
        arcpy.management.CreateDatabaseConnection(os.path.join(r"\\path\to\scratchDB", getuser()),
                                                  "BCGW.sde",
                                                  "ORACLE",
                                                  "bcgw.bcgov/idwprod1.bcgov",
                                                  "DATABASE_AUTH",
                                                  username,
                                                  bcgwpassword,
                                                  "DO_NOT_SAVE_USERNAME")
    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        arcpy.AddMessage("Entered Exception")
        if os.path.exists(os.path.join(r"\\path\to\scratchDB", getuser())):
            arcpy.Delete_management(r"\\path\to\scratchDB" + '\\' + getuser())
        else:
            pass
        
    arcpy.env.overwriteOutput = True
    env.workspace = os.path.join(r"\\path\to\scratchDB", getuser(), "BCGW.sde")
        

def addStatusLayer():
    """
    A function to add the statused feature class supplied by proponent. The user inputs the path to the working.gdb in the NOW folder.

    """

    mxd = arcpy.mapping.MapDocument(r"\\path\to\map_templates\NW\NorthWest_StatusTemplate.mxd")
    dataframe = arcpy.mapping.ListDataFrames(mxd)[0]
    maplayers = arcpy.mapping.ListLayers(dataframe)

    for lyr in maplayers:
        if lyr.name == "Status Area":
            lyr.definitionQuery = "CORE_NOW = '{}'".format(NoWID)
                
        arcpy.RefreshActiveView()
    
    arcpy.AddMessage("Setting definition query on status layer...")


     
    
    mxd.saveACopy(r"\\path\to\map_templates\NW\NorthWest_StatusTemplateCOPY.mxd")
    del mxd 




def MakeMaps(pdf_path, mine_name, NoWID):
    """
    A function to iterate through group layers, turning them on and exporting maps based on each group layer theme. This function uses the mapping module to identify layout elements, and 
    apply edits to allign with the theme of each map. 

    """

    today = datetime.date.today()
    stripped_NOW = NoWID.replace("-","")
    mxd = arcpy.mapping.MapDocument(r"\\path\to\map_templates\NW\NorthWest_StatusTemplateCOPY.mxd")
    dataframe = arcpy.mapping.ListDataFrames(mxd)[0]
    layers = arcpy.mapping.ListLayers(dataframe)
    mxd.activeView = "PAGE_LAYOUT"
    tenurePath = os.path.join(pdf_path, "1_TENURE_OVERLAPS_" + stripped_NOW + "_" + today.strftime("%Y%b%d") + ".pdf")
    envPath = os.path.join(pdf_path, "2_ENVIRONMENTAL_OVERLAPS_" + stripped_NOW + "_" + today.strftime("%Y%b%d") + ".pdf")
    fnPath = os.path.join(pdf_path, "3_FN_OVERLAPS" + stripped_NOW + "_" + today.strftime("%Y%b%d") + ".pdf")
    lupPath = os.path.join(pdf_path, "4_LUP_OVERLAPS_" + stripped_NOW + "_" + today.strftime("%Y%b%d") + ".pdf")
    otherPath = os.path.join(pdf_path, "5_OTHER_RESOURCE_OVERLAPS" + stripped_NOW + "_" + today.strftime("%Y%b%d") + ".pdf")
    skeenaPath = os.path.join(pdf_path, "6_SKEENA_STATUS_OVERLAPS_" + stripped_NOW + "_" + today.strftime("%Y%b%d") + ".pdf")




    
    mapLayers = arcpy.mapping.ListLayers(mxd, "Status Area", dataframe)
    statuslayer = mapLayers[0]
    arcpy.AddMessage("Getting layer extent")
    
    scales = [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 10000, 15000, 20000, 25000, 30000, 31000, 32000, 32500, 35000, 40000, 42500, 45000, 47500, 50000, 52500, 55000, 60000, 65000, 70000, 75000]
    
    Statusextent = statuslayer.getExtent(True)
    dataframe.extent = Statusextent
    old_scale = dataframe.scale
    arcpy.AddMessage(old_scale)
    new_scale = scales[bisect(scales, old_scale)]

    
    dataframe.scale = new_scale

    arcpy.AddMessage("Refreshing View")
    arcpy.RefreshActiveView()


    
    for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
        if elm.name == "title":
            elm.text = "1. Tenure Overlaps"

        if elm.name == "MineName":
            elm.text = mine_name
        
        if elm.name == "NoWID":
            elm.text = "NoW #: "+ NoWID

        arcpy.RefreshActiveView()


    for lyr in layers:
        if lyr.isGroupLayer and lyr.name == "1 - Tenure Overlaps":
            lyr.visible = True


    arcpy.AddMessage("Exporting Tenure Overlap Map... ")
    arcpy.mapping.ExportToPDF(mxd, tenurePath)



    for lyr in layers:
        if lyr.isGroupLayer and lyr.name == "1 - Tenure Overlaps":
            lyr.visible = False

    for lyr in layers:
        if lyr.isGroupLayer and lyr.name == "2 - ENVIRONMENTAL OVERLAPS":
            lyr.visible = True

    for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
        if elm.name == "title":
            elm.text = "2. Environmental Overlaps"
        arcpy.RefreshActiveView()


    arcpy.AddMessage("Exporting Environmental Overlap Map... ")
    arcpy.mapping.ExportToPDF(mxd, envPath)



    for lyr in layers:
        if lyr.isGroupLayer and lyr.name == "2 - ENVIRONMENTAL OVERLAPS":
            lyr.visible = False

    for lyr in layers:
        if lyr.isGroupLayer and lyr.name == "3 - FIRST NATIONS_CULTURAL HERITAGE":
            lyr.visible = True

    for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
        if elm.name == "title":
            elm.text = "3. First Nation Overlaps"
        if elm.name == "Arch Label":
            elm.text = "INTERNAL to B.C. Government\n Not for Distribution"
        
        arcpy.RefreshActiveView()


    arcpy.AddMessage("Exporting First Nation Map... ")
    arcpy.mapping.ExportToPDF(mxd, fnPath)



    for lyr in layers:
        if lyr.isGroupLayer and lyr.name == "3 - FIRST NATIONS_CULTURAL HERITAGE":
            lyr.visible = False

    for lyr in layers:
        if lyr.isGroupLayer and lyr.name == "4 - LAND USE PLAN OVERLAPS":
            lyr.visible = True

    for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
        if elm.name == "title":
            elm.text = "4. Land Use Plan Overlaps"

        if elm.name == "Arch Label":
            elm.text = " "

    arcpy.AddMessage("Exporting Land Use Plan Map... ")
    arcpy.mapping.ExportToPDF(mxd, lupPath)



    for lyr in layers:
        if lyr.isGroupLayer and lyr.name == "3 - FIRST NATIONS_CULTURAL HERITAGE":
            lyr.visible = False

    for lyr in layers:
        if lyr.isGroupLayer and lyr.name == "5 - OTHER RESOURCE OVERLAPS":
            lyr.visible = True

    for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
        if elm.name == "title":
            elm.text = "5. Over Resource Overlaps"
        if elm.name == "Arch Label":
            elm.text = " "
        arcpy.RefreshActiveView()


    arcpy.AddMessage("Exporting Other Resource Map... ")
    arcpy.mapping.ExportToPDF(mxd, otherPath)


    for lyr in layers:
        if lyr.isGroupLayer and lyr.name == "5 - OTHER RESOURCE OVERLAPS":
            lyr.visible = False

    for lyr in layers:
        if lyr.isGroupLayer and lyr.name == "6. Skeena Status Layers\n Non ILLR":
            lyr.visible = True

    for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
        if elm.name == "title":
            elm.text = "6 - Skeena Status Layers - Non ILLR Overlaps"
        arcpy.RefreshActiveView()


    arcpy.AddMessage("Exporting Skeena Map... ")
    arcpy.mapping.ExportToPDF(mxd, skeenaPath)


    
def logout():
    '''
    A logout prompt to delete the database connections created in the 'login' function
    '''
    arcpy.AddMessage("Logging out of BCGW...")
    if os.path.exists(os.path.join(r"\\path\to\scratchDB", getuser())):
        rmtree(os.path.join(r"\\path\to\scratchDB", getuser()))
    else:
        pass

login(username, bcgwpassword)

addStatusLayer()

MakeMaps(pdf_path, mine_name, NoWID)

logout()
