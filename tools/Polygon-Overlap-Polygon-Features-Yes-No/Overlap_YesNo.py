#A tool to state whether or not one polygon (input) overlaps another polygon with a Yes/No statement
#Written by Jesse Fraser (jesse.fraser@gov.bc.ca)
#Started Jan 14th 2020

import time
import numpy
arcpy.env.overwriteOutput = True

time = time.strftime("%Y%m%d")

#connect to BCGW
BCGW = r'Database Connections\BCGW4Scripting.sde'
#Get the average of the values
#Variables for Toolbox
#The layer to append the Y/N question to
fcName = arcpy.GetParameterAsText(0)

#The layer that will be iterated through to provide Y/N
input = arcpy.GetParameterAsText(1)

#FN field name
field_name= arcpy.GetParameterAsText(2)


#create a def quer for the FN layer
arcpy.MakeFeatureLayer_management(input, "lyr_Overlap")
lyr_Overlap = arcpy.mapping.Layer("lyr_Overlap")

#Get the name of lyr_Overlap to use in the query
desc = arcpy.Describe(lyr_Overlap)
lyr_Overlap_name = desc.name
#create an FID based on the name of the input layer, and union FID output
quer_field = "FID_" + lyr_Overlap_name



#populate a list of fields
#Get a list of fields
all_fields = [f.name for f in arcpy.ListFields(lyr_Overlap)]
DontDeleteFields = ["Shape_Area", "Shape_Length", "GEOMETRY_Area", "GEOMETRY_Length", "Shape", "OBJECTID"]
delete_fields = list(set(all_fields) - set(DontDeleteFields))
AnnoyingFields = ("Shape_Area_1", "Shape_Length_1", "GEOMETRY_Area_1", "GEOMETRY_Length_1","Join_Count_1","TARGET_FID_1")
delete_fields =  list(set(delete_fields)|set(AnnoyingFields))
num = 0
with arcpy.da.UpdateCursor(lyr_Overlap, [field_name]) as cursor:
	for test in cursor:
		
		print num
		
		
		''' Not Needed 2020/01/20
		#set variable that matches the two layers together
		matcher = test[0]
		#print matcher
		'''
		
		div = str(num)
		old_union_num = str(num-1)
		#print str(test[0])
		#From Original ESI work.  Wet'suwet'en sets of the query issue because it is spelt different ways different places.
		if test[0] == "Wet'suwet'en First Nation":
			lyr_Overlap.definitionQuery = field_name+ r" = 'Wet''suwet''en First Nation'"
		
		elif test[0] == r"Office of the Wet'suwet'en":
			lyr_Overlap.definitionQuery = field_name+ r" = 'Office of the Wet''suwet''en'"
		
		else:
			lyr_Overlap.definitionQuery = field_name+ " = \'" + test[0] +"\'"
		
		
		
		#Testing break
		#break
		
		if num > 0:
			output_union = fcName + "_" + div
			input_union = fcName + "_" + old_union_num
			arcpy.SpatialJoin_analysis(input_union, lyr_Overlap, output_union)
					
			new_field = test[0] + "_YesNo"
			
			arcpy.AddField_management(output_union, new_field, "TEXT")
			arcpy.MakeFeatureLayer_management(output_union, "lyr_union")
			lyr_union = arcpy.mapping.Layer("lyr_union")
			
			#list of all the field names
			field_names = [f.name for f in arcpy.ListFields(lyr_union)]
			#last field name which is the field that has just been added
			prop_field = field_names[-1]
			
			#This one may not work - Need to figure out a way to get the actual name of the layer rather than the whole file path
			#probably need an operator w/ num value to field_name
			
			#Testing Break
			#break
									
			#populate the fields that overlap Interest Layer
			if test[0] == "Wet'suwet'en First Nation":
				lyr_union.definitionQuery = field_name+ " = \'Wet\'\'suwet\'\'en First Nation\'"
			elif test[0] == "Office of the Wet'suwet'en":
				lyr_union.definitionQuery = field_name+ " = \'Office of the Wet\'\'suwet\'\'en\'"
			else:
				lyr_union.definitionQuery = field_name+ " = \'" + test[0] +"\'"
			
			arcpy.CalculateField_management(lyr_union, prop_field, "\"Yes\"", "PYTHON_9.3")
			
			#Populate fields that don't overlap Interest Layer
			lyr_union.definitionQuery = field_name+ " IS NULL "
			arcpy.CalculateField_management(lyr_union, prop_field, "\"No\"", "PYTHON_9.3")
			
			#Take the def query off to delete useless stuff
			lyr_union.definitionQuery = ""
			
			#Remove until the issue with None is figured out
			arcpy.DeleteField_management(output_union, delete_fields)				
		
			#Test without this - It works without KEEP EXCLUDED
			#arcpy.DeleteFeatures_management(lyr_union)
		
			lyr_Overlap.definitionQuery = ""
			
			
			arcpy.DeleteFeatures_management(input_union)
			
			
			num = num+1
			
						
		
		else:
			output_union = fcName + "_" + div
			arcpy.SpatialJoin_analysis(fcName, lyr_Overlap, output_union)
			
			
						
			new_field = test[0] + "_YesNo"
			arcpy.AddField_management(output_union, new_field, "TEXT")
			arcpy.MakeFeatureLayer_management(output_union, "lyr_union")
			lyr_union = arcpy.mapping.Layer("lyr_union")
			
			
			
			#list of all the field names
			field_names = [f.name for f in arcpy.ListFields(lyr_union)]
			#last field name which is the field that has just been added
			prop_field = field_names[-1]
			
			#This one may not work - Need to figure out a way to get the actual name of the layer rather than the whole file path
			
			#test via print variables
			#print matcher
			#print quer_field
			
			#Testing Break
			#break
			
			#populate the fields that overlap Interest Layer
			if test[0] == "Wet'suwet'en First Nation":
				lyr_Overlap.definitionQuery = field_name+ r" = 'Wet''suwet''en First Nation'"
		
			elif test[0] == r"Office of the Wet'suwet'en":
				lyr_Overlap.definitionQuery = field_name+ r" = 'Office of the Wet''suwet''en'"
				
			else:
				lyr_union.definitionQuery = field_name+ " = \'" + test[0] +"\'"
				
			arcpy.CalculateField_management(lyr_union, prop_field, "\"Yes\"", "PYTHON_9.3")
			
			#Populate fields that don't overlap Interest Layer
			lyr_union.definitionQuery = field_name+ " IS NULL "
			arcpy.CalculateField_management(lyr_union, prop_field, "\"No\"", "PYTHON_9.3")
			
			
			#Take the def query off to delete useless stuff
			lyr_union.definitionQuery = ""
		
			#Remove until the issue with None is figured out
			arcpy.DeleteField_management(output_union, delete_fields)				
		
			#Test without this - It works without KEEP EXCLUDED
			#arcpy.DeleteFeatures_management(lyr_union)
		
			
			lyr_Overlap.definitionQuery = ""
		
		
			num = num+1
			
			#Test break
			#break
			''' Old Clunky Code
			with arcpy.da.UpdateCursor(lyr_union, [fn_field, prop_field]) as blah:
				for boring in blah:
					#test via print variables
					#print boring[0]
					#print test[0]
					
					#boring[0] is showing up as None.  Need it to show up as the same as test
					if boring[0] == matcher:
						boring[1] = "Yes"
						blah.updateRow(boring)
						
					else:
						boring[1] = "No"
						blah.updateRow(boring)
		
		#Take the def query off to delete useless stuff
		lyr_union.definitionQuery = ""
		
		#Remove until the issue with None is figured out
		arcpy.DeleteField_management(lyr_union, delete_fields)				
		
		arcpy.DeleteFeatures_management(lyr_union)
		
		lyr_Overlap.definitionQuery = ""
		
		
		num = num+1		
			'''
output_final = fcName + "_last_" + time

arcpy.CopyFeatures_management(lyr_union, output_final)	

final_2 = ["Join_Count", "TARGET_FID"]
arcpy.DeleteField_management(output_union, final_2)		
