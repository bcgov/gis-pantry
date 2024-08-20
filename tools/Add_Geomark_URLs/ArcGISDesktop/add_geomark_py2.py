r"""

Original Author: jeff.kruys@gov.bc.ca (FIRB) 

Created on:
2024-08-13

Purpose:
This script creates Geomark URLs for each feature in an input dataset, and 
writes them to a new field named Geomark_URL. It can be run at the command
prompt on a system with ArcGIS Pro installed, or directly in ArcGIS Desktop 
10.x in a script tool named Add_Geomark_URL in a toolbox named 
Add_Geomark_URL.tbx.

Usage:
add_geomark_py2.py lyr

Positional Arguments:
   lyr              Input layer

Requirements:
ArcGIS Pro

Optional Arguments:
  -h, --help       show this help message and exit
  -l, --level      log level messages to display; Default: 20 - INFO
  -ld, --log_dir   path to directory for output log file

Example Input:
X:\fullpath\add_geomark_py2.py Y:\fullpath\lyr

History
2024-08-13 (JK): Created script.
"""

import arcpy, urllib2, time, sys
from urllib import urlencode

def add_geomark_url(in_fc):

    # Get the spatial reference of the input dataset
    srid = arcpy.Describe(in_fc).spatialReference.factoryCode
    arcpy.AddMessage(time.strftime("%Y-%m-%d %H:%M:%S : ") + "Spatial reference code of input dataset: " + str(srid))

    # Add Geomark_URL field if it doesn't already exist
    flist = [f.name for f in arcpy.ListFields(in_fc)]
    if "Geomark_URL" not in flist:
        try:
            arcpy.AddField_management(in_table=in_fc, field_name="Geomark_URL", field_type="TEXT", field_length=100)
        except:
            arcpy.AddError(time.strftime("%Y-%m-%d %H:%M:%S : ") + "Unable to add field to input dataset. Exiting.")
            sys.exit()
        arcpy.AddMessage(time.strftime("%Y-%m-%d %H:%M:%S : ") + "Added Geomark_URL field to input layer")
    else:
        arcpy.AddMessage(time.strftime("%Y-%m-%d %H:%M:%S : ") + "Geomark_URL field already exists in input layer")

    # Read each record, send request to create Geomark URL, write the returned URL to the Geomark_URL field
    row_total = int(arcpy.GetCount_management(in_fc).getOutput(0))
    read_count = 0
    update_count = 0
    arcpy.AddMessage(time.strftime("%Y-%m-%d %H:%M:%S : ") + "Processing " + str(row_total) + " feature(s) of input "
                                   "dataset")
    with arcpy.da.UpdateCursor(in_fc, ["Geomark_URL", "SHAPE@"]) as cursor:
        for row in cursor:
            read_count += 1
            exist_url = row[0]
            if exist_url is None:
                geom = row[1]
                if geom is None:
                    row[0] = "Null geometry"
                else:
                    geom_wkt = geom.WKT
                    post_url = "https://apps.gov.bc.ca/pub/geomark/geomarks/new"
                    payload = {"bufferSegments": 8, "body": geom_wkt, "bufferMetres": 0, "callback": None, 
                               "failureRedirectUrl": None, "bufferJoin": "ROUND", "bufferMitreLimit": 5, 
                               "bufferCap": "ROUND", "redirectUrl": None, "resultFormat": None, "format": "wkt", 
                               "srid": srid, "allowOverlap": "false"}
                    post = urlencode(payload)
                    req = urllib2.Request(post_url, post)
                    response = urllib2.urlopen(req)
                    if response.code == 200:
                        r = response.read()
                        out_url = r.split('"url":"')[1].split('"')[0]
                        if out_url == "https://apps.gov.bc.ca/pub/geomark/geomarks/new":
                            row[0] = "Could not create Geomark URL for this geometry"
                        else:
                            row[0] = out_url
                            update_count += 1
                    else:
                        row[0] = "Error response code " + str(response.code)
                cursor.updateRow(row)

            if read_count % 10 == 0 or read_count == row_total:
                arcpy.AddMessage(time.strftime("%Y-%m-%d %H:%M:%S : ") + "Processed " + str(read_count) + " of " + 
                                 str(row_total) + " feature(s) and added Geomark URL to " + str(update_count) + 
                                 " feature(s)")

if __name__ == "__main__":
    in_fc = arcpy.GetParameterAsText(0)
    add_geomark_url(in_fc)
