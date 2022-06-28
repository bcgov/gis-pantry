import os
import sys
###############################################
'''
AUTHOR: Mark McGirr
Date  : 06-05-2019
Arguments: None
Outputs: None
Dependancies: need QGIS_PATH in as environment variable
History:
----------------------------------------------
0?-05-2019 - Mark McGirr
    Creation of environment setup for qgis standalone scripts
06-05-2019 - Will Burt
    addition of qgis_root for install path substitutions
07-04-2020 - Will Burt
    move qgis_root to environment variable
15-07-2020 - Will Burt
    allow for difference in ltr installation structure
''' 
###############################################
if 'QGIS_PATH' in os.environ.keys():
    qgis_root = os.environ['QGIS_PATH']
else:
    print("qgis_root not found; exiting script.")
    raise OSError(2,f'Expected envrironment variable "QGIS_PATH" not found')

print("qgis_root is: {}\n".format(qgis_root))

qgis_app_folder = 'qgis'
if not os.path.exists(os.path.join(qgis_root,qgis_app_folder)):
    qgis_app_folder = 'qgis-ltr'
    assert os.path.exists(os.path.join(qgis_root,qgis_app_folder))

# Define plugin locations from QGIS3
sys.path.append(qgis_root + '/' + qgis_app_folder + '/python')
sys.path.append(qgis_root + '/' + qgis_app_folder + '/plugins')
sys.path.append(qgis_root + '/apps/qt5/bin')
sys.path.append(qgis_root + '/' + qgis_app_folder + '/bin')
sys.path.append(qgis_root + '/' + qgis_app_folder + '/python/plugins')

# Define Qt5 plugin path since Qt5 can't find it
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qgis_root + '/apps/Qt5/plugins'  # ;'+qgis_root + '/apps/qgis/qtplugins

# Enviro setup from python-qgis.bat
os.environ['GDAL_DATA'] = qgis_root + '/share/gdal'
os.environ['GDAL_DRIVER_PATH'] = qgis_root + '/bin/gdalplugins'
os.environ['GDAL_FILENAME_IS_UTF8'] = 'YES'
os.environ['GEOTIFF_CSV'] = qgis_root + '/share/epsg_csv'
os.environ['QGIS_PREFIX_PATH'] = qgis_root + '/' + qgis_app_folder
os.environ['QT_PLUGIN_PATH'] = qgis_root + \
    '/' + qgis_app_folder + '/qtplugins;'+qgis_root + '/apps/qt5/plugins'
os.environ['VSI_CACHE'] = 'TRUE'
os.environ['VSI_CACHE_SIZE'] = '1000000'

# Enviro setup from qt5_env.bat
os.environ['QT_PLUGIN_PATH'] = qgis_root + \
    f'/apps/{qgis_app_folder}/qtplugins;'+qgis_root + '/apps/qt5/plugins'
os.environ['O4W_QT_PREFIX'] = qgis_root + '/apps/Qt5'
os.environ['O4W_QT_BINARIES'] = qgis_root + '/apps/Qt5/bin'
os.environ['O4W_QT_PLUGINS'] = qgis_root + '/apps/Qt5/plugins'
os.environ['O4W_QT_LIBRARIES'] = qgis_root + '/apps/Qt5/lib'
os.environ['O4W_QT_TRANSLATIONS'] = qgis_root + '/apps/Qt5/translations'
os.environ['O4W_QT_HEADERS'] = qgis_root + '/apps/Qt5/include'
os.environ['O4W_QT_DOC'] = qgis_root + '/apps/Qt5/doc'

# Enviro setup from py3_env.bat
os.environ['PYTHONPATH'] = qgis_root + f'/apps/{qgis_app_folder}/python;'
os.environ['PYTHONHOME'] = qgis_root + '/apps/Python37'
os.environ['OSGEO4W_ROOT'] = qgis_root + ''

# Mimic path from cmd window after running .bat file
os.environ['Path'] = qgis_root + f'/apps/{qgis_app_folder}/bin;'+qgis_root + '/apps/Python37;'+qgis_root + '/apps/Python37/Scripts;'+qgis_root + \
    '/apps/qt5/bin;'+qgis_root + '/apps/Python27/Scripts;'+qgis_root + \
    '/bin;C:/Windows/system32;C:/Windows;C:/Windows/system32/WBem'

print("\nBoilerplate env OK\n")

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
QgsApplication.setPrefixPath(qgis_root + f'/apps/{qgis_app_folder}', True)      # Extra
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
Processing.initialize()

print(f"Boilerplate ran OK: {sys.argv[0]}")
#===============================================================================
# End of boilerplate
#===============================================================================