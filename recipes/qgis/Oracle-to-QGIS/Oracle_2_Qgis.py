''' 
AUTHOR: Evan Lavine 
Date  : 04-07-2019 
Arguments: None
Outputs: QGIS Vector Layer(s)
Dependencies: Python3, QGIS3.4 
---------------------------------------------- 
'''

import json
import getpass

# --------------- QGIS IMPORTS BLOCK ----------------------------------------
import os
import sys
sys.path.append(r'E:\sw_nt\QGIS_3.4\apps\qgis\python')
sys.path.append(r'E:\sw_nt\QGIS_3.4\apps\Python37\Lib\site-packages')
os.environ['PATH'] += r";E:\sw_nt\QGIS_3.4\apps\qgis\bin;E:\sw_nt\QGIS_3.4\apps\qgis\bin;E:\sw_nt\QGIS_3.4\apps\Qt5\bin;"
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r'E:\sw_nt\QGIS_3.4\apps\Qt5\plugins'
os.environ['QT_PLUGIN_PATH'] = r'E:\sw_nt\QGIS_3.4\apps\qgis\qtplugins;E:\sw_nt\QGIS_3.4\apps\qt5\plugins'
if 'PYTHONPATH' in os.environ:
    os.environ['PYTHONPATH'] += r'E:\sw_nt\QGIS_3.4\apps\qgis\python'
else:
    os.environ['PYTHONPATH'] = r'E:\sw_nt\QGIS_3.4\apps\qgis\python'
os.environ['PYTHONHOME'] = r'E:\sw_nt\QGIS_3.4\apps\Python37'
from qgis.core import *
QgsApplication.setPrefixPath(r'E:\sw_nt\QGIS_3.4\apps\qgis', True)
qgs = QgsApplication([], False)
qgs.initQgis()
# if using processing tools do this
sys.path.append(r'E:\sw_nt\QGIS_3.4\apps\qgis\python\plugins')
from processing.core.Processing import Processing
import processing
from qgis.analysis import QgsNativeAlgorithms
Processing.initialize()
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
feedback = QgsProcessingFeedback()
# --------------- END QGIS IMPORTS ----------------------------------------


'''
#---------------------------Class o2q Description------------------------------ 
The purpose of this class is to improve efficiencies of simple geoprocessing function in Qgis (Q).
The BC government warehouse contains large tables that congest processing when brought into Q.
This class reduces the table size through the use of SQL statements. Q layers are then produced 
and can be used or exported based on user preferences.  

Processes include:
    i) Select By Location 
        - Completely Within 
        - Intersect
    ii) Select By Attribute
    iii) Union
    iv) Intersection

#------------------------------------------------------------------------------ 
'''

class o2q:
    # JSON_FILE: Contains information about most layers in the BCGW
    json_file = r'W:\FOR\RSI\DKL\General_User_Data\elavine\projects\Lands\Scripts\layer_dict.json'
    

    # INIT METHOD: sets up the oracle database connection and Qgis instance
    def __init__(self, database, host, user, port, password):
        self.project = QgsProject.instance()
        self.tc_root = self.project.layerTreeRoot()
        self.db = database
        self.host = host
        self.port = port
        self.user = user
        self.password = password
    

    # SELECT_BY_ATTRIBUTE METHOD: returns a qgis vector layer using an sql query on a single dataset 
        # INPUTS:   data = schema.table
        #           datawc = sql statment ie fieldname = 'value'
    def select_by_attribute(self, data, datawc):
        if datawc != '':
            datawc = ' where ' + datawc
        sql = "(select * from {}  {} )".format(data, datawc)
        return self.__build_layer(data, sql)
    

    # SELECT_BY_LOCATION METHOD: returns a QGIS vector layer by defining the type of overlay and calls the method for building the overlay                                
        # INPUTS:   data1/2 = schema.table
        #           datawc = sql statment ie fieldname = 'value'
        #           overlay_type = 'Completely Within' or 'Intersect' 
    def select_by_location(self, data1, data2, data1wc, data2wc, overlay_type):
        if overlay_type == 'Completely Within':
            return self.__inside(data1, data2, data1wc, data2wc)
        elif overlay_type == 'Intersect':
            return self.__anyinteract(data1, data2, data1wc, data2wc)
   

    # __INSIDE METHOD:  internal method that returns an sql statement based on an oracle SDO_RELATE spatial operation 
    #                   INSIDE selects features from DATA1 that are fully within the defined features of DATA2                               
        # INPUTS:   data1 = Feature being selected (schema.table)
        #           data2 = Features defining the selection (schema.table)
        #           datawc = sql statment ie fieldname = 'value'    
    def __inside(self, data1, data2, data1wc, data2wc):
            data1wc, data2wc = self.__whereclauses(data1wc, data2wc)         
            sql = "(select * from {0}  where {4} sdo_INSIDE({2},  (select {3}  from {1} {5})) = 'TRUE')".format(data1, data2, self.__get_geomcolumn(data1), self.__get_geomcolumn(data2), data1wc, data2wc)
            return self.__build_layer(data1, sql)
   
   
    # __ANYINTERACT METHOD: internal method that returns an sql statement based on an oracle SDO_RELATE spatial operation                                 
    #                       ANYINTERACT selects features from DATA1 that intersect the defined features of DATA2     
        # INPUTS:   data1 = Feature being selected (schema.table)
        #           data2 = Features defining the selection (schema.table)
        #           datawc = sql statment ie fieldname = 'value'                 
    def __anyinteract(self, data1, data2, data1wc, data2wc):
        data1wc, data2wc = self.__whereclauses(data1wc, data2wc)
        sql = "(select * from {0}  where {4} sdo_ANYINTERACT({2},  (select {3}  from {1} {5})) = 'TRUE')".format(data1, data2, self.__get_geomcolumn(data1), self.__get_geomcolumn(data2), data1wc, data2wc)
        return self.__build_layer(data1, sql)
    
    
    # __WHERECLAUSES METHOD: internal method that returns a transformed whereclauses 
        # INPUTS:   datawc = sql statment ie fieldname = 'value'  
    def __whereclauses(self, datawc1, datawc2):
            if datawc1 != '':
                datawc1 = datawc1 + ' and '
            if datawc2 != '':
                datawc2 = ' where ' + datawc2       
            return datawc1, datawc2 
    
    
    # __BUILD_LAYER METHOD: internal method that returns a built QGIS vector layer 
    #                       NOTE: Method assumes paramaters based on BCGW datasets 
        # INPUTS:   data1 = schema.table
        #           sql = sql statements that were formed in any of the above methods  
    def __build_layer(self, data1, sql):
        uri = QgsDataSourceUri()        
        uri.setConnection(self.host, self.port, self.db, self.user, self.password)
        uri.setDriver('oracle')
        uri.setSrid('3005')
        uri.setUseEstimatedMetadata(True)
        uri.setKeyColumn('OBJECTID') 
        uri.setDataSource( "", sql, self.__get_geomcolumn(data1), "", "OBJECTID")
        uri.setWkbType(int('{}'.format(getattr(QgsWkbTypes, self.__get_geomtype(data1)))))
        n_layer = QgsVectorLayer(uri.uri(), self.__get_layernm(data1), 'oracle')
        return n_layer 
   
   
    # __GET_GEOMTYPE METHOD: internal method that determines the geometry type of a dataset ie Polygon, Point, LineString
        # INPUTS:   data = schema.table    
    def __get_geomtype(self, datasource):
        with open(self.json_file) as jf:
            data = json.load(jf)
            for j in data: 
                dsource = str(j['data_source']) 
                if datasource == dsource:
                    geom = str(j['layerGeometryType'])
                    self.geomT = geom
                    return self.geomT
   
   
    # __GET_GEOMCOLUMN METHOD: internal method that determines the geometry column of a dataset ie SHAPE, GEOMETRY
        # INPUTS:   data = schema.table     
    def __get_geomcolumn(self, datasource):
        with open(self.json_file) as jf:
            data = json.load(jf)
            for j in data: 
                dsource = str(j['data_source']) 
                if datasource == dsource:
                    geom = str(j['layerGeometryColumn'])
                    self.geomC =  geom    
                    return self.geomC    
    
    
    # __GET_LAYERNM METHOD: internal method that determines an appropriate vector layer name
        # INPUTS:   data = schema.table
    def __get_layernm(self, datasource):
        with open(self.json_file) as jf:
            data = json.load(jf)
            for j in data: 
                dsource = str(j['data_source']) 
                if datasource == dsource:
                    nm = str(j['layerDisplayName'])
                    self.nm = nm
                    return self.nm        
    
    
    # UNION METHOD: method returns a built QGIS vector layer that is a union of two layers
    #               two layers must have some overlap  
        # INPUTS:   layer1/2 = must be qgis layers
    def union(self, layer1, layer2):
        u_layer = (processing.run("native:union", {'INPUT': layer1,'OVERLAY': layer2,'OUTPUT':'memory:'})).get('OUTPUT')
        return u_layer
   
   
    # INTERSECTION METHOD: method returns a built QGIS vector layer that is an intersection of two Polygon layers
    #               two layers must have some overlap
    #               fields can be reduced to what user's interest area... default is all fields by using the listfields method which returns the list of fields
        # INPUTS:   layer1/2 = must be qgis layers and both be polygons
    def intersection(self, layer1, layer2):
        i_layer = (processing.run("native:intersection", {'INPUT': layer1,'OVERLAY': layer2, 'INPUT_FIELDS':self.__listFields(layer1),'OVERLAY_FIELDS':self.__listFields(layer2), 'OUTPUT':'memory:'})).get('OUTPUT')
        return i_layer
   
   
    # LINE_INTERSECTION METHOD: method returns a built QGIS vector layer that is an intersection of two Line layers
    #               two layers must have some overlap 
        # INPUTS:   layer1/2 = must be qgis layers and both be lines
    def line_intersection(self, layer1, layer2):
        l_i_layer = (processing.run("native:splitwithlines", {'INPUT': layer1, 'LINES': layer2, 'OUTPUT':'memory:'})).get('OUTPUT')
        return l_i_layer
   
   
    # __LISTFIELDS METHOD: internal method that returns a list of all the fields in a layer except for 'SE_ANNO_CAD_DATA'           
        # INPUTS:   oracle_source = can either be a QGIS vector layer or a schema.table from BCGW
    def __listFields(self, oracle_source):
        try:
            oracle_source.isValid()
            flist = [f.name() for f in oracle_source.fields()]
            flist.remove('SE_ANNO_CAD_DATA')
        except: 
            print('yup')
            uri = QgsDataSourceUri()
            uri.setConnection(self.host, self.port,self.db, self.user, self.password)
            schema, table = oracle_source.split('.')
            uri.setDataSource(schema, table, self.__get_geomcolumn(oracle_source))       
            uri.setSrid('3005')
            if oracle_source == 'WHSE_FOREST_VEGETATION.VEG_COMP_LYR_R1_POLY':
                uri.setKeyColumn('OBJECT_ID')  
            else:
                uri.setKeyColumn('OBJECTID')  
            uri.setUseEstimatedMetadata(True)
            #make the layer
            vlayer = QgsVectorLayer(uri.uri(), 'temp_layer', 'oracle')
            assert vlayer.isValid()
            flist = [f.name() for f in vlayer.fields()]
            flist.remove('SE_ANNO_CAD_DATA')            
        return flist

if __name__ == "__main__":
    #example POLYGON ON POLYGON
        #varaible set up
    data1 = "WHSE_CADASTRE.CBM_CADASTRAL_FABRIC_PUB_SVW"
    data1wc = "FEATURE_AREA_SQM > 100000"
    data2 = "WHSE_ADMIN_BOUNDARIES.EBC_PROV_ELECTORAL_DIST_SVW"
    data2wc = "ED_ABBREVIATION = 'KLW'"
    database = 'db name'
    host = 'host name'
    user = 'user name'
    port = 'port number'
    password = '********'
    overlay = 'Completely Within'
        #define an object to the class
    test = o2q(database, host, user, port, password) #sets up database connection and object
        # first layer will be created using a select by location where the features in data1 must be fully inside data2 
    within = test.select_by_location(data1, data2, data1wc, data2wc, overlay)   
        # second layer will be created using a simple select by attribute to define the area of interest
    aoi = test.select_by_attribute(data2, data2wc)
        # create an intersected vector layer where the output has all the tables 
    a = test.intersection(within, aoi)
    QgsProject.instance().addMapLayer(a)
        # create a union vector layer from the two layers 
    b = test.union(within, aoi)
    QgsProject.instance().addMapLayer(b)


    #example LINE ON LINE
        #varaible set up
    data1 = "WHSE_BASEMAPPING.TRIM_TRANSPORTATION_LINES"
    data1wc = "FEATURE_LENGTH_M > 1000"
    data2 = "WHSE_ADMIN_BOUNDARIES.EBC_PROV_ELECTORAL_DIST_SVW"
    data2wc = "ED_ABBREVIATION = 'KLW'"
    data3 = "WHSE_BASEMAPPING.NTS_BC_WATER_LINES_125M"
    data3wc = ""
    database = 'db name'
    host = 'host name'
    user = 'user name'
    port = 'port number'
    password = '********'
    overlay = 'Intersect'
        #define an object to the class
    test = o2q(database, host, user, port, password) #sets up database connection and object
        # layers will be created using a select by location where the features in the first parameter must be fully inside features in the second parameter 
    within = test.select_by_location(data1, data2, data1wc, data2wc, overlay)    
    within2 = test.select_by_location(data3, data2, data3wc, data2wc, overlay)   
        # create an intersected vector layer where the second layer (within2) will define the intersection breaks
    a = test.line_intersection(within, within2)
    QgsProject.instance().addMapLayer(a)
        # create a union vector layer from the two layers 
    b = test.union(within, within2)
    QgsProject.instance().addMapLayer(b)
