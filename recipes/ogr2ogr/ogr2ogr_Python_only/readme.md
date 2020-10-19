
<!-- 
Examples of markdown here: https://www.markdownguide.org/basic-syntax/
Syntax:placing an image from a website    ![myimg](link)
Syntax:placing two separate website images, separated by &nbsp spaces:  ![img1](link1)&nbsp;&nbsp;&nbsp;&nbsp; ![img2](link2)
Syntax:making coloured text (uses HTML):  <span style="color:blue">some *blue* text</span>
-->

![GDAL](https://www.osgeo.org/wp-content/themes/roots/assets/img/logo-osgeo.svg "GDAL")&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ![OGR](https://gdal.org/_static/gdalicon.png "OGR")&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![BCGOV](https://catalogue.data.gov.bc.ca/assets/gov/images/gov3_bc_logo.png "BCGOV")

# ogr from BCGW
This is a script that allows you to grab a dataset or filtered subset from the BC data Catalogue (BCGW) and translate it to one of several geospatial formats:

* GeoPackage - QGIS' native format, similar to a geodatabase. Works in QGIS and ArcGIS 10.3, 10.6 and ArcPro
* GeoJSON - very lightweight, easy-to-read format. Can drag-and-drop into QGIS
* KML - Google Earth layers
* ESRI Shapefile - ESRI Shapefile
* More will be added..

#### The script does the following:
* <span style="color:green">takes user input for desired output format ("GPKG", "GeoJSON", "KML", or "ESRI Shapefile"), path and filename</span>
* <span style="color:green">creates an ogr2ogr command line interface (CLI) string - this is the string you would use to run ogr2ogr in the OSGeo4W shell</span>
* <span style="color:green">executes the CLI string from within the Python script (via the subprocess module)</span>

*That's it - your geospatial file will be found in your specified path after running the script.*

### Notes
* <span style="color:lightblue">There are several usage examples embedded within the script; these provide good examples of how to use SQL to filter a BCGW dataset by attributes or spatial extent.</span>

## License
    Copyright 2019 BC Provincial Government

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.