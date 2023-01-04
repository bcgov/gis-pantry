import os
import cx_Oracle
import pandas as pd
#import fiona
import geopandas as gpd


def connect_to_DB (username,password,hostname):
    """ Returns a connection to Oracle database"""
    try:
        connection = cx_Oracle.connect(username, password, hostname, encoding="UTF-8")
        print  ("Successffuly connected to the database")
    except:
        raise Exception('Connection failed! Please verifiy your login parameters')

    return connection


def esri_to_gdf (aoi):
    """Returns a Geopandas file (gdf) based on 
       an ESRI format vector (shp or featureclass/gdb)"""
    
    if '.shp' in aoi: 
        gdf = gpd.read_file(aoi)
    
    elif '.gdb' in aoi:
        l = aoi.split ('.gdb')
        gdb = l[0] + '.gdb'
        fc = os.path.basename(aoi)
        gdf = gpd.read_file(filename= gdb, layer= fc)
        
    else:
        raise Exception ('Format not recognized. Please provide a shp or featureclass (gdb)')
    
    return gdf
    
      
def get_wkt_srid (gdf):
    """Returns the SRID and WKT string of each feature in a gdf"""
    
    #gdf['wkt'] = gdf.apply(lambda row:row['geometry'].wkt, axis=1)
    
    srid = gdf.crs.to_epsg()
    if srid != 3005:
        raise Exception ('Shape must be in BC Albers Projection!')
    
    # Generate WKT strings. 
    #If WKT string is larger then 4000 characters (ORACLE VARCHAR2 limit), 
     # OPTION A: algorithm will simplify the geometry until limit is reached.
    
    wkt_dict = {}
    for index, row in gdf.iterrows():
        f = 'feature '+ str(index) # Replace index with another ID column (name ?)
        wkt = row['geometry'].wkt
    
        if len(wkt) < 4000:
            print ('{} - FULL WKT returned: within Oracle VARCHAR limit'.format(f)) 
            wkt_dict [f] = wkt
            
        else:
            print ('Geometry will be Simplified for {} - beyond Oracle VARCHAR limit'.format (f))
            s = 50
            wkt_sim = row['geometry'].simplify(s).wkt

            while len(wkt_sim) > 4000:
                s += 10
                wkt_sim = row['geometry'].simplify(s).wkt

            print ('Geometry Simplified with Tolerance {} m'.format (s))            
            wkt_dict [f] = wkt_sim 
                
            #Option B: just generate an Envelope Geometry
            #wkt_env = row['geometry'].envelope.wkt
            #wkt_dict [f] = wkt_env

    return wkt_dict, srid


def read_query(connection,query):
    "Returns a df containing SQL Query results"
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        names = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        return pd.DataFrame(rows, columns=names)
    
    finally:
        if cursor is not None:
            cursor.close()
   
            
def generate_report (workspace, df_list, sheet_list, filename):
    """ Exports dataframes to multi-tab excel spreasheet"""
    out_file = os.path.join(workspace, str(filename) + '.xlsx')

    writer = pd.ExcelWriter(out_file,engine='xlsxwriter')

    for dataframe, sheet in zip(df_list, sheet_list):
        dataframe = dataframe.reset_index(drop=True)
        dataframe.index = dataframe.index + 1

        dataframe.to_excel(writer, sheet_name=sheet, index=False, startrow=0 , startcol=0)

        worksheet = writer.sheets[sheet]

        worksheet.set_column(0, dataframe.shape[1], 20)
        
        col_names = [{'header': col_name} for col_name in dataframe.columns[1:-1]]
        col_names.insert(0,{'header' : dataframe.columns[0], 'total_string': 'Total'})
        col_names.append ({'header' : dataframe.columns[-1], 'total_function': 'count'})

        worksheet.add_table(0, 0, dataframe.shape[0]+1, dataframe.shape[1]-1, {
            'total_row': True,
            'columns': col_names})

    writer.save()


def main ():
    aoi = input("Enter the location of your AOI file (shp or featureclass):")
    
    hostname = 'bcgw.bcgov/idwprod1.bcgov'
    bcgw_user = os.getenv('bcgw_user')
    bcgw_pwd = os.getenv('bcgw_pwd')
    
    print ('Connecting to BCGW...')
    connection = connect_to_DB (bcgw_user,bcgw_pwd,hostname)
    
    print ('\nReading the input file...')
    gdf = esri_to_gdf (aoi)
    
    print ('\nGetting WKT and SRID...')
    wkt_dict, srid = get_wkt_srid (gdf)
    
    sql =  """
            SELECT*
            FROM WHSE_TANTALIS.TA_CROWN_TENURES_SVW t
            WHERE t.TENURE_PURPOSE = 'AQUACULTURE'
            AND t.TENURE_STAGE = 'TENURE'
            AND SDO_RELATE (t.SHAPE, SDO_GEOMETRY('{w}', {s}),
                            'mask=ANYINTERACT') = 'TRUE'
            """
    
    print ('\nRunning SQL...')
    dfs = []
    keys = []
    for k, v in wkt_dict.items():
        query = sql.format(w= v,  s= srid)
        df = read_query(connection,query)
        
        if df.shape [0] < 1:
            print ('Feature {} table is empy - No results exported')
        else:
            dfs.append(df)
            keys.append(k)  
    
    print ('\nExporting Query Results...')
    out_loc = input("Enter an output location (folder):")
    sheets = ['Intersect ' + k for k in keys]
    generate_report (out_loc, dfs, sheets, 'Query_Results')


main ()
