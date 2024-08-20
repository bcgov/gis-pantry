# Name

Add_Geomark_URLs

# Author

Jeff Kruys, jeff.kruys@gov.bc.ca, Spatial Data Analyst, Forest Investment and Reporting Branch, Ministry of Forests

# Description

The Geomark Web Service takes a feature geometry as input and assigns it a unique URL. This URL can then be sent to another party as a representation of the geometry.

This script tool will add a field named Geomark_URL to a spatial dataset that you select (FGDB feature class, shapefile etc.) and populate the field with a Geomark URL for each feature. There is one tool designed to work in ArcGIS Desktop 10.x (ArcCatalog or ArcMap), and another tool designed to work within ArcGIS Pro 3.x.

# Usage

To use the tool in ArcGIS Desktop, download the two files in the ArcGISDesktop folder above, and save them together in a folder on your local drive or a network drive that you have write access to. In ArcMap, open the Catalog pane (in the Windows menu and select Catalog), browse to the folder where you saved the files, and expand the toolbox item named Add_Geomark_URLs_ArcGISDesktop.tbx. You should see a script tool named Add Geomark URL. Double-click this tool to run it. You will be prompted to select a map layer; select one and click OK to run.

To use the tool in ArcGIS Pro, download the file Add_Geomark_URLs_ArcGISPro.atbx in the ArcGISPro folder above, and save it in a folder on your local drive or a network drive that you have write access to. (This file has the Python code embedded in it, so you do not need to download the other file, add_geomark_py3.py - it is only provided for reference.) In an ArcGIS Pro project, in the Catalog pane under the Project tab, connect to the folder where you saved the file, then browse to that folder and expand the file. You should see a script tool named Add_Geomark_URLs. Double-click that tool to start it. You will be prompted to select a map layer; select one and click OK to run. 

# Dependencies/Requirements/Environments

These scripts have been tested in the GTS desktops named "Kamloops Desktop - Geospatial" (with ArcGIS Pro 3.2.2) and "Kamloops Desktop - ArcGIS 10-8" (with ArcGIS Desktop 10.8).

Executing the tool in the ArcGIS Pro environment requires the Python "requests" module, which should have been installed by default with any installation of ArcGIS Pro and Python 3.x.

Executing the tool in the ArcGIS Desktop environment requires the Python "urllib" and "urllib2" modules, which should have been installed by default with any installation of ArcGIS Desktop 10.8 and Python 2.x.

If you receive an error such as "ImportError: No module named urllib" when running either of these tools, please contact the author.

# Known Bugs/Limitations

This tool is intended to make it easier to generate Geomark URLs more quickly than uploading individual spatial data files for individual features to the Geomark Web Service. 

The ArcGIS Desktop version of the tool runs quickly, creating 10 Geomark URLs in a few seconds. The ArcGIS Pro version of the tool takes a little longer to run - 10 URLs in about 30 seconds.

Both tools are only intended to be used on datasets with small numbers of records - in the hundreds at most. 

# Credits

Thanks to the developers of the Geomark Web Service.

# Update Log

2024-08-20 (Jeff Kruys): Tools uploaded to GitHub.

2024-08-13 (Jeff Kruys): Tool completed and tested in ArcGIS Desktop 10.8.

2024-08-12 (Jeff Kruys): Tool completed and tested in ArcGIS Pro 3.2.2.
