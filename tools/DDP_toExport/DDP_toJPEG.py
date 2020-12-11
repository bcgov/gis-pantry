import os  
import arcpy  

input_mxd = arcpy.GetParameterAsText(0)  


folder_output = arcpy.GetParameterAsText(1)

field_name = arcpy.GetParameterAsText(2)



output_name = arcpy.GetParameterAsText(3)

#Combine name 
output = folder_output + "\\" + output_name

#Get the string MXD into an "MXD" format to allow for mxd value
mxd = arcpy.mapping.MapDocument(input_mxd)  

#shorten the feature that will be called a bunch of times
ddp = mxd.dataDrivenPages


for pageNum in range(ddp.pageCount+1):   
	mxd.dataDrivenPages.currentPageID = pageNum 
	

		
	pageName = ddp.pageRow.getValue(field_name)  
		
	arcpy.mapping.ExportToJPEG(mxd, output + pageName + ".jpg")  

del mxd 