This Python recipe runs SQL Queries against BCGW Spatial tables/views
and external shapes (AOI).


## User Inputs:
1) AOI - ESRI shp and featureclass/gdb are supported.
2) bcgw_user - BCGW/idwprod1 username
3) bcgw_pwd -  BCGW/idwprod1 password
4) SQL - query to execute.
5) out_loc - Output location


## Workflow:
1) Connect to Database (BCGW).
2) Convert ESRI format shape to Geopandas format. 
3) Retireve Geometry WKT string and Spatial ref. for each feature.
4) Run the SQL Query.
5) Export Query Results to an Excel file.


## Dependencies:
- cx_Oracle
- Geopandas
- Pandas
  
  
The query used in this recipe is looking for Active Aqua Crown Tenures
intersecting with an AOI. Customize the "sql" parameter 
for other  Query types.


See Oracle doscumentation for full list of Spatial Operators:
https://docs.oracle.com/cd/E11882_01/appdev.112/e11830/sdo_operat.htm#SPATL110
