# AGO_ItemPropertiesUpdate_fromXLSX.py
# AGO_ItemProperties_toXLSX.py

# Background/Overview
These scripts are part of a workflow for updating AGO item properites.  Script 1 (AGO_ItemProperties_toXLSX.py) reads item properties from a user-defined AGO group
and writes them to am XLSX file.  The user can then review the content of the spread-
sheet, updating properties as needed.  Script 2 (AGO_ItemPropertiesUpdate_fromXLSX.py) 
can then be used to 'push' the updated item properties back to AGO.   

# Usage
1.  a)  Run AGO_ItemProperties_toXLSX.py from an IDE
    b)  When the Gui pop up, enter the parameters for the usage report to be generated, and click submit.
            Project Name:       Name of the project being reported on.  This variable 
                                is only used in the name of the XLSX output.
            AGO Group Name:     Name of the AGO group that holds the items to be 
                                reported on.
            Search Keyword (optional):  Enter a single keyword that could be found 
                                in the items' title or tags.
            Output Folder (for XLSX):   The directory where the XLSX report will be
                                exported to.
            AGO Username:       Username of the AGO account used to log in.
            AGO_Password:       Password of the AGO account used to log in.
    c)  The script will open the XLSX file, upon completion.  

2.  a)  Review the results.
    b)  Modify properties in the XLSX, as needed

3.  a)  Run AGO_ItemPropertiesUpdate_fromXLSX.py from an IDE.
    b)  When the Gui pop up, enter the parameters for the usage report to be generated, and click submit.
            Input XLSX Path:    This is the name of the spreadsheet created in step 1,
                                and modified in step 2.
            AGO Username:       Username of the AGO account used to log in.
            AGO_Password:       Password of the AGO account used to log in.
    c)  The script will push the updates back to AGO, item by item.

# Limitations
Currently, the tool requires a group name be supplied as a parameter via the GUI.