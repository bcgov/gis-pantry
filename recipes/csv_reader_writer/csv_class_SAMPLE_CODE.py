'''
csv_class.py
description: Sample code for using csv_class.py 

Copyright 2023 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at 

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

# ************************************************************************
# CSV
# ************************************************************************
# Create the CSV object.
my_csv = geobc.CSV()

import_csv_path = r"< network path to csv file to import >"
export_csv_path = r"< network path to csv file to export >"

# Creates dictionary list out of the csv
# Dict List Format:
ordered_dict_list = my_csv.create_dict_list(import_csv_path)
print(ordered_dict_list)

# Exports dictionary list to csv
my_csv.export_csv(ordered_dict_list, export_csv_path)

# Loop/Query the dictionary List
for row in ordered_dict_list:
    # Get the value of the cell in "Column Name" for current row
    my_cell = row.get("Column Name")

    # Update the cell value for "Column Name" on current row
    row.update({"Column Name" : "New Value"})

# Delete the CSV object.
del my_csv
