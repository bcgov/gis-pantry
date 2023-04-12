'''
ArcGIS Online Dependency Checker

A script to check to list out how items in AGO are used, to determine patterns, and which items are no longer needed.

March 10th, 2023

Isaac Cave, South Coast Region

V0.3
Added retention policy to only keep n spreadsheets

V0.2
Cleaned up code, fixed bugs;
-accounts for Error 403 in groups (try/except)
-handles unshared items better
-searches for groups
-added readme

V0.1
Initial

# TODO: notebook support is a special case. downloaded file needs to be loaded as text to work
'''
# %%
# Imports
from arcgis.gis import GIS
from datetime import datetime
from json import dump
import os
import pandas as pd
import time

#%%
# Credentials
# Insert your own method here
sys.path.insert(1, r'Local\scripts\python\credentials')
import credential_access

url = 'https://governmentofbc.maps.arcgis.com' # change to your url, whether maphub, geohub, or other
gis = GIS(url, credential_access.agol_username, credential_access.agol_password)

#%%
# Configuration
maphub_accounts = ["account1", "account2"]
# max_search = 10000 # Maximum number of items # limit for testing
max_search = 10000

host_types = [
    "Feature Service", "Feature Layer", "Web Map", "Dashboard", 
    "StoryMap", "Web Mapping Application", "Web AppBuilder", 
    "Map Service", 
    ]
dependent_types = [
    "Web Map", "Dashboard", "Notebook", "Web Mapping Application", 
    "Web Experience", "StoryMap", "Web Scene", "Web AppBuilder", 
    "Hub Page","Hub Site Application", "Hub Initiative", 
    ] # To prevent naively querying irrelevant json

# URL template
url_base = url
url_template = url_base + "/home/item.html?id="

csv_location = r"Results"
retention = 4 # How many past results to keep

# %%
# Main part
start = time.time()
df = pd.DataFrame()
df_i = 0
count = 0
dependent_count = 0
id_checked = []
item_list = []
dependents = []
dependents = gis.content.search(query="*", max_items=max_search) # Searches across all users in AGO
for username in maphub_accounts: # Searches for items owned by the accounts listed above
    item_list += gis.content.search(query="* AND \  owner:" + username, max_items=max_search)

## Iterates thru the dependent locations found, attempts to dump the json, and does a string search for item IDs and URL (if available)
for dependent in dependents:
    count = 0
    if dependent.type in dependent_types:
        try:
            dependent_dat = gis.content.get(dependent.id)
            dependent_json = dependent_dat.get_data(try_json=False)
        except AttributeError:
            dependent_json = None
            print("Skipping. Could not get dependent json")
        if dependent_json is not None:
            dependent_count += 1
            # iterate thru items to search for, add their entry to the df, populate
            for result in item_list:
                if result.type in host_types:
                    count +=1
                    if result.id not in id_checked:
                        # Build df entry
                        df.loc[df_i, "Item Title"] = result.title
                        df.loc[df_i, "Item ID"] = result.id
                        df.loc[df_i, "Item URL"] = url_template + result.id # concatenates url from base provided above
                        df.loc[df_i, "Item Owner"] = result.owner
                        df.loc[df_i, "Item Type"] = result.type
                        # Grabbing groups is VERY Slow.
                        ## comment out this section if this isn't required 
                        df.loc[df_i, "Groups"] = ""
                        print(result.title, result.id)
                        groups = result.shared_with['groups']
                        try: # Some groups will throw error 403. This is inconsistent and changes each run.
                            if len(groups) > 0:
                                for group in groups:
                                    try: # Some groups have permission errors
                                        group_title = group.title
                                    except:
                                        group_title = "UNKNOWN"
                                        print("Unable to access a group")
                                        df.loc[df_i, "Groups"] = (df.loc[df_i, "Groups"] + ", " + group_title).strip(", ")
                                    df.loc[df_i, "Groups"] = (df.loc[df_i, "Groups"] + ", " + group_title).strip(", ")
                            else:
                                print("Unshared")
                                df.loc[df_i, "Groups"] = "Unshared"
                        except:
                            print("Error checking sharing")
                            df.loc[df_i, "Groups"] = "ERROR"
                        ## End of the groups section
                        df.loc[df_i, "Dependent App Names"] = ""
                        df.loc[df_i, "Dependent App IDs"] = ""
                        df.loc[df_i, "Dependent App Owners"] = ""
                        df.loc[df_i, "Dependent App Count"] = 0
                        df_i += 1
                        id_checked.append(result.id)
                    if result.id is not None and len(result.id) > 0:
                        in_id = result.id
                    else:
                        in_id = None
                    if result.url is not None and len(result.url) > 0:
                        in_url = result.url
                    else:
                        in_url = None
                    row_value = df.loc[df["Item ID"] == in_id].index[0]
                    if in_id is not None and in_id in dependent_json:
                        print(f"FOUND the ID {in_id} in {dependent.title}")
                        df.loc[row_value, "Dependent App Names"] = (df.loc[row_value, "Dependent App Names"] + ", " + dependent.title).strip(", ")
                        df.loc[row_value, "Dependent App IDs"] = (df.loc[row_value, "Dependent App IDs"] + ", " + dependent.id).strip(", ")
                        if dependent.owner not in df.loc[row_value, "Dependent App Owners"]:
                            df.loc[row_value, "Dependent App Owners"] = (df.loc[row_value, "Dependent App Owners"] + ", " + dependent.owner).strip(", ")
                        df.loc[row_value, "Dependent App Count"] = df.loc[row_value, "Dependent App Count"] + 1
                    elif in_url is not None and in_url in dependent_json: # Only needed for double checking
                        print(f"FOUND the URL {in_url} in {dependent.title}")
                        df.loc[row_value, "Dependent App Names"] = (df.loc[row_value, "Dependent App Names"] + ", " + dependent.title).strip(", ")
                        df.loc[row_value, "Dependent App IDs"] = (df.loc[row_value, "Dependent App IDs"] + ", " + dependent.id).strip(", ")
                        if dependent.owner not in df.loc[row_value, "Dependent App Owners"]:
                            df.loc[row_value, "Dependent App Owners"] = (df.loc[row_value, "Dependent App Owners"] + ", " + dependent.owner).strip(", ")
                        df.loc[row_value, "Dependent App Count"] = df.loc[row_value, "Dependent App Count"] + 1

            print(f"checked thru {dependent.title} for {count} items")
print(f"Checked thru {dependent_count} Usage locations")

today = datetime.today().strftime("%Y_%m_%d")
df.to_csv(csv_location + f"\\Dependencies_{today}.csv", index = False)

end = time.time()
end_min = int((end-start)//60)
end_hr = int(end_min//60)
print(f"runtime: {end_min} mins")

# %%
# Delete old results
dir_list = os.listdir(csv_location)
dir_list_len = len(dir_list)
if dir_list_len > retention:
    dir_list.sort()
    remove_list = dir_list[0:-(retention)]
    for item in remove_list:
        print(f"Removing {item} from {csv_location}")
        os.remove(csv_location + "\\" + item)

# %%