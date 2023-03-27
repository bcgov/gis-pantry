'''
Author:     Wes Smith (with borrowed code from Jing Zhang)
Date:       Feb 2023

Overview:  This script was written as the 1st of a 2 script workflow for updating AGO item properties 
based on a user specified AGO group.  This script reads the item properties and writes them to an xlsx 
file.  AGO_ItemPropertiesUpdate_fromXLSX.py can then be used to bring changes back into AGO.
User inputs are captured via a tkinter gui. 
'''

from arcgis.gis import GIS
import datetime, time
import os, sys
import pandas as pd
import tkinter as tk

def main():
    
    # record start time
    start_time = time.time()
    
    print("\n\n***Running AGO Item Properties to XLSX Script***\n")

    ### PRELIMINARIES ###

    # Datestamps for filename
    datestamp = datetime.datetime.now().strftime("%Y%m%d").replace("/","")
    year = datetime.datetime.now().strftime("%Y")

    # Run the GUI to collect User Input
    # 'year' variable supplied as default value to tool's year parameter
    input_dict = run_the_gui()

    # Parameter Check
    print("Input Parameters:")
    for k, v in input_dict.items():
        if k != "ago_password":
            print(f"   {k}:  {v}")
        else:
            print(f"   {k}:  {'*' * len(v)}")

    output_xlsx= os.path.join(input_dict["output_dir"], 
                f"{input_dict['project_name']}_AGO_ItemsList_{datestamp}.xlsx")

    # Sign in 
    global gis
    gis = GIS(  username=input_dict["ago_username"], 
                password=input_dict["ago_password"])

    ### PROCESS ###

    # Create list of items
    # by group
    item_list = get_items_by_group(group_name=input_dict["group_name"])

    # Refine list with keyword
    item_list = refine_items_by_keyword(item_list, search_keyword=None)
    
    # Create list of properties
    properties_dict = get_properties(item_list)

    # Export list of properties
    export_to_xlsx(properties_dict, output_xlsx)

    print("\nScript is complete...")
    os.startfile(output_xlsx, 'open')

    # record end time
    print(f"Runtime:  {time.strftime('%Hh %Mm %Ss', time.gmtime(time.time()-start_time))}\n\n")

#_________________________________________________________________    

def get_items_by_group(group_name=None):

    print("\nGetting items from group_name")

    try:
        group = gis.groups.search(f"title:{group_name}")[0]
        search_result = group.content() if group else None
        if search_result:
            print(f"{len(search_result)} items found in the group ('{group_name}').")
        else:
            print(f"No items found in the group ('{group_name}')."\
                "*** EXITING ***")
            sys.exit()
    except:
        print(f"No groups found with the name '{group_name}'."\
            "*** EXITING ***")
        sys.exit()

    return search_result

def refine_items_by_keyword(item_obj_list, search_keyword=None):

    print("\nUsing Keyword to Filter Items in List")
    if not search_keyword:
        print("   No keyword Provided")
        return item_obj_list

    if not isinstance(item_obj_list, list):
        print("   The script was expecting a 'list' type variable for the 'item_obj_list' parameter.\n"\
            "A different type was provided.  *** EXITING ***")
        sys.exit()

    refined_list = []
    keywords = set(search_keyword.split())
    
    for item in item_obj_list:
        if any(keyword in (item.tags, item.title) for keyword in keywords):
            refined_list.append(item)
    
    print(f"{len(refined_list)} items found with keyword '{search_keyword}'")

    return refined_list

def get_properties(item_obj_list):

    print("\nGetting item properties")

    # Prepare List of Item Details to Include in Report
    # Each list will be separate column
    title = []
    itemid = []
    url = []
    owner = []
    itemtype = []
    description = []
    summary = []
    tags = []
    termofuse = []
    credit = []
    size = []
    modified_date = []

    # Populate Lists
    for item in item_obj_list:
        # Title
        title.append(item.title)
        # ItemID
        itemid.append(item.itemid)
        # URL
        if not item.url or item.url == "nan" :
            url.append("https://governmentofbc.maps.arcgis.com/home/item.html?id="+item.itemid)
        else:
            url.append(item.url)
        # Type
        itemtype.append(item.type)
        # Owner
        owner.append(item.owner)
        # Description
        if item.description:
            description.append(item.description)
        else:
            description.append(None)
        # Summary
        summary.append(item.snippet)
        # Tags
        tag_str = ', '.join([str(char) for char in item.tags])
        tags.append(tag_str)
        # Terms of use
        termofuse.append(item.licenseInfo)
        # Credits
        credit.append(item.accessInformation)
        # Size on AGO
        size.append(item.size)
        # Date Modified
        modified_date.append(datetime.datetime.fromtimestamp(int(item.modified/1000)).strftime('%Y%m%d'))

    return {"Title": title, 
            'Item ID': itemid,
            "Item Type": itemtype,
            "Owner": owner,
            'URL': url,
            "Summary": summary,
            "Description": description,
            "Tags": tags,
            "Term of Use": termofuse,
            "Credits": credit,
            "Size on AGO": size,
            "Modified Date": modified_date
    }

def create_dataframe(dict):
    df = pd.DataFrame(dict)
    return df

def export_to_xlsx(dict, output_file):

    print("\nExporting properties to Excel")

    df = create_dataframe(dict)
    # file does not exist
    if not os.path.exists(output_file):
        df.to_excel(output_file)
    # file exists
    else:
        print(f"A file with the same name alreayd exists:\n\t{output_file}\nWould you like to overwrite it?")
        overwrite = input("type y/n > ")
        print(overwrite)
        if overwrite == "y":
            os.remove(output_file)
            df.to_excel(output_file)
            message = "data was overwritten"
        else:
            message = "data was not overwritten"
        print(message)
    print(f"{output_file}")
    
#_________________________________________________________________

def run_the_gui():
    
    def get_user_input():
        
        user_input_1 = entry1.get()
        user_input_2 = entry2.get()
        user_input_3 = entry3.get()
        user_input_4 = entry4.get()
        user_input_5 = entry5.get()
        user_input_6 = entry6.get()

        global input_dict
        input_dict = {
            "project_name": user_input_1.strip(),
            "group_name":   user_input_2.strip(),
            "search_keyword":   user_input_3.strip(),
            "output_dir":   user_input_4.strip(),
            "ago_username": user_input_5.upper().strip(),
            "ago_password": user_input_6.strip(),
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
    root.title("AGO Item Properties to XLSX by Group")
    
    label1 = tk.Label(root, text="Project Name")
    label2 = tk.Label(root, text="AGO Group Name:")
    label3 = tk.Label(root, text="Search Keyword (optional):")
    label4 = tk.Label(root, text="Output Folder (for XLSX):")
    label5 = tk.Label(root, text="AGO Username:")
    label6 = tk.Label(root, text="AGO Password:")

    entry1 = tk.Entry(root)
    entry2 = tk.Entry(root)
    entry3 = tk.Entry(root)
    entry4 = tk.Entry(root)
    #entry4.insert(0, r"\\spatialfiles.bcgov\Work\srm\nan\Workarea\wes\Scratch\API_tests")
    entry5 = tk.Entry(root) 
    entry6 = tk.Entry(root, show="*")
    
    label1.grid(row=0, column=0, sticky="W")
    label2.grid(row=1, column=0, sticky="W")
    label3.grid(row=2, column=0, sticky="W")
    label4.grid(row=3, column=0, sticky="W")
    label5.grid(row=4, column=0, sticky="W")
    label6.grid(row=5, column=0, sticky="W")

    entry1.grid(row=0, column=1)
    entry2.grid(row=1, column=1)
    entry3.grid(row=2, column=1)
    entry4.grid(row=3, column=1)
    entry5.grid(row=4, column=1)
    entry6.grid(row=5, column=1)

    submit_button = tk.Button(root, text="Submit", command=combine_functions(get_user_input, quit_gui))
    submit_button.grid(row=6, column=1, pady=10)

    root.mainloop()
    
    return input_dict

#_________________________________________________________________

if __name__ == '__main__':
    main()
