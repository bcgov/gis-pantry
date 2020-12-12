
# Exporting data in QGIS

[home](../README.md)

[QGIS Documentation](https://docs.qgis.org/testing/en/docs/gentle_gis_introduction/data_capture.html)

## Index
* [Exporting to geopackage](#Exporting-to-geopackage)
* [Exporting to KML (Google Earth)](#Exporting-to-KML)
* [Exporting to shapefile](#Exporting-to-shapefile)
* [Exporting from temporary layers](#Exporting-from-temporary-layers)
* [Exporting from virtual layers](#Exporting-from-virtual-layers)

Exporting features in QGIS is pretty straightforward - you can choose one of 23 different file formats, export all features or selected features only, and you can define the coordinate reference system (CRS) while exporting.

## Exporting to geopackage
Here is a Geopackage (GeoDataPackage) (the native QGIS format) being exported to another Geopackage, in a new CRS, with only a few fields being written ( no need to include them all!). The Geopackage file's *layer name* defaults to being the same as the *file name*, or you can give it a unique name. Note that the geometry field *(geom)*  is automatically included in the fields exported, and the spatial index defaults to being built.

![exportGif_2](https://github.com/gecko2019/gis-pantry/blob/master/docs/getting-started-with-QGIS/images/exportGif_2.gif "Wheeeee!!")

Similar to ArcMap and ArcGIS Pro, one can also export selected features only:
![exportGif_3](https://github.com/gecko2019/gis-pantry/blob/master/docs/getting-started-with-QGIS/images/exportGif_3.gif "Oh yeahhhh!!")

GeoPackage can be read like a file geodatabase in ArcMap or ArcGIS Pro, but using dashes in the file name or layer names (i.e. roads-non-status) make one unreadable in ArcGIS.

## Exporting to KML (Google Earth)

KML is a popular and very accessible data format. Below is an example of exporting from selected GeoPackage features to KML and setting the Namefield (so each feature is easy to identify in Google Earth). It's important to ensure that "Save only selected features" and "Extent: current layer" boxes are checked. There's no need to try a new CRS, as KML files can only be in geographic coordinates (WGS 84 / EPSG 4326). (There's no attempt to preserve symbology, as QGIS is not good at exporting symbology to KML files.)
![exportToKML](https://github.com/gecko2019/gis-pantry/blob/master/docs/getting-started-with-QGIS/images/exportToKML.gif "Oh yeahhhh!!")

When you open the KML in Google Earth, you'll see the default symbology (features outlined in red) and can easily find the OPENING_ID you're looking for (or whatever field you specified as the Namefield.)
![tryExportedKML_final](https://github.com/gecko2019/gis-pantry/blob/master/docs/getting-started-with-QGIS/images/tryExportedKML_final.gif "That'll do!")

## Exporting to shapefile
A major drawback of exporting to shapefile is that field names in your source spatial file will be trimmed to just 10 characters width - this will make your field names hard to interpret!

More soon..

## Exporting from temporary layers
Coming soon..

## Exporting from virtual layers
Coming soon..