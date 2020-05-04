#A tool to report the open timber marks inside AOI Land
#Written by Jesse Fraser (jesse.fraser@gov.bc.ca)
#December 11th 2018
#Modifed by Owen Fritch (owen.fritch@gov.bc.ca) May 30 2019

import sys, string, os, time, win32com.client, datetime, win32api, arcpy, arcpy.mapping , csv
#import  wml_library_arcpy_v3 as wml_library
from arcpy import env

arcpy.env.overwriteOutput = True

try:
    arcpy.CheckOutExtension("Spatial")
    from arcpy.sa import *
    from arcpy.da import *
except:
    arcpy.AddError("Spatial Extension could not be checked out")
    os.sys.exit(0)
def printline(message):  
    """printline(message)  
  
        message(string):  
       The message to be printed  
    """  
    print message  
    arcpy.AddMessage(message)  

time = time.strftime("%Y%m%d")

#Area of Interest shapefile
AOI = arcpy.GetParameterAsText(0)

#Data Range choices
quarter = arcpy.GetParameterAsText(1)

#Year of interest
Year = arcpy.GetParameterAsText(2)
printline(Year)
#Save location
save = arcpy.GetParameterAsText(3)

#Name of Area of Interest
name = arcpy.GetParameterAsText(4)

#Location of BCGW w/Password embedded... You need to have a database called BCGW4Scripting.sde
BCGW = r'Database Connections\BCGW4Scripting.sde'

#Forest Harvest Authority Path
Harv = 'WHSE_FOREST_TENURE.FTEN_HARVEST_AUTH_POLY_SVW'

#Harvest Authority from BCGW
Input_Harv = os.path.join(BCGW,Harv)

#create layers to query
arcpy.MakeFeatureLayer_management(Input_Harv,"test_lyr")
lyr_fc = arcpy.mapping.Layer("test_lyr")

#Definition Query fields
issuedate = 'ISSUE_DATE'
expirydate = 'EXPIRY_DATE'	


#If statement testing which quarter folks want
if quarter == 'First':
	#Save location geodatabase
	gdbname = 'Q1_' + Year + '_Harvest_auth_'+ time
	#Query values
	datebase = 'date \'' + Year + '-04-01\''
	datefinish = 'date \'' + Year + '-06-30\''
	text = 'Q1_' + Year
	
elif quarter == 'Second':
	#Save location geodatabase
	gdbname = 'Q2_' + Year + '_Harvest_auth_'+ time
	#Query values
	datebase = 'date \'' + Year + '-07-01\''
	datefinish = 'date \'' + Year + '-09-30\''
	text = 'Q2_' + Year

elif quarter == 'Third':
	#Save location geodatabase
	gdbname = 'Q3_' + Year + '_Harvest_auth_'+ time
	#Query values
	datebase = 'date \'' + Year + '-10-01\''
	datefinish = 'date \'' + Year + '-12-31\''
	text = 'Q3_' + Year
	
elif quarter == 'Fourth':
	#Save location geodatabase
	gdbname = 'Q4_' + Year + '_Harvest_auth_'+ time
	#Query values
	datebase = 'date \'' + Year + '-01-01\''
	datefinish = 'date \'' + Year + '-03-31\''
	text = 'Q4_' + Year
else: 
	print "Invalid Quarter Value"
	arcpy.AddError("Invalid Quarter Value")
	
#Definition Query
defquery = expirydate + '>= ' + datebase + 'AND ' + issuedate + '<= ' + datefinish
	#O.Fritch 2019-05-30 changed expression to use ">=" and "<=" instead of ">" and "<"
	#Otherwise any permits issued on the last day of a quarter, or retired on the first day of a quarter, are never counted 
#Test to see if the values are correct
printline("Definition Query")
printline(defquery)

#Save location of geodatabase		
saveloc = save + '\\' + gdbname + '.gdb'

#Create the GDB
if os.path.exists(saveloc) == False:
 	arcpy.CreateFileGDB_management(save, gdbname)
	print "creating gdb"
#Definition Query based on quarter		
lyr_fc.definitionQuery = defquery

#Harvest Autorities inside of the AOI lands during the Quarter
saveout = saveloc + '\\' + name + '_Harvest_auth'
arcpy.Clip_analysis(lyr_fc, AOI, saveout)

#Add the percent inside field
arcpy.AddField_management(saveout,"Percent_Inside", "Short")
#Calculation for percent in field
calc = "((!GEOMETRY_Area!/!FEATURE_AREA_SQM!)*100)"
type = "PYTHON_9.3"
#Run the calculation
arcpy.CalculateField_management(saveout,"Percent_Inside", calc, type)

#Remove the fields that aren't of interest
#Create a variable list
dropFields = list()  
#get a list of all the fields in the Harvest Authority inside AOI for the Quarter
fieldList = arcpy.ListFields(saveout)     
#Keep the following fields                     
keep_list = ["OBJECTID", "HARVEST_AUTH_STATUS_CODE","FOREST_FILE_ID","CUTTING_PERMIT_ID","ISSUE_DATE","EXPIRY_DATE", "TIMBER_MARK_PRIME", "CLIENT_NAME","FILE_TYPE_CODE", "FILE_TYPE_DESCRIPTION", "FEATURE_AREA_SQM", "GEOMETRY", "GEOMETRY_Length", "GEOMETRY_Area","Percent_Inside"]  
#Iterate through the list of fields
for f in fieldList:  
	#Add field to the list if it isn't in the keep list
	if f.name not in keep_list and f.type not in keep_list:  
		dropFields.append(f.name)  
		#delete the fields that aren't in the keep list
		arcpy.DeleteField_management(saveout, dropFields)  
#Field are removed 

table_save = name + '_TimberMarks_' + text
arcpy.TableToTable_conversion(saveout, saveloc, table_save)