import os
import sys
###############################################
'''
AUTHOR: Mark McGirr
Date  : 06-05-2019
Arguments: None
Outputs: None
Dependancies: 

History:
----------------------------------------------
0?-05-2019 - Mark McGirr
    Creation of environment setup for qgis standalone scripts
06-05-2019 - Will Burt
    addition of qgis_root for install path substitutions
''' 
###############################################
# Set your root QGIS install path
qgis_root = 'E:/sw_nt/QGIS_3.4'

# Define plugin locations from QGIS3
sys.path.append(qgis_root + '/apps/qgis/python')
sys.path.append(qgis_root + '/apps/qgis/plugins')
sys.path.append(qgis_root + '/apps/qt5/bin')


# Define Qt5 plugin path since Qt5 can't find it
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qgis_root + \
    '/apps/Qt5/plugins'  # ;'+qgis_root + '/apps/qgis/qtplugins


# enviro setup from python-qgis.bat
os.environ['GDAL_DATA'] = qgis_root + '/share/gdal'
os.environ['GDAL_DRIVER_PATH'] = qgis_root + '/bin/gdalplugins'
os.environ['GDAL_FILENAME_IS_UTF8'] = 'YES'
os.environ['GEOTIFF_CSV'] = qgis_root + '/share/epsg_csv'
os.environ['QGIS_PREFIX_PATH'] = qgis_root + '/apps/qgis'
os.environ['QT_PLUGIN_PATH'] = qgis_root + \
    '/apps/qgis/qtplugins;'+qgis_root + '/apps/qt5/plugins'
os.environ['VSI_CACHE'] = 'TRUE'
os.environ['VSI_CACHE_SIZE'] = '1000000'

# enviro setup from qt5_env.bat
os.environ['QT_PLUGIN_PATH'] = qgis_root + \
    '/apps/qgis/qtplugin;'+qgis_root + '/apps/qt5/plugins'
os.environ['O4W_QT_PREFIX'] = qgis_root + '/apps/Qt5'
os.environ['O4W_QT_BINARIES'] = qgis_root + '/apps/Qt5/bin'
os.environ['O4W_QT_PLUGINS'] = qgis_root + '/apps/Qt5/plugins'
os.environ['O4W_QT_LIBRARIES'] = qgis_root + '/apps/Qt5/lib'
os.environ['O4W_QT_TRANSLATIONS'] = qgis_root + '/apps/Qt5/translations'
os.environ['O4W_QT_HEADERS'] = qgis_root + '/apps/Qt5/include'
os.environ['O4W_QT_DOC'] = qgis_root + '/apps/Qt5/doc'

# enviro setup from py3_env.bat
os.environ['PYTHONPATH'] = qgis_root + '/apps/qgis/python;'
os.environ['PYTHONHOME'] = qgis_root + '/apps/Python37'
os.environ['OSGEO4W_ROOT'] = qgis_root + ''


# mimic path from cmd window after running bat file
os.environ['Path'] = qgis_root + '/apps/qgis/bin;'+qgis_root + '/apps/Python37;'+qgis_root + '/apps/Python37/Scripts;'+qgis_root + \
    '/apps/qt5/bin;'+qgis_root + '/apps/Python27/Scripts;'+qgis_root + \
    '/bin;C:/Windows/system32;C:/Windows;C:/Windows/system32/WBem'
