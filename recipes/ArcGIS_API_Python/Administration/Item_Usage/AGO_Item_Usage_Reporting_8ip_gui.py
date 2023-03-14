'''
Author:     Wes Smith (with borrowed code from Jing Zhang)
Date:       Feb 2023

Overview:  this script generates a Excel workbook of AGO items and their usage details 
based on 8 user inputs captured with a tkinter gui. 
'''


from arcgis.gis import GIS
import datetime
import time
import os
import pandas as pd
import datetime as dt
import tkinter as tk
from tkinter import ttk


def main():
    # record start time
    start_time = time.time()
    
    print("\n\n***Running Usage Report Script***\n")

    # Datestamps for filename
    datestamp = datetime.datetime.now().strftime("%Y%m%d").replace("/","")
    year = datetime.datetime.now().strftime("%Y")

    # Run the GUI to collect User Input
    # 'year' variable supplied as default value to tool's year parameter
    input_dict = run_the_gui(year)

    # Parameter Check
    print("Input Parameters:")
    for k, v in input_dict.items():
        if k != "ago_password":
            print(f"   {k}:  {v}")
        else:
            print(f"   {k}:  {'*' * len(v)}")

    # Cast year var to int
    year = int(input_dict["year"])

    #month_of_interest = "January"
    month_int = get_month_int(input_dict["month"])
    
    # Custom Date
    ## dt tuple format: (Year, Month, Day) 
    ## Integer of Month                *** Starts 1 days before date1 and 1 day after date2 ***
    global date1, date2
    # Catch request for December
    if month_int == 12:
        date1 = dt.datetime(year,month_int,2)
        date2 = dt.datetime(year+1,1,1)
    # All months except December
    else:
        date1 = dt.datetime(year,month_int,2)
        date2 = dt.datetime(year,month_int+1,1)

    # Sign in 
    username = input_dict["ago_username"] #Case Sensitive.  Must all be upper case.
    global gis
    gis = GIS(  username=input_dict["ago_username"], 
                password=input_dict["ago_password"]) 

    # ESRI Date Range
    #https://developers.arcgis.com/python/api-reference/arcgis.gis.toc.html#arcgis.gis.Item.usage
    #datarange = "60D"

    # Create list of items
    # by group
    item_list = get_items_by_group(group_name=input_dict["group_name"])

    # by folder

    # by keyword

    # prepare usage data
    usage_dict = get_usage_multiple_items(item_list, input_dict["search_keyword"])

    print(usage_dict['titles'])
    # Process usage data
    usage_dict = process_usages(usage_dict, 
                            input_dict["month"], 
                            input_dict["year"],)

    # Make usage report
    xlsx_report = make_usage_report(usage_dict, 
                            datestamp, 
                            input_dict,)

    print("\nDone")

    os.startfile(xlsx_report)

    # record end time
    print(f"Runtime:  {time.strftime('%Hh %Mm %Ss', time.gmtime(time.time()-start_time))}\n\n")


#_________________________________________________________________
# Functions
#_________________________________________________________________

# Not Tested - Not working with GUI
def get_usage_single_item(item_id):
    item =  gis.content.get(item_id)
    usage_df = item.usage(date_range=(date1, date2))

    titles = [item.title]
    item_type = [item.type]
    usages = [usage_df]
    itemids = [item_id]

    return {'titles': titles,
            'item_types': item_type,
            'usages': usages,   
            'itemids': itemids,
    }


def get_items_by_group(group_name=None):

    print("\nGetting items from group_name")

    # Catch no group name provided
    if not group_name:
        print("   No group_name parameter provided to get_items_by_group() function")
        search_result = None
    # Group name provided
    else:
        # Group Object
        group = gis.groups.search(f"title:{group_name}")[0]
        # Group exists
        if group:
            # Group content, returned as list of item objects
            search_result = group.content()
            print(f"   {len(search_result)} items found in the group ({group_name}).")
        # Group does not exist
        else:
            print(f"    No groups found with the name '{group_name}")
    
    return search_result


def get_items_by_folder():
    pass


def get_items_by_keyword():
    pass 


def get_usage_multiple_items(item_obj_list, search_keyword=None):

    print("\nMaking Usage Lists from Items")
    if not search_keyword:
        print("   No keyword Provided")

    if isinstance(item_obj_list, list):

        # Count the # of item objects in the list
        count = 0
        for item in item_obj_list:
            if search_keyword:
                if search_keyword in item.tags or \
                        search_keyword in item.title or \
                        search_keyword + " " in item.tags or \
                        " " + search_keyword + " " in item.title:
                    count += 1
            else:
                count += 1

        print(f"   {count} items found with keyword '{search_keyword}'")

        # Lists to be populated with a value for each item
        titles = []
        item_types = []
        usages = []
        itemids = []

        # Loop over item objects in list
        for item in item_obj_list:
            # Catch if keyword was entered by user
            if search_keyword:
                if search_keyword in item.tags or \
                        search_keyword in item.title or \
                        search_keyword + " " in item.tags or \
                        " " + search_keyword + " " in item.title:
                    print(f"      {item.title}  |  {item.type}")
                    titles.append(item.title)
                    item_types.append(item.type)
                    itemids.append(item.itemid)
                    usages.append(item.usage(date_range=(date1, date2))) # Pandas df object
            # No keyword was entered
            else:
                print(f"      {item.title}  |  {item.type}")
                titles.append(item.title)
                item_types.append(item.type)
                itemids.append(item.itemid)
                usages.append(item.usage(date_range=(date1, date2))) # Pandas df object

    # Check count of each list
    print(f"   count of titles - itemids - usage  |  {len(titles)}    -     {len(itemids)}    -    {len(usages)}")

    return {'titles': titles,
            'item_types': item_types,
            'usages': usages,   
            'itemids': itemids,
    }


def process_usages(usage_dict, month, year):

    print("\nProcessing usage records, by item.")

    # lists of each item, populated by data from each item
    counts = []
    months = []
    years = []
    # Loop over each item's usage dataframe
    for usage_record in usage_dict["usages"]:
        
        record_index = 0
        count = 0
        
        # Catch no usage records
        if usage_record is None:
            count = -1
        # Usage record exists
        else:
            # generate the sum of the usage counts for each day
            for record in usage_record["Date"]:
                #print(record)
                count = count + usage_record["Usage"][record_index]
                record_index += 1    
        
        # Add to lists
        months.append(month)
        years.append(year)
        counts.append(count)

    # Add to dictionary
    usage_dict['months'] = months
    usage_dict['years'] = years
    usage_dict['counts'] = counts
    
    return usage_dict


def make_usage_report(usage_dict, datestamp, input_dict):
    
    print("\nMaking usage report")

    # Create empty data frame
    df=pd.DataFrame()

    # Fill the data frame
    df["Title"] =       usage_dict["titles"]
    df["Item Type"] =   usage_dict["item_types"]
    df['Item ID'] =     usage_dict["itemids"]
    df['Month'] =       usage_dict["months"]
    df['Year'] =        usage_dict["years"]
    df['Usage'] =       usage_dict["counts"]

    #print(df.head())
    print(df)

    #df=df.set_index("Usage")
    #df=df.drop(-1,axis=0)

    # Prepare to Export
    project = input_dict["project_name"]
    output_dir = input_dict["output_dir"]
    month = input_dict["month"]
    year = input_dict['year']
    output_name = f"{project}_Usage_Report_{year}{month}_{datestamp}"
    output = os.path.join(output_dir, output_name + ".xlsx")

    # Export
    df.to_excel(output) 

    print(f"\nOutput file:\n{output}")

    return output


def report_counts(df):
    # Count using built-in Panada methods
    count = df.Usage.sum(axis=0)
    print(f"Usage by df sum(): {count}")

    # Count through iterating over attribute values in rows
    df.reset_index()
    count = 0
    for index, row in df.iterrows():
        if row["Date"].month:# == Month:
            count += row["Usage"]   
    print(f"Usage by iteration: {count}")

    return count

def get_month_int(month_of_interest):

    month_dict = {
        1: {"name": "January",
            "days": 31},
        2: {"name": "February",
            "days": 28},
        3: {"name": "March",
            "days": 31},
        4: {"name": "April",
            "days": 30},
        5: {"name": "May",
            "days": 31},
        6: {"name": "June",
            "days": 30},
        7: {"name": "July",
            "days": 31},
        8: {"name": "August",
            "days": 31},
        9: {"name": "September",
            "days": 30},
        10: {"name": "October",
            "days": 31},
        11: {"name": "November",
            "days": 30},
        12: {"name": "December",
            "days": 31},
    }

    found = False
    for month_int, props in month_dict.items():
        if props["name"] == month_of_interest:
            found = True
            return month_int
    if not found:
        print("Error getting integer of month")
        return None

#_________________________________________________________________
# GUI
#_________________________________________________________________

def run_the_gui(current_year):
    
    def get_user_input():
        
        user_input_1 = entry1.get()
        user_input_2 = entry2.get()
        user_input_3 = entry3.get()
        user_input_4 = entry4.get()
        user_input_5 = entry5.get()
        user_input_6 = entry6.get()
        user_input_7 = entry7.get()
        user_input_8 = entry8.get()

        global input_dict
        input_dict = {
            "project_name": user_input_1,
            "group_name":   user_input_2,
            "search_keyword":   user_input_3,
            "output_dir":   user_input_4,
            "month":        user_input_5,
            "year":         user_input_6,
            "ago_username": user_input_7.upper(),
            "ago_password": user_input_8,
        }

    def quit_gui():
        root.quit()

    def combine_functions(*funcs):
    
        def combined_functions(*args, **kwargs):
            # Call the passed functions, with their arguments (if they have any)
            for func in funcs:
                func(*args, **kwargs)
    
        return combined_functions

    root = tk.Tk()
    root.title("AGO Item Usage by Group")

    # Month drop down
    month_options = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    
    label1 = tk.Label(root, text="Project Name")
    label2 = tk.Label(root, text="Group Name:")
    label3 = tk.Label(root, text="Search String (Keyword):")
    label4 = tk.Label(root, text="Output Folder:")
    label5 = tk.Label(root, text="Report Month:")
    label6 = tk.Label(root, text="Year:")
    label7 = tk.Label(root, text="AGO Username:")
    label8 = tk.Label(root, text="AGO_Password:")

    entry1 = tk.Entry(root)
    #entry1.insert(0, "SBOT")
    entry2 = tk.Entry(root)
    #entry2.insert(0, "Stewardship Baseline Objectives Tool (SBOT) - Broadcast Group")
    entry3 = tk.Entry(root)
    #entry3.insert(0, "Main")
    entry4 = tk.Entry(root)
    #entry4.insert(0, r"\\spatialfiles.bcgov\Work\srm\nan\Workarea\wes\Scratch\API_tests")
    entry5 = tk.StringVar()
    option_menu = ttk.OptionMenu(
            root,
            entry5,
            None, month_options[0],
            *month_options,    ) 
    entry6 = tk.Entry(root)
    entry6.insert(0, str(current_year))
    entry7 = tk.Entry(root)
    #entry7.insert(0, "WESSMITH.BC")
    entry8 = tk.Entry(root, show="*")

    label1.grid(row=0, column=0, sticky="W")
    label2.grid(row=1, column=0, sticky="W")
    label3.grid(row=2, column=0, sticky="W")
    label4.grid(row=3, column=0, sticky="W")
    label5.grid(row=4, column=0, sticky="W")
    label6.grid(row=5, column=0, sticky="W")
    label7.grid(row=6, column=0, sticky="W")
    label8.grid(row=7, column=0, sticky="W")

    entry1.grid(row=0, column=1)
    entry2.grid(row=1, column=1)
    entry3.grid(row=2, column=1)
    entry4.grid(row=3, column=1)
    option_menu.grid(row=4, column=1)
    entry6.grid(row=5, column=1)
    entry7.grid(row=6, column=1)
    entry8.grid(row=7, column=1)

    submit_button = tk.Button(root, text="Submit", command=combine_functions(get_user_input, quit_gui))
    submit_button.grid(row=8, column=1, pady=10)
    #entry5.focus()

    root.mainloop()
    
    return input_dict

#_________________________________________________________________

if __name__ == '__main__':
    main()