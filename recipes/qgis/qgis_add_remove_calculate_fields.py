'''
AUTHOR: Mark McGirr
Date  : 06-05-2019
Arguments: None
Outputs: None
Dependancies: 

History:
----------------------------------------------
'''


import os
import sys
import set_qgis_environment


from PyQt5.QtCore import *


#------------------------------------------------------
# With path set, import QGIS3
from qgis.core import *
#------------------------------------------------------



#------------------------------------------------------
# Initialize the app or QGIS3 will crash
QgsApplication.setPrefixPath("qgis_root + '/' + '/apps/qgis", True)
app = QgsApplication([], False)
app.initQgis()
#------------------------------------------------------



#------------------------------------------------------
# Initialize processing and add native tools
from qgis.analysis import QgsNativeAlgorithms
sys.path.append('E:/sw_nt/QGIS_3.4/apps/qgis/python/plugins')
import processing  # processing causes psycopg2-binary warning
from processing.core.Processing import Processing
Processing.initialize()
app.processingRegistry().addProvider(QgsNativeAlgorithms())
#------------------------------------------------------







def add_fields_to_geopackage():

    # create layer of featureclass to run against
    fc_input = r'../script_output_data/alexis.gpkg'
    fc_input_layer = QgsVectorLayer(fc_input, '', 'ogr')
    
    # build list of all field names that exist in the FC.  convert them all to lower so I don't have to worry about upper or lower case.
    existing_fields = []
    for field in fc_input_layer.fields():
        existing_fields.append(field.name().lower())
    
    
    field_to_add = "mm_integer"
    if existing_fields.count(field_to_add.lower())== 0:
        print ('cant_find_field',field_to_add, ' so adding it')
        fc_input_layer.dataProvider().addAttributes([QgsField(field_to_add, QVariant.Int)])
    else:
        print(field_to_add , "already exists")

    
    field_to_add = "mm_text"
    if existing_fields.count(field_to_add.lower())== 0:
        print ('cant_find_field',field_to_add, ' so adding it')
        fc_input_layer.dataProvider().addAttributes([QgsField(field_to_add, QVariant.String)])
    else:
        print(field_to_add , "already exists")
    
    
    field_to_add = "area_ha"
    if existing_fields.count(field_to_add.lower())== 0:
        print ('cant_find_field',field_to_add, ' so adding it')
        fc_input_layer.dataProvider().addAttributes([QgsField(field_to_add, QVariant.Double)])
    else:
        print(field_to_add , "already exists")
    
    
    #------------------------------------------------------------------------------ 
    




def calculate_values_for_fields():
    # create layer of featureclass to run against
    fc_input = r'../script_output_data/alexis.gpkg'
    fc_input_layer = QgsVectorLayer(fc_input, '', 'ogr')
    
    
    # add a field so that I can calculate a value into it
    field_to_add = "just_the_letter"
    fc_input_layer.dataProvider().addAttributes([QgsField(field_to_add, QVariant.String)])
    
    # need to specify the numerical position of the field
    field_index_potition = fc_input_layer.fields().indexFromName(field_to_add) 
    
    # select a subset of the records to calculate values for
    selected_records = fc_input_layer.getFeatures(QgsFeatureRequest().setFilterExpression(u' "Assessment_Unit_Name" like \'%_A\' '))
    

    
    #------------------------------------------------------------------------------ 
    #open the FC for editing, calculate the values for selected records, and commit the changes.
 
    fc_input_layer.startEditing()
    
    for feat in selected_records:
      fc_input_layer.changeAttributeValue(feat.id(), field_index_potition, "A")
    
    fc_input_layer.commitChanges()
    #------------------------------------------------------------------------------ 
    
    





def remove_fields_from_geopackage():
 
    # create layer of the featureclass to run against
    fc_input = r'../script_output_data/alexis.gpkg'
    fc_input_layer = QgsVectorLayer(fc_input, '', 'ogr')
    
    
    # build list of all fields currently in the input layer
    list_of_fields = []
    for field in fc_input_layer.fields():
        list_of_fields.append(field.name())
    

    # build list of fields we want to keep
    fields_to_keep = []
    fields_to_keep.append('Assessment_Unit_Group')
    fields_to_keep.append('Assessment_Unit_Name')
    fields_to_keep.append('just_the_letter')
    

    # create final list of fields we want to remove.  We need to get the position index of these fields too.
    fields_to_delete = list((set(list_of_fields)-set(fields_to_keep)))
    fields_to_delete_position_index = []
    for x in fields_to_delete:
        field_index_potition = fc_input_layer.fields().indexFromName(x)
        fields_to_delete_position_index.append(field_index_potition)



    # delete the fields, and commit the changes
    fc_input_layer.dataProvider().deleteAttributes(fields_to_delete_position_index)
    fc_input_layer.updateFields()
    fc_input_layer.commitChanges()
    
 
    #------------------------------------------------------------------------------ 
    
    
    
============================================================

#add_fields_to_geopackage()
#calculate_values_for_fields()
remove_fields_from_geopackage()



#------------------------------------------------------
# exit from qgis
app.exitQgis()
#------------------------------------------------------


print ("############             FINISHED      #################")




