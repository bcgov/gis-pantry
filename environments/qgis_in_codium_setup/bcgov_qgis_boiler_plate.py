#===============================================================================
# Boiler Plate stuff
#===============================================================================
# bcgov_qgis_boiler_plate can be used to set up the QGIS python environment for 
# standalone Python 3 scripts or applications
# author: Mark McGirr, Will Burt
# date: May 17,2021
# usage: start python using the python package installed with QGIS and import this
# module
# requires: Environment Variable QGIS_PATH (this is already set up in BCGOV GTS server environments)
# that shows install path of QGIS

# edits:
# 2021-07-29 Add python dir changes for 3.16.8 + change from python 3.7 to python 3.9

import os, sys

# set up QGIS environment
realpath = os.path.dirname(os.path.realpath(sys.argv[0])) # adds the folder this script sits in to the system path variables
if realpath not in os.path.split(';'):
    sys.path.append(realpath)

# Set correct QGIS root (they are slightly different on Geospatial desktop and Arcgis 10-6 desktop)
if os.path.exists(os.environ['QGIS_PATH']):
    qgis_root = os.environ['QGIS_PATH']
else:
    print("qgis_root not found; exiting script.")
    sys.exit()
print("qgis_root is: {}\n".format(qgis_root))

# Detect python folder
python_dir = None
apps_dir = os.path.join(qgis_root,'apps')
for d in os.listdir(apps_dir):
    if os.path.isdir(os.path.join(apps_dir,d)) and 'PYTHON' in d.upper():
        if d.upper() != 'PYTHON27':
            python_dir = d
if python_dir is None:
    print ("qgis_root PYTHYON not found; exiting script")
    sys.exit()

# Define plugin locations from QGIS3
if os.path.exists(qgis_root + '/apps/qgis'):
    sys.path.append(qgis_root + '/apps/qgis/python')
else:
    sys.path.append(qgis_root + '/apps/qgis-ltr/python')
if os.path.exists(qgis_root + '/apps/qgis'):
    sys.path.append(qgis_root + '/apps/qgis/plugins')
else:
    sys.path.append(qgis_root + '/apps/qgis-ltr/plugins')
sys.path.append(qgis_root + '/apps/qt5/bin')
if os.path.exists(qgis_root + '/apps/qgis'):
    sys.path.append(qgis_root + '/apps/qgis/bin')
else:
    sys.path.append(qgis_root + '/apps/qgis-ltr/bin')
# sys.path.append(r'E:\sw_nt\Python27\ArcGIS10.3\Lib')
if os.path.exists(qgis_root + '/apps/qgis'):
    sys.path.append(qgis_root + '/apps/qgis/python/plugins')
else:
    sys.path.append(qgis_root + '/apps/qgis-ltr/python/plugins')
# Define Qt5 plugin path since Qt5 can't find it
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qgis_root + '/apps/Qt5/plugins'  # ;'+qgis_root + '/apps/qgis/qtplugins

# Enviro setup from python-qgis.bat
# gdal.bat
os.environ['GDAL_DATA'] = qgis_root + '/share/gdal'
os.environ['GDAL_DRIVER_PATH'] = qgis_root + '/bin/gdalplugins'
os.environ['GDAL_FILENAME_IS_UTF8'] = 'YES'
# libgeotiff.bat
os.environ['GEOTIFF_CSV'] = qgis_root + '/share/epsg_csv'
# libjpeg.bat
os.environ['JPEGMEM']='1000000'
# projlib.bat
os.environ['PROJ_LIB']= os.path.join(qgis_root,'share','proj')
if os.path.exists(qgis_root + '/apps/qgis'):
    os.environ['QGIS_PREFIX_PATH'] = qgis_root + '/apps/qgis'
else:
    os.environ['QGIS_PREFIX_PATH'] = qgis_root + '/apps/qgis-ltr'
if os.path.exists(qgis_root + '/apps/qgis'):
    os.environ['QT_PLUGIN_PATH'] = qgis_root + \
        '/apps/qgis/qtplugins;'+qgis_root + '/apps/qt5/plugins'
else:
    os.environ['QT_PLUGIN_PATH'] = qgis_root + \
        '/apps/qgis-ltr/qtplugins;'+qgis_root + '/apps/qt5/plugins'
os.environ['VSI_CACHE'] = 'TRUE'
os.environ['VSI_CACHE_SIZE'] = '1000000'

# Enviro setup from qt5_env.bat
if os.path.exists(qgis_root + '/apps/qgis'):
    os.environ['QT_PLUGIN_PATH'] = qgis_root + \
        '/apps/qgis/qtplugins;'+qgis_root + '/apps/qt5/plugins'
else:
    os.environ['QT_PLUGIN_PATH'] = qgis_root + \
        '/apps/qgis-ltr/qtplugins;'+qgis_root + '/apps/qt5/plugins'
os.environ['O4W_QT_PREFIX'] = qgis_root + '/apps/Qt5'
os.environ['O4W_QT_BINARIES'] = qgis_root + '/apps/Qt5/bin'
os.environ['O4W_QT_PLUGINS'] = qgis_root + '/apps/Qt5/plugins'
os.environ['O4W_QT_LIBRARIES'] = qgis_root + '/apps/Qt5/lib'
os.environ['O4W_QT_TRANSLATIONS'] = qgis_root + '/apps/Qt5/translations'
os.environ['O4W_QT_HEADERS'] = qgis_root + '/apps/Qt5/include'
os.environ['O4W_QT_DOC'] = qgis_root + '/apps/Qt5/doc'

# Enviro setup from py3_env.bat
if os.path.exists(qgis_root + '/apps/qgis'): 
    os.environ['PYTHONPATH'] = qgis_root + '/apps/qgis/python;'
else:
    os.environ['PYTHONPATH'] = qgis_root + '/apps/qgis-ltr/python;'
os.environ['PYTHONHOME'] = qgis_root + '/apps/'+ python_dir
os.environ['OSGEO4W_ROOT'] = qgis_root + ''


# Mimic path from cmd window after running .bat file
if os.path.exists(qgis_root + '/apps/qgis'): 
    os.environ['Path'] = qgis_root + '/apps/qgis/bin;'+qgis_root + '/apps/'+ python_dir+';'+qgis_root + '/apps/'+ python_dir+'/Scripts;'+qgis_root + \
        '/apps/qt5/bin;'+qgis_root + \
        '/bin;C:/Windows/system32;C:/Windows;C:/Windows/system32/WBem'
elif os.path.exists(qgis_root + '/apps/qgis-ltr'):
    os.environ['Path'] = qgis_root + '/apps/qgis-ltr/bin;'+qgis_root + '/apps/'+ python_dir+';'+qgis_root + '/apps/'+ python_dir+'/Scripts;'+qgis_root + \
        '/apps/qt5/bin;'+qgis_root + \
        '/bin;C:/Windows/system32;C:/Windows;C:/Windows/system32/WBem'
else:
    print (f'Oh no! We failed to identify the location of qgis core in:\n {qgis_root}/apps/qgis \n{qgis_root}/apps/qgis-ltr')
    sys.exit()

# Third party imports
from qgis.analysis import QgsNativeAlgorithms # Possible translation: from qgis.py import <class analysis> import <class QgsNativeAlgorithms>
print("from qgis.analysis import QgsNativeAlgorithms... SUCCESS")
from qgis.core import *
print("from qgis.core import *... SUCCESS")
from processing.core.Processing import Processing
print("from processing.core.Processing import Processing... SUCCESS")
import processing
print("import processing... SUCCESS")
from PyQt5.QtCore import *
print("from PyQt5.QtCore import... SUCCESS")
from processing.tools import dataobjects                       # NEW - GMA added
print("from processing.tools import dataobjects... SUCCESS")    # NEW - GMA added
print("All third-party imports OK.")

# Initialize QGIS
feedback = QgsProcessingFeedback()
qgs = QgsApplication([], False)
qgs.initQgis()
# QgsApplication.setPrefixPath(r'E:/sw_nt/QGIS_3.4\apps\qgis', True)      # Extra
if os.path.exists(os.path.join(os.environ['QGIS_PATH'],'apps','qgis')):
    prefix = os.path.join(os.environ['QGIS_PATH'],'apps','qgis')
else:
    prefix = os.path.join(os.environ['QGIS_PATH'],'apps','qgis-ltr')
QgsApplication.setPrefixPath(prefix, True)      # Extra

QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

Processing.initialize()

print("Boilerplate ran OK: {}".format(sys.argv[0]))
#===============================================================================
# End of boilerplate
#===============================================================================