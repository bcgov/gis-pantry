# +-------------------------------------------------------------------------------------------------
# Author:cfolkers
# Ministry, Division, Branch: WLRS - GSS
# Created Date: 2025 03 26
# Updated Date: 
# Description: 
#               open source script to pull data from BCGW and convert it to KML and GPX with colors and attributes picked by client.
#               This is a yearly update for snowmobile access managment area (AMA)s and trails in BC
#               includes all snowmobile AMA and trails with attributes from WHSE_WILDLIFE_INVENTORY.AMA_SNOWMOBILE_MGMT_AREAS_SP
#               and WHSE_WILDLIFE_INVENTORY.AMA_SNOWMOBILE_MGMT_TRAILS_SP   

# Tags: BCGW, Oracle, SQL, KML, GPX, Snowmobile, AMA, Caribou
# +-------------------------------------------------------------------------------------------------

import os 
from shapely.wkt import loads as load_wkt
from shapely.geometry import Polygon
import simplekml
import gpxpy
import gpxpy.gpx
import oracledb
from getpass import getpass
from datetime import date
import numpy as np
import re 

bcgw_username=input('enter bcgw username: ')
bcgw_password=getpass('enter bcgw password: ')

project_folder= r"/gr_2025_162_snomo_access"
work_folder=os.path.join(project_folder, 'work')
output_location=os.path.join(project_folder,"deliverables")

kml_out=os.path.join(output_location, 'kml')
gpx_out=os.path.join(output_location, 'gpx')

# Validate Oracle database connection
try:
    usernme = bcgw_username
    userpwd = bcgw_password
    host = "bcgw.bcgov"
    port = 1521
    service_name = "idwprod1.bcgov"
    dsn = f'{host}:{port}/{service_name}'
    
    # Attempt to establish a connection
    connection = oracledb.connect(user=usernme, password=userpwd, dsn=dsn)
    cursor = connection.cursor()
    print("Database connection successful.")
except oracledb.DatabaseError as e:
    # Handle database connection errors
    error, = e.args
    print(f"Database connection failed: {error.message}")
    exit(1)  # Exit the script if the connection fails

# Define SQL queries for each region
cent_koot_line_q=""" SNOWMOBILE_TRAIL_NAME IN ('Central Selkirks')"""
cent_koot_poly_q=""" SNOWMOBILE_AREA_NAME IN ('Central Selkirks')"""
hart_range_line_q=""""""
hart_range_poly_q="""SNOWMOBILE_AREA_NAME IN ('McBride / Cushing Creek', 'Kakwa Park Riding Area', 'Kakwa Park Riding Area', 'Gleason', 'Lower Torpy River', 'Sande Burn', 'Evanoff Park Riding Area', 'Walker Creek - Wallop Mtn', 'Mt. Hedrich', 'Weaver Peak', 'Northern Hart Range', 'Mt. McCullagh', 'Muller Creek', 'Mt. Kudson - Pearson Peak', 'Captain Creek',
                'Bearpaw Ridge', 'Sande', 'Herrick Creek', 'Three Brothers Peaks', 'Holy Cross Mtn', 'Bastille Creek', 'Limestone Lakes', 'Evanoff', 'Forgetmenot Mtn', 'Mt. Severeid', 'McGregor River', 'Mt. Rider', 'Otter Lake','Fontoniko Creek', 'Framstead Creek', 'Torpy River', 'Pass Lake')"""
n_rockies_line_q="""SNOWMOBILE_TRAIL_NAME IN ('Walker Creek/Wallop Mtn Trail','Iver Lake Trail')"""
n_rockies_poly_q="""SNOWMOBILE_AREA_NAME IN ('Bullmoose Closure', 'Holsworth Meadows', 'Bullmoose South', 'Spieker', 'Tunnel Mountain', 'Mount Palsson', 'Wolverine', 'Sukunka', 'Pyramid', 'Chamberlain', 'Red Deer North', 'Saxon', 'Torrens', 'Nekik', 'Red Deer South', 'Brazion', 'Hasler', 'Klin-se-za', 'Silver Sands', 'Windfall Lake', 'Ptarmigan', 'East Klin-se-za',
                'Hudette', '42', 'Upper Burnt', 'Watson', 'Upper Burnt East', 'Mischininlika', 'Bijoux', 'Murray', 'Albright', 'Imperial')"""
quesnel_high_line_q="""SNOWMOBILE_TRAIL_NAME IN ('Bald Mountain Access Trail')"""
quesnel_high_poly_q="""SNOWMOBILE_AREA_NAME IN ('Eureka Peak SMA Goat Closure', 'Eureka Peak SMA Goat Closure', 'Eureka Peak SMA Riding Area', 'Grain Creek SMA', 'Yanks Peak SMA', 'Bald Mountain SMA', 'Mica Mountain Riding Area', 'Eureka Peak SMA Riding Area', 'Sliding Mtn', 'Bill Miner - Watchman Mtn - Eureka', 'Deception Creek', 'Ishpa Mtn', 'Turks Nose Mtn',
                    'Wells', 'Eureka - Boss Mtn - Deception', 'Warting Lake', 'Blue Lead Creek North', 'Grain Creek', 'Mtn Meridan - Milk Ranch Mtn', 'Mt. Patchett', 'Ketcham Creek', 'Spanish Creek', 'Mt. Patchett South', 'Eaglenest Mtn', 'Blue Lead Creek East', 'Quesnel Lake Junction', 'Cariboo Mtn - Keithley Creek Mtn', 'Hobson Lake', 'Blue Lead Creek West', 'Quart Mtn', 'Hardscrabble Mtn East', 'Two Sisters Mtn')"""
revelstoke_line_q="""SNOWMOBILE_TRAIL_NAME IN ('Fred Laing', 'Foster Access Trail')"""
revelstoke_poly_q="""SNOWMOBILE_AREA_NAME IN ('Anstey Range', 'Mt Grace', 'Queest Mountain Riding Area', 'Trident Glacier', 'Foster Creek', 'Seymour Range', 'Encampment North', 'Sale Mountain', 'Monashee/Selkirk Mountains', 'Monashee/Selkirk Mountains West', 'Myoff Creek - Monashee/Selkirk Mountains', 'Caribou Basin', 'Standard', 'French Glacier',
                    'Monashee/Selkirk Mountains East', 'Revelstoke/Shuswap', 'Keystone','Howard Creek')"""
se_koot_line_q="""SNOWMOBILE_TRAIL_NAME IN ('Angus Access Trail', 'Purcell South Access Trail', 'Angus Access Trail', 'Cranbrook West Rec Mgmt Strategy Travel Corridor', 'Cranbrook West Rec Mgmt Strategy Travel Corridor', 'Cranbrook West Rec Mgmt Strategy Travel Corridor', 'Cranbrook West Rec Mgmt Strategy - Legal S Purcell',
                'Cranbrook West Rec Mgmt Strategy - Legal S Purcell', 'Cranbrook West Rec Mgmt Strategy Travel Corridor', 'Cranbrook West Rec Mgmt Strategy Travel Corridor', 'Purcell South Access Trail', 'Purcell South Access Trail', 'Purcell South Access Trail', 'Purcell South Access Trail', 'Purcell South Access Trail', 'Purcell South Access Trail')"""
se_koot_poly_q="""SNOWMOBILE_AREA_NAME IN ('Purcell South', 'Purcell South', 'Cranbrook West Recreation Management Strategy', 'Purcell South', 'Cranbrook West Recreation Management Strategy', 'Cranbrook West Recreation Management Strategy', 'Cranbrook West Recreation Management Strategy', 'Cranbrook West Recreation Management Strategy',
                'Cranbrook West Recreation Management Strategy', 'Cranbrook West Recreation Management Strategy', 'Cranbrook West Recreation Management Strategy', 'Cranbrook West Recreation Management Strategy / Matthew Creek', 'Cranbrook West Recreation Management Strategy', 'Cranbrook West Recreation Management Strategy', 'Purcell South', 'Cranbrook West Recreation Management Strategy',
                'Cranbrook West Recreation Management Strategy', 'Cranbrook West Recreation Management Strategy', 'Purcell South', 'Cranbrook West Recreation Management Strategy', 'Cranbrook West Recreation Management Strategy', 'Cranbrook West Recreation Management Strategy', 'Cranbrook West Recreation Management Strategy', 'Cranbrook West Recreation Management Strategy', 'Purcell South',
                'Cranbrook West Recreation Management Strategy', 'Purcell South', 'Purcell South', 'Cranbrook West Recreation Management Strategy', 'Cranbrook West Recreation Management Strategy', 'Cranbrook West Recreation Management Strategy', 'Purcell South', 'Purcell South', 'Skookumchuck Creek', 'Cranbrook West Recreation Management Strategy', 'Purcell South', 'Angus', 'Buhl Creek',
                'Purcell South', 'Cranbrook West Recreation Management Strategy', 'Purcell South', 'Purcell South')"""
sw_koot_line_q=""""""
sw_koot_poly_q="""SNOWMOBILE_AREA_NAME IN ('Baldy Mountain', 'Kootenay Pass')"""
uppper_fraser_line_q="""SNOWMOBILE_TRAIL_NAME IN ('Hungry Raven Access Trail', 'Upper Fraser/Quesnel Access Trail', 'Wolverine Access Trail')"""
upper_fraser_poly_q="""SNOWMOBILE_AREA_NAME IN ('Dore River', 'Big Bell Mountain', 'Cariboo River South', 'Pinkerton Peak', 'Suger Bowl Mtn North', 'Castle Creek', 'Stephenie Creek', 'Goat River', 'Narrow Lake North', 'Grizzly Bear Creek', 'Slim Creek', 'Cariboo River', 'Everett Creek', 'Suger Bowl Mtn South', 'Castle Creek Upper', 'Milk River', 'Tumuch Lake','George Mountain')"""
wells_gray_thomp_line_q="""SNOWMOBILE_TRAIL_NAME IN ('North Blue River Access Trail', 'Coulee Access Trail ', 'Allan-Oasis Access Trail', 'Groundhog Access Trail', 'Coulee North Access Trail', 'Bone Creek Glacier Access Trail', 'Bone Access Trail', 'Allan Access Trail', 'Allan Access Trail', 'Maxwell Access Trail', 'Maxwell Access Trail', 'Reg Christie Access Trail', 'Reg Christie Access Trail',
                        'Lion Access Trail', 'Lion Access Trail', 'Chappell Access Trail', 'Chappell Access Trail', 'Chappell Access Trail', 'Lower Bone Lookout Trail', 'Bone Creek Glacier Access Trail', 'Foam Creek Access Trail')"""
wells_gray_thomp_poly_q="""SNOWMOBILE_AREA_NAME IN ('Reg-Christie Riding Area', 'Foam Creek Riding Area', 'White-McRae Waikiki Riding Area', 'Paradise Riding Area', 'Holy Grail Riding Area', 'Chappell Riding Area', 'Trophy Plateau Riding Area', 'Salmon Creek Riding Area', 'Coulees Riding Area ', 'Dominion Mtn/Mt Cheadle', 'Allan-Oasis Riding Area', 'Groundhog Riding Area', 'Bone Creek Riding Area',
                        'Bone Creek Riding Area', 'Thunder-Cook Riding Area', 'Dominion Mtn/Mt Cheadle', 'Groundhog - Avola', 'North Blue River West', 'North Blue River', 'Raft Mtn.', 'Foam Creek', 'Groundhog Mountain East', 'Lyon Creek', 'Reg Christie North', 'Oasis, Allan, Canoe', 'White-Macrae', 'West Raft River', 'Horsehoe')"""
snowmobile_slosures_all_line_q="""all"""
snowmobile_slosures_all_poly_q="""all"""

sql_dict={'central_kootenay':[cent_koot_poly_q,cent_koot_line_q],
          'hart_ranges':[hart_range_poly_q,hart_range_line_q],
          'northern_rockies':[n_rockies_poly_q,n_rockies_line_q],
          'quesnel_highlands':[quesnel_high_poly_q,quesnel_high_line_q],
          'revelstoke_shuswap':[revelstoke_poly_q,revelstoke_line_q],
          'southeast_kootenay':[se_koot_poly_q,se_koot_line_q],
          'southwest_kootenay':[sw_koot_poly_q,sw_koot_line_q],
          'upper_fraser':[upper_fraser_poly_q,uppper_fraser_line_q],
          'wells_gray_thompson':[wells_gray_thomp_poly_q,wells_gray_thomp_line_q],
          'all':[snowmobile_slosures_all_poly_q,snowmobile_slosures_all_line_q]
          }

for folder in [kml_out, gpx_out]:
        if not os.path.exists(folder):
            os.mkdir(folder)

def ensure_closed(coords):
    if coords[0] != coords[-1]:
        return list(coords) + [coords[0]]
    return coords

def export_kml_from_queries(sql_dict, connection, kml_out):
    """
    Export combined KML from SQL queries with all attributes included and specific colors based on attributes.
    Handles Polygon, MultiPolygon, LineString, and MultiLineString geometries.
    """
    for region, queries in sql_dict.items():
        kml = simplekml.Kml()
        poly_query, line_query = queries

        # schema = kml.newschema(name="")
        # schema.newsimplefield(name="SNOWMOBILE_MGMT_AREA_ID", type="int", displayname="Snowmobile Management Area ID")
        # schema.newsimplefield(name="SNOWMOBILE_AREA_NAME", type="string", displayname="Snowmobile Management Area Name")
        # schema.newsimplefield(name="AREA_MANAGEMENT_CLASS", type="string", displayname="Area Management Class")
        # schema.newsimplefield(name="AREA_TIMING_RESTRICTIONS", type="string", displayname="Area Timing Restrictions")
        # schema.newsimplefield(name="AREA_ACCESS_RATIONALE", type="string", displayname="Access Rationale")
        # schema.newsimplefield(name="AREA_FEATURE_NOTES", type="string", displayname="Feature Notes")
        # schema.newsimplefield(name="AREA_USE", type="string", displayname="Use")
        # schema.newsimplefield(name="AREA_POLYGON_RETIRED_DATE", type="string", displayname="Area Retired Date") 
        # schema.newsimplefield(name="FEATURE_CODE", type="string", displayname="Feature Code")
        # schema.newsimplefield(name="OBJECTID", type="string", displayname="Object ID")
        # schema.newsimplefield(name="SE_ANNO_CAD_DATA", type="string", displayname="CAD Data")
        # schema.newsimplefield(name="FEATURE_AREA_SQM", type="float", displayname="Area (sqm)")
        # schema.newsimplefield(name="FEATURE_LENGTH_M", type="float", displayname="Length (m)")
        # schema.newsimplefield(name="SNOWMOBILE_MGMT_TRAIL_ID", type="int", displayname="Snowmobile Management Trail ID")
        # schema.newsimplefield(name="SNOWMOBILE_MGMT_TRAIL_ID", type="string", displayname="Snowmobile Management Trail Name")
        # schema.newsimplefield(name="AREA_MANAGEMENT_CLASS", type="string", displayname="Trail Management Class")
        # schema.newsimplefield(name="TRAIL_TIMING_RESTRICTIONS", type="string", displayname="Trail Timing Restrictions")
        # schema.newsimplefield(name="TRAIL_RETIRED_DATE", type="string", displayname="Trail Retired Date") 

        # Process polygons and multipolygons
        if poly_query:
            if poly_query == """all""":
                cursor = connection.cursor()
                cursor.execute(f"""
                    SELECT SDO_UTIL.TO_WKTGEOMETRY(SDO_CS.TRANSFORM(GEOMETRY, 4326)) AS WKT_GEOMETRY, S.*
                    FROM WHSE_WILDLIFE_INVENTORY.AMA_SNOWMOBILE_MGMT_AREAS_SP S
                    WHERE AREA_POLYGON_RETIRED_DATE IS NULL
                """)
            else:
                cursor = connection.cursor()
                cursor.execute(f"""
                    SELECT SDO_UTIL.TO_WKTGEOMETRY(SDO_CS.TRANSFORM(GEOMETRY, 4326)) AS WKT_GEOMETRY, S.*
                    FROM WHSE_WILDLIFE_INVENTORY.AMA_SNOWMOBILE_MGMT_AREAS_SP S
                    WHERE {poly_query} AND AREA_POLYGON_RETIRED_DATE IS NULL
                """)
            columns = [col[0] for col in cursor.description]
            for row in cursor:
                row_dict = dict(zip(columns, row))
                wkt_geom = str(row_dict['WKT_GEOMETRY'])
                attribute = str(row_dict['AREA_TIMING_RESTRICTIONS']).strip().lower()
                area_name = row_dict['SNOWMOBILE_AREA_NAME']
                shapely_geom = load_wkt(wkt_geom)

                # Determine polygon color based on attribute
                if attribute in ['closed to snowmobiles under sma', 'closed year round without a permit', 'closed year round']:
                    polygon_color = simplekml.Color.rgb(168, 0, 0, 127)
                elif attribute == 'open':
                    polygon_color = simplekml.Color.rgb(0, 31, 237, 127)
                elif attribute == 'open - limited':
                    polygon_color = simplekml.Color.rgb(0, 169, 230, 127)
                elif attribute in ['seasonal closure jan 1 to april 15', 'seasonal closure jan 15 to sept 30']:
                    polygon_color = simplekml.Color.rgb(255, 0, 197, 127)
                elif attribute == 'snowmobiles allowed only dec 1 to april 30':
                    polygon_color = simplekml.Color.rgb(230, 230, 0, 127)
                else:
                    polygon_color = simplekml.Color.rgb(0, 0, 0, 127)

                # # Format description as HTML table, skip WKT_GEOMETRY
                # desc_rows = [
                #     f"<tr><td><b>{key}</b></td><td>{value}</td></tr>"
                #     for key, value in row_dict.items() if key != 'WKT_GEOMETRY'
                # ]
                # formatted_description = "<table>{}</table>".format("".join(desc_rows))


                # Handle Polygon and MultiPolygon
                if shapely_geom.geom_type == "Polygon":
                    polygons = [shapely_geom]
                elif shapely_geom.geom_type == "MultiPolygon":
                    polygons = list(shapely_geom.geoms)
                else:
                    print(f"Unsupported geometry type for area: {shapely_geom.geom_type}")
                    continue

                for i, poly in enumerate(polygons):
                    pol = kml.newpolygon(
                        name=f"{area_name} (part {i+1})" if len(polygons) > 1 else area_name                        
                    )
                    # print(f"Polygon {i}: {len(poly.interiors)} holes")
                    # print(type(poly.exterior.coords), poly.exterior.coords)
                    
                    pol.outerboundaryis = [(lon, lat, 0) for lon, lat in ensure_closed(poly.exterior.coords)]
                    holes = [
                        [(lon, lat, 0) for lon, lat in ensure_closed(interior.coords)]
                        for interior in poly.interiors
                        if len(interior.coords) >= 4
                    ]
                    if holes:
                        pol.innerboundaryis = holes
                    pol.style.polystyle.color = polygon_color
                    pol.style.polystyle.fill = 1
                    pol.style.polystyle.outline = 1
                    pol.style.linestyle.color = simplekml.Color.black
                    pol.style.linestyle.width = 2
                    pol.altitudemode = simplekml.AltitudeMode.clamptoground
                    # pol.extendeddata.schemadata.schemaurl = schema.id
                    #schema fields
                    # pol.extendeddata.schemadata.newsimpledata("SNOWMOBILE_MGMT_AREA_ID", row_dict["SNOWMOBILE_MGMT_AREA_ID"])
                    # pol.extendeddata.schemadata.newsimpledata("SNOWMOBILE_AREA_NAME", row_dict["SNOWMOBILE_AREA_NAME"])
                    # pol.extendeddata.schemadata.newsimpledata("AREA_MANAGEMENT_CLASS", row_dict["AREA_MANAGEMENT_CLASS"])
                    # pol.extendeddata.schemadata.newsimpledata("AREA_TIMING_RESTRICTIONS", row_dict["AREA_TIMING_RESTRICTIONS"])
                    # pol.extendeddata.schemadata.newsimpledata("AREA_ACCESS_RATIONALE", row_dict["AREA_ACCESS_RATIONALE"])
                    # pol.extendeddata.schemadata.newsimpledata("AREA_FEATURE_NOTES", row_dict["AREA_FEATURE_NOTES"])
                    # pol.extendeddata.schemadata.newsimpledata("AREA_USE", row_dict["AREA_USE"])
                    # pol.extendeddata.schemadata.newsimpledata("AREA_POLYGON_RETIRED_DATE", str(row_dict["AREA_POLYGON_RETIRED_DATE"]))
                    # pol.extendeddata.schemadata.newsimpledata("FEATURE_CODE", row_dict["FEATURE_CODE"])
                    # pol.extendeddata.schemadata.newsimpledata("OBJECTID", row_dict["OBJECTID"])
                    # pol.extendeddata.schemadata.newsimpledata("SE_ANNO_CAD_DATA", row_dict["SE_ANNO_CAD_DATA"])
                    # pol.extendeddata.schemadata.newsimpledata("FEATURE_AREA_SQM", row_dict["FEATURE_AREA_SQM"])
                    # pol.extendeddata.schemadata.newsimpledata("FEATURE_LENGTH_M", row_dict["FEATURE_LENGTH_M"])
                    # Create HTML description table with all attributes
                    description_html = "<table style='width:100%; border-collapse:collapse;'>"
                    description_html += "<tr><th style='text-align:left; padding:5px; background-color:#f0f0f0;'>Attribute</th><th style='text-align:left; padding:5px; background-color:#f0f0f0;'>Value</th></tr>"
                    
                    # Add all attributes to the description table
                    for key, value in row_dict.items():
                        if key == "AREA_FEATURE_NOTES":
                            # REPLACE HREF IN FIELD TO OPEN IN EXTERNAL BROWSER
                            if value is not None:
                                # Use regex to handle different href formats (with or without quotes)
                                value = str(value)
                                # Try multiple approaches to encourage external browser opening- does not work in google earth unfortunately
                                # Add both target and additional attributes that some applications recognize
                                # value = re.sub(
                                #     r'<a\s+([^>]*?)href=', r'<a \1target="_blank" rel="external" href=', value, flags=re.IGNORECASE)
                                value = re.sub(
                                        r'<a[^>]*href=[\'"]([^\'"]+)[\'"][^>]*>(.*?)</a>',
                                        r'\2 (\1)',
                                        value,
                                        flags=re.IGNORECASE
                                        
                                )
                                                    # Append message if any URL is present
                                if "http" in value:
                                    value += " — Please copy and paste the link into your web browser."
                                    
                                description_html += f"<tr><td style='padding:3px; border-bottom:1px solid #ddd;'><b>{key}</b></td><td style='padding:3px; border-bottom:1px solid #ddd;'>{value}</td></tr>"
                        elif key != "WKT_GEOMETRY" and value is not None:  # Skip geometry and null values
                            description_html += f"<tr><td style='padding:3px; border-bottom:1px solid #ddd;'><b>{key}</b></td><td style='padding:3px; border-bottom:1px solid #ddd;'>{value}</td></tr>"

                    description_html += "</table>"
                    
                    # Set the formatted description
                    pol.description = description_html
                    pol.snippet = simplekml.Snippet("")
            cursor.close()

        # Process lines and multilines
        if line_query:
            if line_query =="""all""":
                cursor = connection.cursor()
                cursor.execute(f"""
                    SELECT SDO_UTIL.TO_WKTGEOMETRY(SDO_CS.TRANSFORM(GEOMETRY, 4326)) AS WKT_GEOMETRY, S.*
                    FROM WHSE_WILDLIFE_INVENTORY.AMA_SNOWMOBILE_MGMT_TRAILS_SP S
                    WHERE TRAIL_RETIRED_DATE IS NULL 
                """)
            else:
                cursor = connection.cursor()
                cursor.execute(f"""
                    SELECT SDO_UTIL.TO_WKTGEOMETRY(SDO_CS.TRANSFORM(GEOMETRY, 4326)) AS WKT_GEOMETRY, S.*
                    FROM WHSE_WILDLIFE_INVENTORY.AMA_SNOWMOBILE_MGMT_TRAILS_SP S
                    WHERE {line_query} AND TRAIL_RETIRED_DATE IS NULL 
                """)
            columns = [col[0] for col in cursor.description]
            for row in cursor:
                row_dict = dict(zip(columns, row))
                wkt_geom = str(row_dict['WKT_GEOMETRY'])
                attribute = str(row_dict['TRAIL_TIMING_RESTRICTIONS']).strip().lower()
                trail_name = row_dict['SNOWMOBILE_TRAIL_NAME']
                shapely_geom = load_wkt(wkt_geom)

                # Determine line color based on attribute
                if attribute in ['trails open year round']:
                    line_color = simplekml.Color.rgb(230, 0, 169, 255)
                elif attribute == 'trails open december 1 - may 31':
                    line_color = simplekml.Color.rgb(0, 230, 230, 255)
                elif attribute == 'trails open november 1 - april 15':
                    line_color = simplekml.Color.rgb(0, 170, 255, 255)
                elif attribute == 'trails open november 1 - may 31':
                    line_color = simplekml.Color.rgb(0, 152, 230, 255)
                else:
                    line_color = simplekml.Color.rgb(0, 0, 255, 255)

                # # Format description as HTML table, skip WKT_GEOMETRY
                # desc_rows = [
                #     f"<tr><td><b>{key}</b></td><td>{value}</td></tr>"
                #     for key, value in row_dict.items() if key != 'WKT_GEOMETRY'
                # ]
                # formatted_description = "<table>{}</table>".format("".join(desc_rows))

                # Handle LineString and MultiLineString
                if shapely_geom.geom_type == "LineString":
                    lines = [shapely_geom]
                elif shapely_geom.geom_type == "MultiLineString":
                    lines = list(shapely_geom.geoms)
                else:
                    print(f"Unsupported geometry type for trail: {shapely_geom.geom_type}")
                    continue

                for i, line_geom in enumerate(lines):
                    coords = [(lon, lat, 0) for lon, lat in line_geom.coords]
                    line = kml.newlinestring(
                        name=f"{trail_name} (part {i+1})" if len(lines) > 1 else trail_name,
                        # description=formatted_description
                    )
                    # line.extendeddata.schemadata.newsimpledata("SNOWMOBILE_MGMT_TRAIL_ID", row_dict["SNOWMOBILE_MGMT_TRAIL_ID"])
                    # line.extendeddata.schemadata.newsimpledata("SNOWMOBILE_TRAIL_NAME", row_dict["SNOWMOBILE_TRAIL_NAME"])
                    # line.extendeddata.schemadata.newsimpledata("TRAIL_MANAGEMENT_CLASS", row_dict["TRAIL_MANAGEMENT_CLASS"])
                    # line.extendeddata.schemadata.newsimpledata("TRAIL_TIMING_RESTRICTIONS", row_dict["TRAIL_TIMING_RESTRICTIONS"])
                    # line.extendeddata.schemadata.newsimpledata("TRAIL_RETIRED_DATE", row_dict["TRAIL_RETIRED_DATE"])
                    # line.extendeddata.schemadata.newsimpledata("FEATURE_CODE", row_dict["FEATURE_CODE"])
                    # line.extendeddata.schemadata.newsimpledata("OBJECTID", row_dict["OBJECTID"])
                    # line.extendeddata.schemadata.newsimpledata("SE_ANNO_CAD_DATA", row_dict["SE_ANNO_CAD_DATA"])
                    # line.extendeddata.schemadata.newsimpledata("FEATURE_LENGTH_M", row_dict["FEATURE_LENGTH_M"])
                    line.coords = coords
                    line.style.linestyle.color = line_color
                    line.style.linestyle.width = 2

                    # Create HTML description table with all attributes
                    description_html = "<table style='width:100%; border-collapse:collapse;'>"
                    description_html += "<tr><th style='text-align:left; padding:5px; background-color:#f0f0f0;'>Attribute</th><th style='text-align:left; padding:5px; background-color:#f0f0f0;'>Value</th></tr>"
                    
                    # Add all attributes to the description table
                    for key, value in row_dict.items():
                        if key != "WKT_GEOMETRY" and value is not None:  # Skip geometry and null values
                            description_html += f"<tr><td style='padding:3px; border-bottom:1px solid #ddd;'><b>{key}</b></td><td style='padding:3px; border-bottom:1px solid #ddd;'>{value}</td></tr>"
                    
                    description_html += "</table>"
                    
                    # Set the formatted description
                    line.description = description_html
                    line.snippet = simplekml.Snippet("")

            cursor.close()

        # Save the KML file
        kml_file_path = os.path.join(kml_out, f"snowmobile_closure_{region}_{str(date.today())}.kml")
        kml.save(kml_file_path)
        print(f"KML exported to {kml_file_path}")


def export_gpx_from_queries(sql_dict, connection, gpx_out):
    for region, queries in sql_dict.items():
        poly_query, line_query = queries

        print(f"Processing region: {region}")
        print(f"Polygon query: {poly_query}")
        print(f"Line query: {line_query}")

        gpx = gpxpy.gpx.GPX()

        # Process polygons as tracks (using exterior ring)
        if poly_query:
            if poly_query == """all""":
                cursor = connection.cursor()
                cursor.execute(f"""
                    SELECT SDO_UTIL.TO_WKTGEOMETRY(SDO_CS.TRANSFORM(GEOMETRY, 4326)) AS WKT_GEOMETRY, S.*
                    FROM WHSE_WILDLIFE_INVENTORY.AMA_SNOWMOBILE_MGMT_AREAS_SP S
                    WHERE AREA_POLYGON_RETIRED_DATE IS NULL
                """)
            else:
                cursor = connection.cursor()
                cursor.execute(f"""
                    SELECT SDO_UTIL.TO_WKTGEOMETRY(SDO_CS.TRANSFORM(GEOMETRY, 4326)) AS WKT_GEOMETRY, S.*
                    FROM WHSE_WILDLIFE_INVENTORY.AMA_SNOWMOBILE_MGMT_AREAS_SP S
                    WHERE {poly_query} AND AREA_POLYGON_RETIRED_DATE IS NULL
                """)
            columns = [col[0] for col in cursor.description]
            for row in cursor:
                row_dict = dict(zip(columns, row))
                wkt_geom = str(row_dict['WKT_GEOMETRY'])
                area_name = row_dict['SNOWMOBILE_AREA_NAME']
                timing = row_dict.get('AREA_TIMING_RESTRICTIONS', '')

                # Only include area_name and timing in description
                formatted_description = f"Area: {area_name}\nTiming: {timing}"

                shapely_geom = load_wkt(wkt_geom)
                if shapely_geom.geom_type == "Polygon":
                    coords = list(shapely_geom.exterior.coords)
                    gpx_track = gpxpy.gpx.GPXTrack(name=area_name, description=formatted_description)
                    gpx_segment = gpxpy.gpx.GPXTrackSegment()
                    for lon, lat in coords:
                        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon))
                    gpx_track.segments.append(gpx_segment)
                    gpx.tracks.append(gpx_track)

                elif shapely_geom.geom_type == "MultiPolygon":
                    for polygon in shapely_geom.geoms:
                        gpx_segment = gpxpy.gpx.GPXTrackSegment()
                        coords = list(polygon.exterior.coords)
                        for lon, lat in coords:
                            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon))
                        gpx_track = gpxpy.gpx.GPXTrack(name=area_name, description=formatted_description)
                        gpx_track.segments.append(gpx_segment)
                        gpx.tracks.append(gpx_track)

            cursor.close()

        # Process lines as tracks
        if line_query:
            if line_query =="""all""":
                cursor = connection.cursor()
                cursor.execute(f"""
                    SELECT SDO_UTIL.TO_WKTGEOMETRY(SDO_CS.TRANSFORM(GEOMETRY, 4326)) AS WKT_GEOMETRY, S.*
                    FROM WHSE_WILDLIFE_INVENTORY.AMA_SNOWMOBILE_MGMT_TRAILS_SP S
                    WHERE TRAIL_RETIRED_DATE IS NULL 
                """)
            else:
                cursor = connection.cursor()
                cursor.execute(f"""
                    SELECT SDO_UTIL.TO_WKTGEOMETRY(SDO_CS.TRANSFORM(GEOMETRY, 4326)) AS WKT_GEOMETRY, S.*
                    FROM WHSE_WILDLIFE_INVENTORY.AMA_SNOWMOBILE_MGMT_TRAILS_SP S
                    WHERE {line_query} AND TRAIL_RETIRED_DATE IS NULL 
                """)
            columns = [col[0] for col in cursor.description]
            for row in cursor:
                row_dict = dict(zip(columns, row))
                wkt_geom = str(row_dict['WKT_GEOMETRY'])
                trail_name = row_dict['SNOWMOBILE_TRAIL_NAME']
                timing = row_dict.get('TRAIL_TIMING_RESTRICTIONS', '')

                # Only include trail_name and timing in description
                formatted_description = f"Trail: {trail_name}\nTiming: {timing}"

                shapely_geom = load_wkt(wkt_geom)
                if shapely_geom.geom_type == "LineString":
                    coords = list(shapely_geom.coords)
                    gpx_track = gpxpy.gpx.GPXTrack(name=trail_name, description=formatted_description)
                    gpx_segment = gpxpy.gpx.GPXTrackSegment()
                    for lon, lat in coords:
                        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon))
                    gpx_track.segments.append(gpx_segment)
                    gpx.tracks.append(gpx_track)
            cursor.close()

        # Save the GPX file
        gpx_file_path = os.path.join(gpx_out, f"snowmobile_closure_{region}_{str(date.today())}.gpx")
        with open(gpx_file_path, "w") as f:
            f.write(gpx.to_xml())
        print(f"GPX exported to {gpx_file_path}")
    


export_kml_from_queries(sql_dict, connection, kml_out)
export_gpx_from_queries(sql_dict, connection, gpx_out)

