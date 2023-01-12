'''
Author: Isaac Cave
Date: 4th January, 2023
Usage example for committing changes to derivative webmaps

Updates:
v0.1
'''

# %%
############ Imports
from arcgis.gis import GIS
from generic_map_dash_changes import *
import sys

# %% 
############ log in and set up your AGO connection
# Depending on your needs, you may handle credentials differently
sys.path.insert(1, r'\\spatialfiles.bcgov\work\srm\sry\Local\scripts\python\credentials')
from credential_access import *

url = 'https://governmentofbc.maps.arcgis.com' # change to your url, whether maphub, geohub, or other
# global gis
gis = GIS(url, agol_username, agol_password)

# %% 
############ Setting lists of changes
map_list = [
    derived_map(
        gis,
        "8aab32af2c4d48b091dadb55592f723b",
        "33b382a5fda74641a658128f7c3513b4",
        ["182cc61d735-layer-4"], 
        ["18517e8ca9d-layer-10"],
        ), # initial example
    derived_map(
        gis,
        "8aab32af2c4d48b091dadb55592f723b",
        "abca483101e744fe931c7a65a3899de4",
        ["182cc61d735-layer-4"],
        [
            "18517e8ca9d-layer-10", 
            "18517ec8414-layer-11"
            ]
        )
]

# %% 
############ Running the code

for in_map in map_list:
    in_map.changes()
    in_map.push()

# %%
############ Full delete. Restore working example

full_del = ["18517e774c0-layer-8","182dbed7b25-layer-7","182cc69217f-layer-6","182c6c99d58-layer-2","182c6cd2bba-layer-3","182cc61d735-layer-4"]

map_list = [
    derived_map(gis, "8aab32af2c4d48b091dadb55592f723b","33b382a5fda74641a658128f7c3513b4",[],full_del),
    derived_map(gis, "8aab32af2c4d48b091dadb55592f723b","abca483101e744fe931c7a65a3899de4",[],full_del)
]

for in_map in map_list:
    in_map.changes()
    in_map.push()
    print("map written")

# %%
