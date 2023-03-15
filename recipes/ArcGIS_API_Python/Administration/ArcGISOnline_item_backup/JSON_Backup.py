'''
AGO Backup Script
backs up AGO items (excluding layers) from multiple accounts.
Note that the items need to be shared with the account used to do the backing up

Supports backing up to multiple folders with variable retention policies.


Isaac Cave
Feb 15th, 2023
v0.1

v0.2
-Added more backup types to whitelist
-optimized type search logic

v0.3
March 3rd, 2023
-Added support for multiple folders
-Added support for variable retention policies
-Better logging
-Updated description

'''


#%%
# Imports
from arcgis.gis import GIS
from datetime import datetime
import json
import os
import shutil

#%%
# Configuration
maphub_accounts = [
    "account 1", 
    "account 2",
    ] # Accounts to backup from. Items must be shared with PX.SCGIS
max_search = 10000 # Maximum number of items
folders = {
    r"longterm_folder":{
        "max_backups":8
    },
    r"shortterm_folder":{
        "max_backups":2
    },
}

backup_types = ["Web Map", "Dashboard", "Notebook", "Web Mapping Application", 
"Web Experience", "StoryMap", "Web Scene", "Web AppBuilder", 
"Hub Page", "Hub Page","Hub Site Application", "Code Attachment",
 "StoryMap Theme", "Solution", "GeoJson", "Operation View",
"Hub Initiative", "Map Area", "Insights Workbook", "Insights Page"]
#%%
# Credentials
agol_username = ""
agol_password = ""

url = 'http://governmentofbc.maps.arcgis.com' # change to your url, whether maphub, geohub, or other
gis = GIS(url, agol_username, agol_password)

#%%
# Function setup
class json_item:
    def __init__(self,primary_id, folder):
        self.primary_id = primary_id
        self.folder = folder
        self.change_list = []
        self.prim_wm_item = gis.content.get(self.primary_id)
        self.prim_wm_json = self.prim_wm_item.get_data()
    def json_backup(self): #backs up the json to the hardcoded path\
        today = datetime.today().strftime("%Y_%m_%d")
        current_folder = f"{folder}\{today}"
        self.filename = f"{self.prim_wm_item.title}_{self.primary_id}.json".replace(":", "-").replace('"', '').replace("|", "_").replace("/", "_").replace("\\", "_")
        self.filename = f"{current_folder}/{self.filename}"
        if not os.path.exists(current_folder):
            os.mkdir(current_folder)
        with open(self.filename, "w") as file_handle:
            file_handle.write(json.dumps(self.prim_wm_json))


#%%
# Backing up
count = 0
for username in maphub_accounts:
    item_list = []
    for i in gis.content.search(query="* AND \  owner:" + username, max_items=max_search):
        item_list.append(i)

    for result in item_list:
        in_id = result.id
        if result.type in backup_types:
            print(f"backing up {in_id}")
            count+=1
            for folder in folders:
                item = json_item(in_id, folder)
                item.json_backup()
print(f"{count} items backed up")
#%%
# Delete older backups
for folder in folders:
    keep = folders[folder]["max_backups"]
    dir_list = os.listdir(folder)
    dir_list_len = len(dir_list)
    if dir_list_len > keep:
        dir_list.sort()
        remove_list = dir_list[0:-(keep)]
        for item in remove_list:
            print(f"Removing {item} from {folder}")
            shutil.rmtree(folder + "\\" + item)


#%%