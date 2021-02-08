# GIS Processing
[home](../README.md)

Index
* [Vector Menu](#vector-menu)
* [Raster Menu](#raster-menu)
* [Processing Panel](#processing-panel)
* [Advanced processing topics](#advanced-topics)

QGIS provides many processing tools to help you analyze your GIS data. All the standard tools you would expect a GIS to provide are accessible to all users running QGIS. If the tool you need is more specialized it may be only accessible from the included GRASS GIS plugin or specific plugins you may need to install yourself. 
This document will discuss the standard tools available from QGIS. Access to processing tools from within QGIS is presented to users in three locations; Vector Menu, Raster Menu, and Processing Panel.

### Related QGIS Documentation

[QGIS docs - algorithm guide](https://docs.qgis.org/testing/en/docs/user_manual/processing_algs/index.html)

[QGIS Processing Guide]( https://docs.qgis.org/testing/en/docs/training_manual/processing/index.html)

## Vector Menu
The Vector menu provides access to many standard tools for interacting with vectors.  This menu is a convenient way to find common vector tools that have been organized categories: Geoprocessing, Geometry, Research, Analysis, and Data Management Tools.
Vector Menu Category|Examples
Geoprocessing Tools|Buffer, Clip,Intersection, Union
Geometry Tools|Calculate Centroids, Validate Geometry, Mulitpart to Singlepart
Research Tools|Create Grid, Select by Location, Create Random Points, Create Regular Points
Analysis Tools| Mean Coordinates, Field Statistics, Count points in polygon
Data Management Tools | Merge Layers, Split Layers, Join attributes by Location
## Raster Menu
The Raster menu provides access to many standard tools for interacting with raster data. This menu is a convenient way to access Raster Calculator, Align Rasters tool and other common raster tools that have been organized categories: Analysis, Projections, Miscellaneous, Extraction, Conversion. It should be noted that the Raster Calculator accessed in this menu is slightly different than the raster calculator accessed in the processing panel ([more on raster calculator](raster-calculator.md)).
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
## Processing Panel
The Processing Panel can be activated by using the Processing menu and clicking “Toolbox” or pressing <ctr+Alt+T>. This will start the processing toolbox panel. The contents can be searched using the Search dialog or by browsing the processing providers by category. 

![Processing Toolbox](../images/processing-toolbox.png)

The layout of QGIS Processing tools all follow a common layout that contains Parameters/log tabs on the left and a collapsable information dialog screen on the right. Input data layers can be selected from a drop down of suitable existing map layers drawn from the table of contents or select a file using the ![select-file-icon](../images/select-file-icon.png) select file dialog.
If the tool produces output datasets the same dialog button can be clicked in the output section to designate an output. ![processing-tool-output](../images/processing-toolbox-output.png)

If desired most tools allow for the output to remain blank and a temorary layer will be created and added to your map. 

After your tool has completed running the log will list the input parameters, execution time and output data location.
Your results will be accessible via the Results Viewer
Your processing history can be accessed by clicking the history icon ![history-icon](../images/processing-history-viewer-icon.png) at the top of the processing toolbox. 
![processing-history-graphic](../images/processing-history.png)The processing history dialog will list executed processes with respective parameters used. 

Some processing tools can be used in conjunction with layer editing to modify features in place. To use this feature start editing a layer and activate edit in place using the icon ![edit-in-place-icon](../images/processing-edit-in-place-icon.png). This is powerful way of [editing](editing.md) some or all features in a layer without duplicating data. Some examples of useful tools that can be used in this mode are:
- fix geometries
- simplify
- smooth
- multipart to sigleparts

## Advanced topics
[Graphical Modeler](graphical-modeler.md)  
[Processing with python](advanced-processing.md)


---
[Back to top](#gis-processing)
