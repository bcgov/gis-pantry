r"""

Original Author: jeff.kruys@gov.bc.ca (FIRB) 

Created on:
2024-08-12

Purpose:
This script creates Geomark URLs for each feature in an input dataset, and 
writes them to a new field named GeomarkURL. It can be run at the command
prompt on a system with ArcGIS Pro installed, or directly in ArcGIS Pro in a 
script tool named Add_Geomark_URL in a toolbox named Add_Geomark_URL.atbx.

Usage:
add_geomark_py3.py lyr

Positional Arguments:
   lyr              Input layer

Requirements:
ArcGIS Pro

Example Input:
X:\fullpath\add_geomark_py3.py Y:\fullpath\lyr

History
2024-08-12 (JK): Created script.
2024-11-04 (JK): Updated to use http.client instead of requests module to make 
                 API calls; requests module seems to have issues when run in a 
                 GTS session.
2024-11-08 (JK): Creates the new field with name GeomarkURL instead of 
                 Geomark_URL to fit in shapefile 10-character field name limit.
"""

import arcpy
import http.client
import urllib
import time
import json

def add_geomark_url(in_fc):

    # Get the spatial reference of the input dataset
    srid = arcpy.da.Describe(in_fc)["spatialReference"].factoryCode
    arcpy.AddMessage(time.strftime('%Y-%m-%d %H:%M:%S : ') + f"Spatial reference code of input dataset: {srid}")

    # Add GeomarkURL field if it doesn't already exist
    flist = [f.name for f in arcpy.ListFields(in_fc)]
    if "GeomarkURL" not in flist:
        arcpy.management.AddField(in_table=in_fc, field_name="GeomarkURL", field_type="TEXT", field_length=100)
        arcpy.AddMessage(time.strftime('%Y-%m-%d %H:%M:%S : ') + "Added GeomarkURL field to input layer")
    else:
        arcpy.AddMessage(time.strftime('%Y-%m-%d %H:%M:%S : ') + "GeomarkURL field already exists in input layer")

    # Read each record, send API request to create Geomark URL, write the returned URL to the GeomarkURL field
    row_total = int(arcpy.GetCount_management(in_fc).getOutput(0))
    read_count = 0
    update_count = 0
    arcpy.AddMessage(time.strftime('%Y-%m-%d %H:%M:%S : ') + f"Processing {row_total} feature(s) of input dataset")
    with arcpy.da.UpdateCursor(in_fc, ["GeomarkURL", "SHAPE@"]) as cursor:
        for row in cursor:
            read_count += 1
            exist_url = row[0]
            if exist_url is None or exist_url.startswith("Geomark Web Service request failed"):
                geom = row[1]
                if geom is None:
                    row[0] = "Null geometry"
                else:
                    
                    # Construct a POST request via http.client module - it works better than requests module when
                    # sent from a GTS session, and should work for anyone outside GTS too
                    conn = http.client.HTTPSConnection("apps.gov.bc.ca")

                    # payload string should have been easy to build with the following code:
                    # payload_dict = {"bufferSegments": 8, "body": geom_wkt, "srid": srid, "bufferMetres": None, etc. }
                    # payload = urllib.parse.urlencode(payload_dict)

                    # But I could not get this working. Instead I'm only urlencode'ing the geometry and srid, and 
                    # hardcoding the rest of the string as follows, and it seems to work:
                    geom_wkt = geom.WKT
                    geom_dict = {"body": geom_wkt, "srid": srid}
                    geom_dict_urle = urllib.parse.urlencode(geom_dict)
                    payload = fr"bufferSegments=8&{geom_dict_urle}&bufferMetres=&callback=&failureRedirectUrl="
                    payload += fr"&bufferJoin=ROUND&bufferMitreLimit=5&bufferCap=ROUND&redirectUrl=&resultFormat="
                    payload += fr"&format=wkt&allowOverlap=false"
                    headers = { 'content-type': "application/x-www-form-urlencoded" }
                    conn.request("POST", "/pub/geomark/geomarks/new", payload, headers)
                    res = conn.getresponse().read().decode()
                    res_received = True
                    try:
                        res_dict = json.loads(res.replace(";", "").replace("(", "").replace(")", ""))
                    except:
                        res_received = False
                        row[0] = "Geomark Web Service request failed: no response received"
                    if res_received:
                        if isinstance(res_dict, dict):
                            if "url" in res_dict:
                                if res_dict["url"].startswith("https://apps.gov.bc.ca/pub/geomark/geomarks/gm-"):
                                    row[0] = res_dict["url"]
                                    update_count += 1
                                else:
                                    row[0] = "Geomark Web Service request failed: URL in response is not a Geomark"
                            else:
                                row[0] = "Geomark Web Service request failed: response did not contain a URL"
                        else:
                            row[0] = "Geomark Web Service request failed: response could not be loaded to a JSON object"
                    del conn
                cursor.updateRow(row)

            if read_count % 10 == 0 or read_count == row_total:
                arcpy.AddMessage(time.strftime('%Y-%m-%d %H:%M:%S : ') + f"Processed {read_count} of {row_total} "
                      f"feature(s) and added Geomark URL to {update_count} feature(s)")

if __name__ == "__main__":
    in_fc = arcpy.GetParameterAsText(0)
    add_geomark_url(in_fc)
