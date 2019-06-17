'''
AUTHOR: Will Burt 
Date  : 06-13-2019
Arguments: None
Outputs: print statement of process
Dependancies: Python3, QGIS

History:
----------------------------------------------

'''


import os
import sys
from time import time

# --------------- QGIS IMPORTS BLOCK Adjust the QGIS INSTALL PATH AS NEEDED------
sys.path.append(r'C:\Program Files\QGIS 3.4\apps\qgis\python')
sys.path.append(r'C:\Program Files\QGIS 3.4\apps\Python37\Lib\site-packages')
os.environ['PATH'] += r";C:\Program Files\QGIS 3.4\apps\qgis\bin;C:\Program Files\QGIS 3.4\apps\qgis\bin;C:\Program Files\QGIS 3.4\apps\Qt5\bin;"
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r'C:\Program Files\QGIS 3.4\apps\Qt5\plugins'
os.environ['QT_PLUGIN_PATH'] = r'C:\Program Files\QGIS 3.4\apps\qgis\qtplugins;C:\Program Files\QGIS 3.4\apps\qt5\plugins'
if 'PYTHONPATH' in os.environ:
    os.environ['PYTHONPATH'] += r'C:\Program Files\QGIS 3.4\apps\qgis\python'
else:
    os.environ['PYTHONPATH'] = r'C:\Program Files\QGIS 3.4\apps\qgis\python'

os.environ['PYTHONHOME'] = r'C:\Program Files\QGIS 3.4\apps\Python37'
from qgis.core import *
QgsApplication.setPrefixPath(r'C:\Program Files\QGIS 3.4\apps\qgis', True)
qgs = QgsApplication([], False)
qgs.initQgis()
# if using processing tools do this
sys.path.append(r'C:\Program Files\QGIS 3.4\apps\qgis\python\plugins')

from qgis.core import QgsDataSourceUri
from processing.core.Processing import Processing
import processing
from qgis.analysis import QgsNativeAlgorithms

Processing.initialize()
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
feedback = QgsProcessingFeedback()
# --------------- END QGIS IMPORTS ----------------------------------------
print ('starting some benchmarks')
start_time = time()
#some bounding box within BC-Albers minX,maxX,minY,maxY
extent = '1320000,1565000,617000,753000'
#Params for random point generation
params = { 
    'EXTENT' : extent,
    'MIN_DISTANCE' : 0,
    'OUTPUT' : 'memory:', 
    'POINTS_NUMBER' : 1500, 
    'TARGET_CRS' : QgsCoordinateReferenceSystem('EPSG:3005') 
    }
    
feedback = QgsProcessingFeedback()
#run random points processing tool
res = processing.run("qgis:randompointsinextent",params, feedback=feedback)

#params for calculation of distance between all points
params = { 
    'INPUT' : res['OUTPUT'],
    'INPUT_FIELD' : 'id', 
    'MATRIX_TYPE' : 0, 
    'NEAREST_POINTS' : 0, 
    'OUTPUT' : 'memory:', 
    'TARGET' : res['OUTPUT'], 
    'TARGET_FIELD' : 'id' }
n_res = processing.run("qgis:distancematrix",params,feedback=feedback)

#calculate some voronoi polygons
params = {
    'INPUT':res['OUTPUT'],
    'BUFFER':0,
    'OUTPUT':'memory:'}
v_res = processing.run("qgis:voronoipolygons", params, feedback=feedback)

#finished
print (f'test complete in {round(time()-start_time,1)} seconds')