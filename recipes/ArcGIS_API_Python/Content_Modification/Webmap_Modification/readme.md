# Scripting map creation in ArcGIS Online

## Overview
This script allows you to perform some simple changes to an ArcGIS Online (AGO) WebMap and save it to a new map.\

The intended use is to allow users to automate the creation of webmaps where a tool may have multiples in use in dashboards with minor changes.\
For example, a project may require three dashboards, with webmaps that differ only in which layers are visible by default.\
An additional example is a project that has internal/external versions, requiring certain layers to be removed from the external version.


Use the `derived_map` class to define source and destination maps and the layer-ids to change visibility or flag for deletion.

A simple class for working with dashboard selectors, `derived_dashboard` is also included. The functionality generally mirrors the `derived_map` class, accepting source/destination dashboards and a list of selectors to delete.

## Usage
you can use the script by adding it to your script directory (or sys.path) and importing it with:
```python
from generic_map_dash_changes import *
```
or
```python
from generic_map_dash_changes import derived_map
```

You can then define some changes. Note that the classes use layer-ids and map-ids only.
layer-id can be found in the json for the webmap, either using [ArcGIS Online Assistant](https://assistant.esri-ps.com/content) or by calling the json with ArcGIS API.\
The map-id comes from the URL of the webmap.\
Example: [https://governmentofbc.maps.arcgis.com/home/item.html?id=8aab32af2c4d48b091dadb55592f723b](https://governmentofbc.maps.arcgis.com/home/item.html?id=8aab32af2c4d48b091dadb55592f723b)

```python
map_1 = derived_map(
    gis,
    "8aab32af2c4d48b091dadb55592f723b", # The original map id
    "33b382a5fda74641a658128f7c3513b4", # The derived map id
    ["182cc61d735-layer-4"], # List of layers to turn on visibility
    ["18517e8ca9d-layer-10"] # List of layers to delete
    )
```

Once you have defined your changes, you use the `changes()` function to created a modified version of the original json, then use `push()` to updated the derived map:

```python
map_1.changes()
map_1.push()
```
