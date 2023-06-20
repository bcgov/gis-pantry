'''
BC Hydro Outages

Written by: Michael Dykes (michael.dykes@gov.bc.ca) and Paulina Marczak (paulina.marczak@gov.bc.ca)
Created: May 27, 2021

Purpose: Grab BC Hydro Web Content (from https://www.bchydro.com/power-outages/app/outage-map.html) and update ArcGIS Online Hosted Feature Layer
'''

# Import libraries/modules
import logging, os, sys, getpass, requests, datetime, json
from arcgis.gis import GIS
from arcgis import geometry, features
    
#Set logging level (NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL)
logging_level = logging.INFO

def Set_Logging_Level(logging_level):
    '''Set logging level from logging_level variable to send messages to the console'''
    global log
    # Setup logger and set logging level based off logging_level parameter
    logging.basicConfig(level=logging_level)
    # Set logger name to script filename (for display in console)
    log = logging.getLogger(f"{os.path.basename(os.path.splitext(__file__)[0])}-logger")
    # Get logging level as string for display in log 
    logging_level_str = logging.getLevelName(logging_level)
    log.info(f"Script console logging level set to - {logging_level_str}")

def Find_Config_File():
    '''Find config.json file that holds secrets (paths/itemIDs/etc) to be used in this script'''
    try:
        # Find 'config.json' file that should be stored in the same directory as this script
        config_file = os.path.join(os.path.dirname(__file__),'config.json')
        # Open config file as json object and store as conf variable for use elsewhere in script
        with open(config_file) as json_conf :
            global conf 
            conf = json.load(json_conf)
        log.info("Config file found")
    except:
        # No config file is found, shutdown script
        log.critical("No config file found - Stopping script")
        sys.exit(1)

def Create_AGO_Connection():
    '''Create connection to ArcGIS Online, creates a global variable "gis"'''
    log.info("Creating connection to ArcGIS Online...")
    if "AGO_Portal_URL" in conf:
        portal_url = conf["AGO_Portal_URL"]
    else:
        log.critical("No AGO Portal URL found in config.json - Stopping script")
        sys.exit(1)
    if 'JENKINS_URL' in os.environ:
        portal_username = sys.argv[1]
        portal_password = sys.argv[2]
        log.info("System arguement AGO credentials found")
    else:
        try:
            portal_username = os.getenv('GEOHUB_USERNAME')
            portal_password = os.getenv('GEOHUB_PASSWORD')
            log.info("Environment variable AGO credentials found")
        except:
            log.info("*User input required*")
            portal_username = input("Enter AGO username:")
            portal_password = getpass.getpass(prompt='Enter AGO password:')
            
    global gis
    gis = GIS(portal_url, username=portal_username, password=portal_password, expiration=9999)
    log.info("Connection to ArcGIS Online created successfully")

def AGO_Delete_and_Truncate(AGO_data_item):
    '''Delete existing features and truncate (which resets ObjectID) a table or hosted feature layer'''
    attempts = 0
    success = False
    # 5 attempts to connect and update the layer 
    while attempts < 5 and not success:
        try:
            feature_layer = AGO_data_item.layers[0]
            feature_count = feature_layer.query(where="objectid >= 0", return_count_only=True)
            feature_layer.delete_features(where="objectid >= 0")
            log.info(f"Deleted {feature_count} existing features from - ItemID: {AGO_data_item.id}")
            success = True
            try:
                feature_layer.manager.truncate()
                log.info(f"Data truncated")
            except:
                log.warning("Truncate failed")
        except:
            log.warning(f"Re-Attempting Delete Existing Features. Attempt Number {attempts}")
            attempts += 1
            Create_AGO_Connection()
            if attempts == 5:
                log.critical(f"***No More Attempts Left. AGO Update Failed***")
                sys.exit(1)
            
def Connect_to_Website_or_API_JSON(url,encode=False):
    '''Connect to a website or API and retrieve data from it as JSON'''
    x = requests.get(url)
    if encode:
        x.encoding = x.apparent_encoding
    # If good web return/connection
    if x.status_code == 200:
        # If data that can be read in json is returned
        try:
            if x and x.json():
                return x.json()
        except:
            log.critical(f"Website or API Data Not Found - Stopping script")
            sys.exit(1)
    else:
        log.critical(f"Connection to Website or API Failed - Stopping script")
        sys.exit(1)

def Update_BCHydro_Outages_AGO(bchydro_data,bchydro_itemid):
    '''Clear existing features, and append new features to the BC Hydro Outages hosted feature layer in AGO'''
    if bchydro_data:
        log.info(f"{len(bchydro_data)} BC Hydro Outages found")
        # Get Hosted Feature Layers to Update
        bchydro_item = gis.content.get(bchydro_itemid)
        AGO_Delete_and_Truncate(bchydro_item)

        attempts = 0
        success = False
        # 5 attempts to connect and update the layer 
        while attempts < 5 and not success:
            try:
                # Iterate through bchydro JSON items (each outage is its own item)
                n = 0
                for row in bchydro_data:
                    log.debug(f"Append new feature #{n}")
                    # Build LAT/LONG list pairings from unseparated list of LAT/LONGS from website JSON
                    latlong_list = [list(a) for a in zip(row["polygon"][::2],row["polygon"][1::2])]
                    # Create Polygon Geometry WKID:4326 = WGS 1984
                    geom = geometry.Geometry({"type": "Polygon", "rings" : [latlong_list],"spatialReference" : {"wkid" : 4326}})
                    # Build attributes to populate feature attribute table, check for none values in the EST_TIME_ON, OFFTIME and UPDATED date fields
                    attributes = {"OUTAGE_ID": row['id'], 
                            "GIS_ID": row['gisId'],
                            "REGION_ID": row['regionId'],
                            "REGION": row['regionName'],
                            "MUNI": row['municipality'],
                            "DETAILS": row['area'],
                            "CAUSE": row['cause'],
                            "AFFECTED":  row['numCustomersOut'],
                            "CREW_STATUS": row['crewStatusDescription'],
                            "EST_TIME_ON": datetime.datetime.utcfromtimestamp(row['dateOn']/1000).replace(tzinfo=datetime.timezone.utc).astimezone(tz=None) if row['dateOn'] else None,
                            "OFFTIME": datetime.datetime.utcfromtimestamp(row['dateOff']/1000).replace(tzinfo=datetime.timezone.utc).astimezone(tz=None) if row['dateOff'] else None,
                            "UPDATED": datetime.datetime.utcfromtimestamp(row['lastUpdated']/1000).replace(tzinfo=datetime.timezone.utc).astimezone(tz=None) if row['lastUpdated'] else None,
                            "CREW_ETA": datetime.datetime.utcfromtimestamp(row['crewEta']/1000).replace(tzinfo=datetime.timezone.utc).astimezone(tz=None) if row['crewEta'] else None,
                            "CREW_ETR": datetime.datetime.utcfromtimestamp(row['crewEtr']/1000).replace(tzinfo=datetime.timezone.utc).astimezone(tz=None) if row['crewEtr'] else None,
                            "SHOW_ETA": row['showEta'],
                            "SHOW_ETR": row['showEtr']}
                    # Create new feature
                    newfeature = features.Feature(geom,attributes)
                    # Add feature to existing hosted feature layer
                    result = bchydro_item.layers[0].edit_features(adds = [newfeature])
                    log.debug(result)
                    success = True
                    n+=1
                log.info(f"Finished creating {n} new BC Hydro Outage features in AGO - ItemID: {bchydro_itemid}")

            # If attempt fails, retry attempt (up to 5 times then exit script if unsuccessful)
            except:
                log.warning(f"Re-Attempting AGO Update. Attempt Number {attempts}")
                attempts += 1
                Create_AGO_Connection()
                if attempts == 5:
                    log.critical(f"***No More Attempts Left. AGO Update Failed***")
                    sys.exit(1)
    else:
        log.info("No BC Hydro Outages found")

def main():
    '''Run code (if executed as script)'''
    Set_Logging_Level(logging_level)
    Find_Config_File()
    bchydro_outages_url = r"https://www.bchydro.com/power-outages/app/outages-map-data.json"
    bchydro_data = Connect_to_Website_or_API_JSON(bchydro_outages_url)
    Create_AGO_Connection()
    HydroOutages_ItemID = conf["HydroOutages_ItemID"]
    Update_BCHydro_Outages_AGO(bchydro_data,HydroOutages_ItemID)
    HydroOutagesLFN_ItemID = conf["HydroOutagesLFN_ItemID"]
    Update_BCHydro_Outages_AGO(bchydro_data,HydroOutagesLFN_ItemID)
    gis._con.logout()
    log.info("**Script completed**")

if __name__ == "__main__":
    main()
