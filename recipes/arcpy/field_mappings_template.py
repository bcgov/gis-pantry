#Import your required libraries
import arcpy
 
# Set the workspace
arcpy.env.workspace = 'C:\GIS\Fieldmapping_Test.gdb'
 
#Set variables for data
data_file_1 = 'fieldmap_data_1'
data_file_2 = 'fieldmap_data_2'
output_file = 'fieldmap_result'
 
#Create the required FieldMap and FieldMappings objects
#Only a single main fieldmappings object is required
#Aadditonal fieldmap objects are required for each field you want to link
fieldmappings = arcpy.FieldMappings()
fieldmap_A = arcpy.FieldMap()
fieldmap_B = arcpy.FieldMap()
fieldmap_C = arcpy.FieldMap()
 
#----------------------------------------------------------------------------------------------------
 
#Get the field names for the data files
#Use some process to list the fields you want to use
fields_1 = arcpy.ListFields(data_file_1)
fields_2 = arcpy.ListFields(data_file_2)
#Then use some logic to determine which fields you want to match
 
#OR
 
#Manually list them out
Type_1 = "ParcelClass" 
Type_2 = "ParcelType"
 
PIN_1 = "PIN"
PIN_2 = "PIN_SID"
 
Legal_1 = "LegalDescription"
Legal_2 = "ParcelDescription"
 
#----------------------------------------------------------------------------------------------------
 
#Add fields to their corresponding FieldMap objects
#You are adding sets of data together to a single fieldmap object
#The source data file and the field name from that file that you want to link
#Then the other data file and its corresponding field name
fieldmap_A.addInputField(data_file_1, Type_1)
fieldmap_A.addInputField(data_file_2, Type_2)
 
#Continue with all of the fieldmaps you want to create.
#Each field map object is one link between the files.
fieldmap_B.addInputField(data_file_1, PIN_1)
fieldmap_B.addInputField(data_file_2, PIN_2)
 
#You can have as many links as you want
fieldmap_C.addInputField(data_file_1, Legal_1)
fieldmap_C.addInputField(data_file_2, Legal_2)
 
#----------------------------------------------------------------------------------------------------
 
# Optional, set new names for the output fields.
# If you do not do this step the output fields will take the names from the first datafile

# If I recall, the syntax here has to do with the fact that we are working with objects and their
# properties not simple variables.
# So you have to get a new outputField object from the current one, and then change it's properties.
# To finish you set the fieldMap object's outputField property. If you don't, then nothing changes!
 
# Set properties of the first output name
field_name = fieldmap_A.outputField # get(create) the outputField object you will modify from the fieldmap_A object...
field_name.name = 'Parcel' # set its name property
field_name.aliasName = 'Parcel' # set its alias property
fieldmap_A.outputField = field_name # now set fieldmap_A outputField property to the modified one...
 
# Set properties of the second output name
field_name = fieldmap_B.outputField
field_name.name = 'PIN'
field_name.aliasName = 'PIN'
fieldmap_B.outputField = field_name
 
# Set properties of the third output name
field_name = fieldmap_C.outputField
field_name.name = 'Legal'
field_name.aliasName = 'Legal'
fieldmap_C.outputField = field_name
 
#----------------------------------------------------------------------------------------------------
 
#Finally add the field map objects back into the main field mappings object
fieldmappings.addFieldMap(fieldmap_A)
fieldmappings.addFieldMap(fieldmap_B)
fieldmappings.addFieldMap(fieldmap_C)
 
#----------------------------------------------------------------------------------------------------
 
#Run your merge!
arcpy.Merge_management([data_file_1, data_file_2], output_file, fieldmappings)