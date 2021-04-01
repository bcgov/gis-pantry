# Advanced automation with python and QGIS (PyQGIS)

[Home](../README.md)

QGIS is a powerful tool to solve more complex and custom analysis problems using python scripting. QGIS uses a 64-bit Python 3 interepreter that is included with the software.

Recomended reading

* [PyQGIS 101 - Anita Graser](https://anitagraser.com/pyqgis-101-introduction-to-qgis-python-programming-for-non-programmers/)
* [QGIS Python Cookbook ](https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/)

Index <br>
* [QGIS Python console](#qgis-python-console)
* [Stand-alone Python Scipts](#stand-alone-python-scripts)
* [Plugin developement](#plugin-developement)

# QGIS Python Console
The QGIS Python Console can be accessed from the Plugins Menu --> Python Console or from the Python Console launch icon in the plugins toolbar using this icon  ![python-console-icon](../images/python-console-icon.png)<br>
Below is an example of adding a shapefile to your project taken directly from the [PyQGIS Cookbook](https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/loadlayer.html#id1)

```
# get the path to the shapefile e.g. /home/project/data/ports.shp
path_to_airports_layer = "testdata/airports.shp"

# The format is:
# vlayer = QgsVectorLayer(data_source, layer_name, provider_name)

vlayer = QgsVectorLayer(path_to_airports_layer, "Airports layer", "ogr")
if not vlayer.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(vlayer)
```
The Python Console gives you access to everything in your project including data and data symbologies, map canvas contents, and layouts.

## Stand-alone python scripts
Running standalone scripts with QGIS dependencies is more complex then executing script from within the QGIS Python Console primarly due to the environment and QT application dependencies required for scripts to run correctly. Setting these dependencies has been handeled in a script [qgis_set_environment.py](https://github.com/bcgov/gis-pantry/blob/master/recipes/qgis/qgis_set_environment.py) that can be imported to your standalone script to handle the setup. A os environment variable QGIS_PATH needs to be set on your windows installation to point to the QGIS install path.

If you are utilizing the BCGW oracle database there is some good tools to help create QGIS vector layers here [qgis-helpers.py](https://github.com/bcgov/gis-pantry/blob/master/recipes/qgis/qgis_helpers.py)

Once the environment setup script has been imported python should execute as it does in the QGIS Python Console. Some examples can be found [here](https://github.com/bcgov/gis-pantry/tree/master/recipes/qgis)

## Plugin Developement

There has been very little experience building plugins for QGIS in the BCGOV. One example can be found [here](https://github.com/bcgov/new2Q-reports/tree/master/Plugin/fn_bline).

Some tools have been created to help create templates that will expediate plugin developement.
* [Plugin Builder Plugin](https://github.com/g-sherman/Qgis-Plugin-Builder)
* [Minimalist Plugin Template](https://github.com/wonder-sk/qgis-minimal-plugin)

---
[Back to Top](#Advanced-automation-with-python-and-QGIS-(PyQGIS))

