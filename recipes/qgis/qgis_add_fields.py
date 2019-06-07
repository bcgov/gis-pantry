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
#from PyQt5.QtCore import QVariant


#------------------------------------------------------
# With path set, import QGIS3
from qgis.core import *
#from qgis.core import QgsApplication, QgsProcessingFeedback, QgsVectorLayer ,QgsVectorDataProvider,QgsField
#from qgis.PyQt.QtCore import QVariant
#------------------------------------------------------



#------------------------------------------------------
# Initialize the app or QGIS3 will crash
QgsApplication.setPrefixPath("E:/sw_nt/QGIS_3.4/apps/qgis", True)
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





#===============================================================================
# remove field from shape file
#===============================================================================
fc_input = r'../script_output_data/alexis.shp'
fc_input_layer = QgsVectorLayer(fc_input, '', 'ogr')


field_to_delete = 'mytextxx18'

# build list of all fields
list_of_fields = []
for field in fc_input_layer.fields():
    list_of_fields.append(field.name())

if list_of_fields.count(field_to_delete) > 0:
    print ("deleting field " , field_to_delete)
    field_index = list_of_fields.index(field_to_delete)
    fc_input_layer.dataProvider().deleteAttributes([field_index])
else:
    print ('could not find field to delete it')
#------------------------------------------------------------------------------ 






#===============================================================================
# add INT field to geo package
#===============================================================================
fc_input = r'../script_output_data/alexis.gpkg'
fc_input_layer = QgsVectorLayer(fc_input, '', 'ogr')

# build list of all field names that exist in the FC.  convert them all to lower so I don't have to worry about upper or lower case.
existing_fields = []
for field in fc_input_layer.fields():
    print (field.name().lower())
    existing_fields.append(field.name().lower())


field_to_add = "xxxyyy"
if existing_fields.count(field_to_add.lower())== 0:
    print ('cant_find_field',field_to_add, ' so adding it')
    fc_input_layer.dataProvider().addAttributes([QgsField(field_to_add, QVariant.Int)])
else:
    print(field_to_add , "already exists")
#------------------------------------------------------------------------------ 










#===============================================================================
# add STRING field to shape file
#===============================================================================
fc_input = r'../script_output_data/alexis.shp'
fc_input_layer = QgsVectorLayer(fc_input, '', 'ogr')

# build list of all field names that exist in the FC.  convert them all to lower so I don't have to worry about upper or lower case.
existing_fields = []
for field in fc_input_layer.fields():
    print (field.name().lower())
    existing_fields.append(field.name().lower())


field_to_add = "xxxyyy"
if existing_fields.count(field_to_add.lower())== 0:
    print ('cant_find_field',field_to_add, ' so adding it')
    fc_input_layer.dataProvider().addAttributes([QgsField(field_to_add, QVariant.String)])
else:
    print(field_to_add , "already exists")


#outlayer.startEditing()
#new_field_index = outlayer.fieldNameIndex('SUM')
#for f in processing.features(outlayer):
#fc_input_layer.changeAttributeValue(fc_input_layer.id(), "mytext",'bigtest')
selection=fc_input_layer.getFeatures(QgsFeatureRequest().setFilterExpression('"myint"= 15'))
for feat in selection:
  fc_input_layer.changeAttributeValue(feat.id(), 'myint_1', 3)
  #layer.changeAttributeValue(feat.id(), ANB, 3)




#fc_input_layer.changeAttributeValue(fc_input_layer.id(), 'myint_1', 3)

#fc_input_layer.setAttribute(fc_input_layer.fieldNameIndex('mytext'), 'bigtest' )
  #outlayer.changeAttributeValue(f.id(), new_field_index, sum_unique_values[f[dissolve_field]])
#outlayer.commitChanges()


#------------------------------------------------------------------------------ 







#------------------------------------------------------
# exit from qgis
app.exitQgis()
#------------------------------------------------------



print ("############             FINISHED      #################")
