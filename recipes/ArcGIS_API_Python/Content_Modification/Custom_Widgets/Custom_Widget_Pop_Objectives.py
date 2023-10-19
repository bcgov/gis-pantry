'''
A script to generate graphs in plotly for use in the Mountain Goat SBOT

The script is intended to be run via Jenkins AFTER any survey updates (linked job)

Inputs:
    Inputs are generally set up to be generic and should be easily changed to adapt to other projects
    For Mountain Goat:
        input_datasets["dataset1"]: The management polygons containing the population estimates. Currently taken from AGO
        input_datasets["dataset2"]: contains the raw and estimate range population objectives for each area. pulled in from a csv.
        directories: object to define working/output directories
        object_properties: the attributes required to upload the datasets to object storage:
            bucket
            folder
            url
            Note that secret is taken from the external s3_credentials.json
        agol_pop_objectives: The location that the population objectives ago table is. This allows the s3 url to be served

Credentials:
    Stored externally in json. No sensitive information is stored in the script.


Output will be:
    -A series of SVG files sent to object storage
    -A table with the population numbers and a url linking to the SVG graphs
    --The table will be uploaded to AGO automatically
        The specifics are defined in:
            object_properties
            agol_pop_objectives

After the script:
    On AGO, use the Embedded Content widget type to embed the graph via the url from a table


#### Background
    Follows this tutorial: https://plotly.com/python/gauge-charts/
    requires plotly, kaleido

    setting policies for multiple items in bucket:
    https://stackoverflow.com/questions/69588432/minio-bucket-private-but-objects-public


Author:
Isaac Cave

Changelog:

2023-09-27
Minor formatting changes

2023-09-21
improved readme, made script description clearer

2023-08-29
Cleanup of unused code, added docstrings to functions

2023-06-22
Initial writing


'''

# %% Imports

import json
import os
import sys

import arcpy
from arcgis.gis import GIS
from arcgis.features import FeatureLayer

# This is used at the end of the script. Use your method for overwriting the layer on AGOL
sys.path.insert(1, r'path to overwrite method')
from overwrite_from_pro_project import overwrite_from_pro

sys.path.insert(1, r'path to credentials handling')
import credential_access as creds

# %% Inputs

input_datasets = {
    "dataset1": {
        "dataset": r"rest url for the dataset", # URL, including sublayer #
        "fields": {
            "GMUname": "PMU", # join key
            "popField": "PopEst",
            "yearField": "Year",
        }  
    }, # This will come from AGO, similar to the arcade script
    "dataset2": {
        "dataset": r"UNC path to the csv", # full path to the csv
        "fields": {
            "GMUname": "GMU", # join key
            "objectiveLow": "population_objective_lower",
            "objectiveHigh": "population_objective_upper",
            "objectiveRaw": "Population_objectives_raw",
        }
    },
}

directories = {
    "working": {
        "folder": r"UNC path to your working folder",
        "gdb": r"scratch.gdb",
    },
    "output": {
        "folder": r"UNC path to your working folder",
        "gdb": r"upload.gdb",
    },
}

object_properties = {
    "bucket": "bucket_name",
    "folder": "pub/mtn_goat/objective/svg/",
    "url": "URL",
}

agol_dataset2 = {
    "fs_id": "",
    "service_id": "",
}

# %% Functions

def recreategdb(scratch_path, scratch_gdb):
    '''
    Delete and recreate gdb
    '''
    scratch_gdb_path = scratch_path + f"\\{scratch_gdb}"
    if os.path.exists(scratch_gdb_path):
        print("Deleting and re-creating gdb")
        arcpy.management.Delete(scratch_gdb_path)
    arcpy.management.CreateFileGDB(scratch_path, scratch_gdb)

class gaugeChart():
    '''
    class to handle creating gauge charts in a unified format
    supports creating the graph and saving to svg
    '''
    def __init__(self):
        from plotly import io
        import plotly.graph_objects as go
        self.io = io
        self.go = go
    def plot(self, gmu, year, pop, min, max):
        '''
        create the plot, accepts GMU, pop, min/max
        automatically sets the range
        '''
        self.gmu = gmu
        self.year = year
        if max > pop:
            self.range = max + 50
        else:
            self.range = pop + 50
        self.title = f"{gmu}, {year}"

        # Create the figure
        self.fig = self.go.Figure(self.go.Indicator(
            mode = "gauge+number",
            value = pop,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': self.title, 'font': {'size': 24}},
            gauge = {
                'axis': {'dtick': 50, 'range': [None, self.range], 'tickwidth': 0, 'tickcolor': "#2b2b2b"},
                'bar': {'thickness': 0.5,'color': "#f5f5f5"},
                'bgcolor': "#474747",
                'borderwidth': 1.5,
                'shape': 'angular',
                'bordercolor': "#f5f5f5",
                'steps': [
                    {'range': [min, max], 'color': '#00a600', 'thickness': 1,}],
                'threshold': {
                    'line': {'color': "white", 'width': 1},
                    'thickness': 0.5,
                    'value': pop},
                    }))
        self.fig.update_layout(paper_bgcolor = "#474747", font = {'color': "#f5f5f5", 'family': "Arial"}, margin = {"autoexpand": True, "b": 2, "l": 32, "r": 32, "t": 32})
    def view(self):
        '''
        To view the created chart.
        Do not use this in Jenkins or a headless environment
        '''
        self.fig.show()
    def saveSVG(self, path, name):
        '''
        Creates the SVG
        '''
        self.replace_dict = {
            " ": "_",
            "(": "",
            ")": "",
        }
        self.svg_name = name
        self.path = f"{path}\\{self.svg_name}"
        for key, val in self.replace_dict.items():
            self.path = self.path.replace(key, val)
        print(self.path)
        self.io.write_image(fig = self.fig, file = self.path, width = 400, height = 250)

class objectStore():
    def __init__(self, endpoint, access_id, secret):
        import json
        self.json = json
        from minio import Minio
        self.client = Minio(
            endpoint, # The endpoint
            access_id, # access key
            secret, # secret key
        )
    def upload(self, bucket, object, file):
        '''
        Uploads the specified as an object to the bucket.
        Must init the bucket ahead of time.
        '''
        self.client.fput_object(
            bucket, 
            object, 
            file, 
            content_type = "image/svg+xml" # In a generic version, this shouldnt be hardcoded
        )
    def make_public(self, bucket, object):
        '''
        sets the policy on the object to allow public access
        '''
        self.policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"},
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket}/{object}",
                },
            ],
        }
        self.client.set_bucket_policy(bucket, self.json.dumps(self.policy))
        print(f"set {bucket}/{object} as public")
        
# %%
# Credentials

url = 'portal URL' # change to your url, whether maphub, geohub, or other
gis = GIS(url, creds.agol_username, creds.agol_password)

# Handle your credentials in a way that you see appropriate
with open(r"s3_credentials.json") as s3_file:
    s3_credentials = json.load(s3_file)
endpoint, access_id, secret = s3_credentials["endpoint"], s3_credentials["accessId"], s3_credentials["secret"]

print("Credentials complete")
# %% Setup

# Delete/recreate working folder and gdb
for directory, dir_properties in directories.items():
    recreategdb(dir_properties["folder"], dir_properties['gdb'])

arcpy.env.overwriteOutput = True
workingGDB = directories["working"]["folder"] + f"\\{directories['working']['gdb']}"
arcpy.env.workspace = workingGDB
arcpy.env.parallelProcessingFactor = "100%"

# %% Main

# Load AGO FS
fl = FeatureLayer(input_datasets["dataset1"]["dataset"])
fs = fl.query()
fs.save(workingGDB, "dataset1")

# Load csv
pop_obj_tbl = arcpy.conversion.ExportTable(input_datasets["dataset2"]["dataset"], "dataset2_tbl")

# Join population and targets
FC_tempjoin = arcpy.management.AddJoin("dataset1", 
                                    input_datasets["dataset1"]["fields"]["GMUname"], 
                                    pop_obj_tbl, 
                                    input_datasets["dataset2"]["fields"]["GMUname"], )
joinedFC = arcpy.conversion.ExportTable(FC_tempjoin, "joinedFC", "dataset1.PopEst_aerial_complete IS NOT NULL")

print("Pre-analysis complete")
# SearchCursor to make graphs
    # minio to upload to object storage

fields = []
for dataset in input_datasets.values():
    for field in dataset["fields"].values():
        if field not in fields:
            fields.append(field)
        else:
            print(f"duplicate field {field} not added")
print(fields)
chart = gaugeChart()
object_storage = objectStore(endpoint, access_id, secret)
with arcpy.da.SearchCursor(joinedFC, fields) as cursor:
    # build up attributes for graph
    for row in cursor:
        print(row) # Successfully grabs the row from each feature
        min_pre = row[fields.index(input_datasets["dataset2"]["fields"]["objectiveLow"])]
        max_pre = row[fields.index(input_datasets["dataset2"]["fields"]["objectiveHigh"])]
        if min_pre is not None and max_pre is not None: # attribute validation. Should happen for each int transformation
            # chart = gaugeChart()
            gmu_attribute = row[fields.index(input_datasets["dataset1"]["fields"]["GMUname"])]
            year_attribute = int(row[fields.index(input_datasets["dataset1"]["fields"]["yearField"])])
            pop_attribute = int(row[fields.index(input_datasets["dataset1"]["fields"]["popField"])])
            min_attribute = int(min_pre)
            max_attribute = int(max_pre)
            chart.plot(gmu_attribute, year_attribute, pop_attribute, min_attribute, max_attribute)
            svg_name = f"{gmu_attribute}_{year_attribute}.svg"
            object_name = f"{object_properties['folder']}{svg_name}"
            chart.saveSVG(f"{directories['output']['folder']}\\charts", svg_name)
            object_storage.upload(object_properties["bucket"], object_name, chart.path)
# object_storage.make_public(object_properties["bucket"], f"{object_properties['folder']}*") # uncomment to make charts public

print("Charts created")
# Preparing the table for AGO
output_table_path = f"{directories['output']['folder']}\\{directories['output']['gdb']}/dataset2"
output_table = arcpy.conversion.ExportTable(joinedFC, output_table_path)

arcpy.management.CalculateField(output_table, 
                                "url", 
                                f'"{object_properties["url"]}" + "{object_properties["bucket"]}" + "/" + "{object_properties["folder"]}" + !{input_datasets["dataset1"]["fields"]["GMUname"]}! + "_" + str(!{input_datasets["dataset1"]["fields"]["yearField"]}!)[0:4] + ".svg"', 
                                "PYTHON3")
fields.append("url")


# Calculate the description
fields.append("description")
description_block = '''
def description(pop, min, max):
    desc = None
    if None not in [pop, min, max]:
        if pop > max:
            desc = "The population estimate is above the objective of " + str(min) + "-" + str(max) + " mountain goats"
        elif pop > min:
            desc = "The population estimate is within the objective of " + str(min) + "-" + str(max) + " mountain goats"
        elif pop < min:
            desc = "The population estimate is below the objective of "  + str(min) + "-" + str(max) + " mountain goats"
    return desc
    pass


'''
arcpy.management.CalculateField(output_table, 
                                "description", 
                                f'description(!{input_datasets["dataset1"]["fields"]["popField"]}!, !{input_datasets["dataset2"]["fields"]["objectiveLow"]}!, !{input_datasets["dataset2"]["fields"]["objectiveHigh"]}!)', 
                                "PYTHON3", 
                                description_block)

# field cleanup
arcpy.management.DeleteField(output_table, fields, "KEEP_FIELDS")

# Upload table to AGO
overwrite_from_pro({output_table_path:agol_dataset2["service_id"]}, creds.agol_username, creds.agol_password)

print("finished")
# %%
