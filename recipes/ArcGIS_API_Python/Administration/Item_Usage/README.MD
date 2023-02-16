# AGO_Item_Usage_Reporting_8ip_gui.py

# Background/Overview
Using the using ArcGIS API for Python, this script generates a Excel workbook of AGO items and their usage details based on 8 user inputs.  The script springs from the logic of a script written by Jing Zhang.  A tkinter GUI is used to collect user inputs, which are then fed into the main script.  The code for creating the GUI is a part of the script for ease of deployment, creating a stand-alone script.

# Usage
1. Run the script from envoronment for running python scripts.
2. When the Gui pop up, enter the parameters for the usage report to be generated
    Project Name:               Name of the project being reported on.  This variable is only used in the name of the XLSX output.
    Group Name:                 Name of the AGO group that holds the items to be reported on.
    Search String (Keyword):    Enter a single keyword that could be found in the items' title or tags. 
    Output Folder:              The directory where the XLSX report will be exported to.
    Report Month:               The month to be reported on (use the dropdown).
    Year:                       The year of the month to be reported on.
    AGO Username:               Username of the AGO account used to log in.
    AGO_Password:               Password of the AGO account used to log in. 
3. The script will open the XLSX file.  Review the results.

# Limitations
Currently, the tool requires a group name be supplied as a parameter via the GUI.

Different AGO items report usage differently.  Check out ESRI's notes about what is reported by the ```item.usage()``` method in the API Reference for the [arcgis.gis.module](https://developers.arcgis.com/python/api-reference/arcgis.gis.toc.html#arcgis.gis.Item.usage).