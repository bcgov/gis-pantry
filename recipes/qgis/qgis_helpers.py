# qgis_helpers.py
# description: some helpers for qgis standalone python scripts
import sys
import os
import qgis_set_environment
from osgeo import ogr
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery 

def create_oracle_layer(layer_name,user_name,user_pass,db_table,geom_column_name,sql=None,geom_type=None,key='OBJECTID'):
    # create an QgsVector from oracle table
    uri = QgsDataSourceUri()
    uri.setConnection('bcgw.bcgov', '1521','idwprod1.bcgov', user_name, user_pass)
    schema, table = db_table.split('.')
    geom_c = get_bcgw_geomcolumn(db_table=db_table,user_name=user_name,user_pass=user_pass)
    geom_type = get_bcgw_table_geomtype(db_table=db_table,geom_column_name=geom_c,user_name=user_name,user_pass=user_pass)
    key = get_bcgw_column_key(db_table=db_table,user_name=user_name,user_pass=user_pass)
    if sql is not None:
        if len(sql)>0:
            if 'WHERE' in sql.upper():
                uri.setSql(sql)
                uri.setDataSource(schema, table, geom_column_name)
            else:
                table = f"(select * from {db_table} WHERE {sql} )"
                uri.setDataSource("", table, geom_column_name,"",key)
    else:
        uri.setDataSource(schema, table, geom_column_name,key)
    
    uri.setSrid('EPSG:3005')
    
    uri.setUseEstimatedMetadata(True)
    uri.setKeyColumn(key)
    
    if geom_type == 'Point':
        uri.setWkbType(QgsWkbTypes.Point)
    elif geom_type == 'Polygon':
        uri.setWkbType(QgsWkbTypes.Polygon)
    elif geom_type == 'LineString':
        uri.setWkbType(QgsWkbTypes.LineString)
    elif geom_type == 'MultiPolygon':
        uri.setWkbType(QgsWkbTypes.MultiPolygon)
    elif geom_type == 'MultiLineString':
        uri.setWkbType(QgsWkbTypes.MultiLineString)
    elif geom_type == 'MulitPoint':
        uri.setWkbType(QgsWkbTypes.MulitPoint)
    else:
        print (f"Unexpected geometry: {geom_type}")

    tlayer = QgsVectorLayer(uri.uri(), layer_name, 'oracle')
    assert tlayer.isValid()
    tlayer.setCrs(QgsCoordinateReferenceSystem("EPSG:3005"))
    
    return tlayer

def get_bcgw_table_geomtype(db_table,geom_column_name,user_name,user_pass):
    # get geometry type from oracle table - oracle stores multiple types so
    # this returns the maximum type ie multiline, multipolygon, multipoint if
    # present in geometry
    owner,table = db_table.split('.') 
    driver ="QOCISPATIAL"
    conn_name = "bcgw_conn"
    if not QSqlDatabase.contains(conn_name):
        db = QSqlDatabase.addDatabase(driver,conn_name)
    else:
        db = QSqlDatabase.database(conn_name)
    db.setDatabaseName('bcgw.bcgov' + "/" + 'idwprod1.bcgov') 
    db.setUserName(user_name) 
    db.setPassword(user_pass) 
    db.open()
    if not db.open(): 
        print ("Failed Connection from find_bcgw_the_geom") 
    q = QSqlQuery(db) 
    query = f"SELECT MAX(t.{geom_column_name}.GET_GTYPE()) AS geometry_type from {owner}.{table} t"
    q.exec(query) 
    q.first()
    type_num = q.value(0)
    if type_num == 1:
        geom_t = 'Point'
    elif type_num == 2:
        geom_t = 'LineString'
    elif type_num == 3:
        geom_t = 'Polygon'
    elif type_num == 7:
        geom_t = 'MultiPolygon'
    elif type_num ==5:
        geom_t = 'MulitPoint'
    elif type_num ==6:
        geom_t = 'MultiLineString'
    else:
        db.close()
        raise TypeError
    db.close()
    return geom_t

def get_bcgw_geomcolumn(db_table,user_name,user_pass):
    # get the name of the geometry column for oracle table
    owner,table = db_table.split('.') 
    driver ="QOCISPATIAL" 
    conn_name = "bcgw_conn"
    if not QSqlDatabase.contains(conn_name):
        db = QSqlDatabase.addDatabase(driver,conn_name)
    else:
        db = QSqlDatabase.database(conn_name)
    db.setDatabaseName('bcgw.bcgov' + "/" + 'idwprod1.bcgov') 
    db.setUserName(user_name) 
    db.setPassword(user_pass) 
    db.open()
    if not db.open(): 
        print ("Failed Connection from find_bcgw_the_geom") 
    q = QSqlQuery(db) 
    query ="SELECT COLUMN_NAME from all_tab_columns where OWNER = '{}' AND TABLE_NAME = '{}' AND DATA_TYPE = 'SDO_GEOMETRY'".format(owner,table)  
    q.exec(query) 
    q.first() 
    geom_c = q.value(0)
    db.close()
    return geom_c

def get_bcgw_column_key(db_table,user_name,user_pass):
    # estimate a unique id column for an oracle table if OBJECTID does not exist
    owner,table = db_table.split('.') 
    driver ="QOCISPATIAL" 
    conn_name = "bcgw_conn"
    if not QSqlDatabase.contains(conn_name):
        db = QSqlDatabase.addDatabase(driver,conn_name)
    else:
        db = QSqlDatabase.database(conn_name)
    db.setDatabaseName('bcgw.bcgov' + "/" + 'idwprod1.bcgov') 
    db.setUserName(user_name) 
    db.setPassword(user_pass) 
    db.open()
    if not db.open(): 
        print ("Failed Connection from find_bcgw_the_geom") 
    q = QSqlQuery(db)
    sql = f"SELECT cols.column_name \
    FROM all_tab_cols cols where cols.table_name = '{table}' and cols.COLUMN_NAME like \'OBJECTID\'"
    q.exec(sql)
    if q.first():
        key_c = q.value(0)
    else:
        sql = f"SELECT COLUMN_NAME FROM all_tab_cols where table_name = '{table}' \
            order by COLUMN_ID FETCH FIRST 1 ROWS ONLY"
        q.exec(sql)
        if q.first():
            key_c = q.value(0)
    db.close()
    return key_c

def create_gpkg(root,name,overwrite=False):
    # create an empty geopackage
    fullpath = os.path.join(root,name)
    if os.path.exists(fullpath):
        if overwrite is True:
            try:
                os.remove(fullpath)
            except OSError as error:
                print (error)
                print (f"Error removing: {fullpath}")
        else:
            print (f"Error: File exists (overwite=False)")
            return None
    else:
        driver = ogr.GetDriverByName('GPKG')
        driver.CreateDataSource(fullpath)
        return fullpath

