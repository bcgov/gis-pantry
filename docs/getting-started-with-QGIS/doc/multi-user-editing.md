#  Multi-user editing in QGIS
#  Using PostGIS and the Versioning Plugin

[home](../readme.md)

[QGIS Documentation](https://docs.qgis.org/testing/en/docs/gentle_gis_introduction/data_capture.html)


## What is PostgreSQL / PostGIS and why do you need it?
PostgreSQL (pronounced "postgres" by these authors) is an open source object-relational database system that came out of the University of California, Berkeley in the 1980's (https://www.postgresql.org/about/).

PostGIS is an add on for PostgreSQL that spatially enables the database (https://postgis.net/). 

How to load the Versioining Plugin into QGIS:
![](../images/LoadingVersioningPlugin.gif)

## What is the versioning plugin

Our team has dived into using PostGIS on the recommendation from our architecture specialists as an open-source solution to allow for multiple users to access, edit, and save changes concurently without the risk of locked datasets and lost changes. A plugin has been developed for QGIS by Oslandia for versioning PostGIS databases (https://github.com/Oslandia/qgis-versioning). (Our architecture specialists are busy setting up our database and testing is commencing now, so this project is still in it's infancy).  

These are some extra links to browse through for those interested in learning more about PostGIS and the Versioning plugin:
  * https://www.bostongis.com/PrinterFriendly.aspx?content_name=postgis_tut01
  * https://docs.qgis.org/testing/en/docs/training_manual/spatial_databases/index.html   
  * https://readthedocs.org/projects/qgis-versioning/downloads/pdf/latest/
  * https://qgis-versioning.readthedocs.io/en/latest/introduction.html

![](../images/)

## Connecting to a PostgreSQL Database
1. 
![](../images/)

## Versioning Plugin
1. Add a link to Jing's plugins page for more info..
### Start versioning a data set
1. Group layers
2. "historize: tables and field created
3. Back to PG Admin to show new tables and fields
4. 
![](../images/create_grid.gif)
### How to tell if a table is historized already
1. c
2. 
![](../images/)
## Creating a verison and doing edits
1. 
2. 
3. 
4. 
![](../images/)
## Branching
1.  
2. 
3. 
![](../images/)
## Committing edits to the master

![](../images/)
1. Commit button
2. Conflicts
3. 
4. 
![](../images/)

## View historical changes and reverting.
1. 
2. 
3. 
![](../images/)


![](../images/)
