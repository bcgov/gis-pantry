# Field and row counter and samples tool for ArcGIS 10.6

This is a script tool for finding the number of rows and fields in a layer, and to get some sample vlaues for each row. It's meant to run in ArcGIS Desktop 10.6. The tool is a useful way to quickly explore a dataset you are not familiar with; it is a much quicker way to get a feel for the values contained in each field, rather than browsing a (sometimes very large) attribute table.

# Parameters:

>Choose your dataset from BCGW or folder location (or leave blank):
>Choose your layer from the Table of Contents (or leave blank)
- You can choose a dataset either from BCGW or folder location, or from Table of Contents. 

> Choose your BCGW .sde connection from this list: 
- This parameter gives you a choice of any pre-existing BCGW connections you have set up in your ArcGIS Database Connections

>Show sample values for each field?
- This is a yes / no checkbox .

> How many sample values per field?
- Default value is 3, adding more will slow down the script..

> Use quick mode? (recommended for large datasets)
- A yes/ no checkbox to toggle 'Quick mode', which limits the sample size to 10 rows, and gives up trying to find new values if you get the same value 5x in a row (in random rows).

# Date: July 8, 2019
