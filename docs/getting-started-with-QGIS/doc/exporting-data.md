
# Exporting data in QGIS

[home](../README.md)

[QGIS Documentation](https://docs.qgis.org/testing/en/docs/gentle_gis_introduction/data_capture.html)

## Index
* [Exporting - general](#Exporting-general)
* [Exporting to geopackage](#Exporting-to-geopackage)
* [Exporting to KML (Google Earth)](#Exporting-to-KML)
* [Exporting to shapefile](#Exporting-to-shapefile)
* [Exporting from temporary layers](#Exporting-from-temporary-layers)
* [Exporting from virtual layers](#Exporting-from-virtual-layers)

## Export all features / selected features 
Exporting features in QGIS is pretty straightforward - you can choose one of 23 different file formats, export all features or selected features only, and you can define the coordinate reference system (CRS) while exporting.

Here is a Geopackage (the native QGIS format) being exported to another Geopackage, in a new CRS, with only a few fields being written ( no need to include them all!). The Geopackage file's layer name defaults to being the same as the file, or you can give it a unique name. Note that the geometry field is automatically included in the fields exported, and the spatial index defaults to being built.
![](https://github.com/bcgov/gis-pantry/blob/master/docs/getting-started-with-QGIS/images/exportGif_2.gif)
