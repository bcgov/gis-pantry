# GIS Processing
[home](readme.md)


[QGIS docs - algorithm guide](https://docs.qgis.org/testing/en/docs/user_manual/processing_algs/index.html)

[QGIS Processing Guide]( https://docs.qgis.org/testing/en/docs/training_manual/processing/index.html)

QGIS provides many processing tools to help you analyze your GIS data. All the standard tools you would expect a GIS to provide are accessible to all users running QGIS. If the tool you need is more specialized it may be only accessible from the included GRASS GIS plugin or specific plugins you may need to install yourself. 
This document will discuss the standard tools available from QGIS. Access to processing tools from within QGIS is presented to users in three locations; Vector Menu, Raster Menu, and Processing Panel.
## Vector Menu
The Vector menu provides access to many standard tools for interacting with vectors.  This menu is a convenient way to find common vector tools that have been organized categories: Geoprocessing, Geometry, Research, Analysis, and Data Management Tools.
Vector Menu Category|Examples
Geoprocessing Tools|Buffer, Clip,Intersection, Union
Geometry Tools|Calculate Centroids, Validate Geometry, Mulitpart to Singlepart
Research Tools|Create Grid, Select by Location, Create Random Points, Create Regular Points
Analysis Tools| Mean Coordinates, Field Statistics, Count points in polygon
Data Management Tools | Merge Layers, Split Layers, Join attributes by Location
## Raster Menu
The Raster menu provides access to many standard tools for interacting with raster data. This menu is a convenient way to access Raster Calculator, Align Rasters tool and other common raster tools that have been organized categories: Analysis, Projections, Miscellaneous, Extraction, Conversion. It should be noted that the Raster Calculator accessed in this menu is slightly different than the raster calculator accessed in the processing panel.
Raster Menu Category|Examples
Analysis|Aspect, Slope, Hillshade
Projections|Assign Projection, Extract Projection,Warp(reproject)
Miscellaneous|Merge, Build Virtual Raster, Tile index
Extraction|Clip Raster, Create contours
Conversion|Raster to Vector, Vector to Raster, Translate (conversion)
## Processing Panel
The Processing Panel can be activated by using the Processing menu and clicking “Toolbox” or pressing <ctr+Alt+T>. This will start the processing toolbox panel. The contents can be searched using the Search dialog or by browsing the processing providers by category. 

![Processing Toolbox](../images/processing-toolbox.png)