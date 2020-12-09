import os  
import arcpy  

input_mxd = arcpy.GetParameterAsText(0)  
#input_mxd = r"\\spatialfiles.bcgov\work\srm\smt\Workarea\ArcProj\P17_Skeena_ESI\Work\11by17_Watershed_DDP 200708.mxd"

folder_output = arcpy.GetParameterAsText(1)
#folder_output = r"\\spatialfiles.bcgov\work\srm\smt\Workarea\ArcProj\P17_Skeena_ESI\Output\Maps\Wetlands\Tier2\2020 Wetland Sampling\Watersheds for Sample Wetlands - Draw 1"
field_name = arcpy.GetParameterAsText(2)
#field_name = r"Watershed_ID"


output_name = arcpy.GetParameterAsText(3)
#output_name = "SSAF_WetlandSample_Watersheds_200819_"
#Combine name 
output = folder_output + "\\" + output_name

#Get the string MXD into an "MXD" format to allow for mxd value
mxd = arcpy.mapping.MapDocument(input_mxd)  

#shorten the feature that will be called a bunch of times
ddp = mxd.dataDrivenPages


for pageNum in range(ddp.pageCount+1):   
	mxd.dataDrivenPages.currentPageID = pageNum 
	
	#pageName = ddp.pageRow.getValue("SSAF 2020 Sample Wetland Complexes.Wetland_Comp_ID")
		
	pageName = ddp.pageRow.getValue(field_name)  
		
	arcpy.mapping.ExportToJPEG(mxd, output + pageName + ".jpg")  

del mxd 