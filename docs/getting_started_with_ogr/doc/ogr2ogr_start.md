
# Getting started in command line: ogr2ogr


### 1. start the OsGeo4W command shell, where you can run ogr2ogr commands:
<img src= ./osgeo4wshell_where2.jpg width="300" height="80" />


### 2. . type ogr2ogr -help (hit enter); this shows you all the possible options to use with ogr2ogr.
    Usage: ogr2ogr [--help-general] [-skipfailures] [-append] [-update]
               [-select field_list] [-where restricted_where|@filename]
               [-progress] [-sql <sql statement>|@filename] [-dialect dialect]
               [-preserve_fid] [-fid FID] [-limit nb_features]
               [-spat xmin ymin xmax ymax] [-spat_srs srs_def] [-geomfield field]
               [-a_srs srs_def] [-t_srs srs_def] [-s_srs srs_def]
               [-f format_name] [-overwrite] [[-dsco NAME=VALUE] ...]
               dst_datasource_name src_datasource_name
               [-lco NAME=VALUE] [-nln name]
               [-nlt type|PROMOTE_TO_MULTI|CONVERT_TO_LINEAR|CONVERT_TO_CURVE]
               [-dim XY|XYZ|XYM|XYZM|layer_dim] [layer [layer ...]]


### 3. try running an ogr2ogr transformation: SDE feature class to KML
    ogr2ogr -a_srs epsg:3005 -f "KML" T:\aTest01.kml OCI:BCGWusername/BCGWpassword@IDWPROD1:noTable -sql "select * from WHSE_FOREST_VEGETATION.RSLT_OPENING_SVW  where OPENING_ID = '-228240000'" -progress

*Copy the above line, substitute your own BCGW login info, and paste into the OSGeo4W window and hit enter. Several warnings will pop up, but an output KML file will successfully write to the T: .*

Here's how the command above works:

`ogr2ogr` calls the executable file, E:\sw_nt\QGIS_3.8\bin\ogr2ogr.exe

`-a_srs epsg:3005` assigns an output spatial reference using epsg code 3005 (i.e. BC Albers)

`-f "KML" ` specifies the output format is "KML" (this is one of tow KML drivers in ogr)

`T:\aTest01.kml` this is the output folder and filename; if the folder does not exist, you must create it first

`OCI:BCGWusername/BCGWpassword@IDWPROD1:noTable` this specifies the source file, using the Oracle Spatial (OCI = Oracle Call Interface) driver. This must include a BCGW username and BCGW password, and reference the Oracle instance (@IDWPROD1) found in the tnsnames.ora file in E: . The *noTable* is a placeholder table name that prevents the OCI driver from searching through the entire BCGW for the table you want (you specify that in the SQL statement). 

`-sql` this indictaes the results are to be filtered via an Oracle SQL statement

`"select * from WHSE_FOREST_VEGETATION.RSLT_OPENING_SVW  where OPENING_ID = '-228240000'"` this is an SQL statement that fetches a single row in the RESULTS Openings dataset

`-progress` This shows a progress indicator as below:

    0...10...20...30...40...50...60...70...80...90...100 - done.

### 4. below are several examples (using the same RESULTS Openings dataset and query) of transforming data from the BCGW. You'll notice that different transformations produce differnt warnings. It may seem like all the warnings are a problem, but most only affect things likw field name length or layer names.
   
#### Create a Shapefile (readable in ESRI and QGIS):
    ogr2ogr -a_srs epsg:3005 -f "ESRI Shapefile" T:\aShapefile01.shp OCI:BCGWusername/BCGWpassword@IDWPROD1:noTable -sql "select * from WHSE_FOREST_VEGETATION.RSLT_OPENING_SVW  where OPENING_ID = '-228240000'" -progress

#### Create a GeoPackage (readable in ESRI and QGIS):
    ogr2ogr -a_srs epsg:3005 -f "GPKG" T:\aGeoPackage.gpkg OCI:BCGWusername/BCGWpassword@IDWPROD1:noTable -sql "select * from WHSE_FOREST_VEGETATION.RSLT_OPENING_SVW  where OPENING_ID = '-228240000'" -progress

#### Create a GeoJSON (readable in QGIS):
<<<<<<< HEAD
    ogr2ogr -a_srs epsg:3005 -f "GeoJSON" T:\aJSON.json OCI:BCGWusername/BCGWpassword@IDWPROD1:noTable -sql "select * from WHSE_FOREST_VEGETATION.RSLT_OPENING_SVW  where OPENING_ID = '-228240000'" -progress
=======
    ogr2ogr -a_srs epsg:3005 -f "GeoJSON" T:\aJSON.json OCI:BCGWusername/BCGWpassword@IDWPROD1:noTable -sql "select * from WHSE_FOREST_VEGETATION.RSLT_OPENING_SVW  where OPENING_ID = '-228240000'" -progress
>>>>>>> 914a8a9b9673b25c5a9409bff5fa61639b9103da
