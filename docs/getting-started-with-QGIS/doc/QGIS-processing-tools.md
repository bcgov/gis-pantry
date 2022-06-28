# GIS Processing
[Home](../README.md)

Index
* [Vector Menu](#vector-menu)
* [Raster Menu](#raster-menu)
* [Processing Panel](#processing-panel)
* [Advanced processing topics](#advanced-topics)

QGIS provides many processing tools to help you analyze your GIS data. All the standard tools you would expect a GIS to provide are accessible to all users running QGIS. If the tool you need is more specialized it may be only accessible from the included GRASS GIS plugin or specific plugins you may need to install yourself.

This document will discuss the standard tools available from QGIS. Access to processing tools from within QGIS is presented to users in three locations; Vector Menu, Raster Menu, and Processing Panel.

### Related QGIS Documentation

[QGIS docs - algorithm guide](https://docs.qgis.org/testing/en/docs/user_manual/processing_algs/index.html)

[QGIS Processing Guide](https://docs.qgis.org/testing/en/docs/training_manual/processing/index.html)

## Vector Menu
The Vector menu provides access to many standard tools for interacting with vectors.  This menu is a convenient way to find common vector tools that have been organized into categories: Geoprocessing, Geometry, Research, Analysis, and Data Management Tools.<br>
Vector Menu Category|Examples:

1. Geoprocessing Tools
    - Buffer, Clip,Intersection, Union
2. Geometry Tools
    - Calculate Centroids, Validate Geometry, Mulitpart to Singlepart
3. Research Tools
    - Create Grid, Select by Location, Create Random Points, Create Regular Points
4. Analysis Tools
    - Mean Coordinates, Field Statistics, Count points in polygon
5. Data Management Tools
    - Merge Layers, Split Layers, Join attributes by Location

## Raster Menu
The Raster menu provides access to many standard tools for interacting with raster data. This menu is a convenient way to access Raster Calculator, Align Rasters tool and other common raster tools that have been organized into categories: Analysis, Projections, Miscellaneous, Extraction, and Conversion. It should be noted that the Raster Calculator accessed in this menu is slightly different than the raster calculator accessed in the processing panel ([more on raster calculator](raster-calculator.md)).<br>
Raster Menu Category|Examples:

1. Analysis
    - Aspect, Slope, Hillshade
2. Projections
    - Assign Projection, Extract Projection,Warp(reproject)
3. Miscellaneous
    - Merge, Build Virtual Raster, Tile index
4. Extraction
    - Clip Raster, Create contours
5. Conversion
    - Raster to Vector, Vector to Raster, Translate (conversion)

The Vector menu provides access to many standard tools for interacting with vectors.  This menu is a convenient way to find common vector tools that have been organized into these categories: Geoprocessing, Geometry, Research, Analysis, and Data Management Tools.


## Processing Panel
The Processing Panel can be activated by using the Processing menu and clicking “Toolbox” or pressing **<ctr+Alt+T>**. This will start the processing toolbox panel. The contents can be searched using the Search dialog or by browsing the processing providers by category. 

![Processing Toolbox](../images/processing-toolbox.png)


The QGIS Processing tools all follow a common layout that contains a Parameters tab and Log tab on the left and a collapsible information dialog screen on the right. Input data layers can be selected from a drop down of suitable existing map layers drawn from the table of contents or selected from a file using the ![select-file-icon](../images/select-file-icon.png) select file dialog. If the tool produces output datasets, the same dialog button can be clicked in the output section to designate an output. 

![processing-tool-output](../images/processing-toolbox-output.png)

If desired, most tools allow for the output to remain blank and a temporary layer will be created and added to your map. A temporary layer will have a small icon to the right of the layer name in the Layers panel. Hovering over the icon will show a pop-up saying *"Temporary layer only! Contents will be discarded after closing QGIS"*. 

After your tool has completed running the log will list the input parameters, execution time and output data location. Your results will be accessible via the Results Viewer. And your processing history can be accessed by clicking the history icon ![history-icon](../images/processing-history-viewer-icon.png) at the top of the processing toolbox.


The processing history dialog will list executed processes with respective parameters used. 

![processing-history-graphic](../images/processing-history.png)

Some processing tools can be used in conjunction with layer editing to modify features in place. To use this feature start editing a layer and activate edit in place using the icon ![edit-in-place-icon](../images/processing-edit-in-place-icon.png). This is powerful way of [editing](editing-data.md) some or all features in a layer without duplicating data. Some examples of useful tools that can be used in this mode are:
- fix geometries
- simplify
- smooth
- multipart to sigleparts

## Advanced topics
[Graphical Modeler](graphical-modeler.md)  
[Processing with python](advanced-automation-with-python.md)


---
[Back to top](#gis-processing)
