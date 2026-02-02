# BC Forest Finder

Created by North Ross as part of my [Automating GIS processes](https://autogis-site.readthedocs.io) course at University of Helsinki, I created this repository for the final assignment.

I thought I would add it to the GIS pantry in case it's useful or interesting for anyone else in the BC Government.

The main thing I learned from this class was how to use network analysis through NetworkX. I decided to use OpenStreetMap data for this project since it was easier, but it probably wouldn't be too hard to adapt this to use the Digital Roads Atlas instead.

## Topic: A tool to find the nearest, most accessible forest stand with given characteristics in British Columbia, Canada
In BC, Canada, the Ministry of Forests maintains a large geospatial dataset that divides the province into millions of forest stand polygons. These contain many attributes that serve as our best guess for the ecological characteristics of this stand, such as dominant tree species, age, productivity, and climate zone. 

As an amateur ecologist, citizen science, mushroom forager, and person who's up for adventures, I sometimes find myself querying the VRI for certain characteristics then looking at them on a map to plan a trip to visit them. For example, if I'm looking for chanterelles I might be looking for a 60-100 year old Douglas Fir-dominated stand that is relatively road-accessible. This can be a bit time-consuming especially for someone without a GIS background, so I thought it might be a cool project to adapt this into something a bit easier to use.

This notebook accepts a few core input parameters to select the area, search radius and desired forest stand characteristics. These must be formatted as a SQL-style WHERE clause and requires some familiarity with the VRI Data (see [BC Vegetation Resource Inventory Rank 1 Data](https://catalogue.data.gov.bc.ca/dataset/vri-2024-forest-vegetation-composite-rank-1-layer-r1-)). The easiest way to do this is to copy it from the "Definition Query" in ArcGIS or QGIS.

Additionally, there are a few other parameters that the user can adjust, such as the max number of candidates to display on the output map, the max cross-country (non-network) linear travel distance from the network to the polygon, and the fields and aliases to show on the popups in the final output.

### Structure of this repository:

#### 📒 `BC-Forest-Finder-Port-Refrew.ipynb` 🍄🌲
This jupyter notebook has a detailed explanation of the process of the BC Forest Finder, explored through an example of finding the closest chanterelle-bearing forests within 5km of the town of Port Renfrew on Vancouver Island, BC. Use this notebook to familiarize yourself with the project.

#### 📒 `BC-Forest-Finder-Prince-George.ipynb` 
This notebook is filled with another example of using the BC Forest Finder, but with a less robust description so it is faster to run. It searches for old forest (older than 140 years) within 10km of the town of Smithers, BC. This version will be easier for a user to edit and run again with a new location.

#### 🐍 `bcforestfinder.py`
This Python script file is the module containing all the functions used as part of the analysis. It is imported into the other scripts.

#### 📁 `outputs`
- This folder contains the output folium maps saved as HTML files. These show the top candidate forests, the starting point, and the paths to get there. 

### Required libraries:
- [GeoPandas](https://geopandas.org/en/stable/) and dependencies (pandas, shapely, numpy)
- [OSMnx](https://osmnx.readthedocs.io/en/stable/) and dependencies (NetworkX)
- [DuckDB for Python](https://duckdb.org/docs/stable/guides/python/install) - this is used to quickly and efficiently parse the GeoParquet file containing the VRI data. Due to some issues with GeoPandas' read_parquet function, I found this library works much better.
- [Folium](https://python-visualization.github.io/folium/latest/index.html) and [branca](https://python-visualization.github.io/branca/) are used to create the output interactive Leaflet map.

### Input data:
- [BC Vegetation Resource Inventory Rank 1 Data](https://catalogue.data.gov.bc.ca/dataset/vri-2024-forest-vegetation-composite-rank-1-layer-r1-)
    - This dataset is updated annualy by thhe BC Ministry of Forests.
    - It divides the province into millions of polygons based on air photo imagery and assigns attributes to estimate forest stand characteristics such as:
        - Tree age
        - Dominant species
        - Average tree height/diameter
        - Timber volume
        - Productivity (site index)
        - [BEC zone](https://www.for.gov.bc.ca/hre/becweb/system/how/index.html)
        - and much more.
- Open Street Map data accessed through [NetworkX](https://networkx.org/documentation/)

### Analysis steps:
1. Inputs are a start location (coordinates or search term to geocode), a search radius and desired stand characteristics.
2. Data is selected from the VRI data Parquet file within the radius using duckdb.
3. All candidate polygons are selected from the VRI subset and adjacent ones are grouped together.
4. Using NetworkX with OpenStreetMap data, calculate estimated travel time from the start location to the polygons. Rank these based on the shortest travel time.

### Results:
1. A text string listing the stands, their travel time and nearest road surface material.
2. Show a Folium map with satellite base layer showing the polygon outlines and the route there.
    - This can also optionally be exported as an HTML including the above text string.

### Troubleshooting:
Usually the DuckDB operation querying the VRI parquet data (bcforestfinder.get_vri()) will take a bit of time to run. Occasionally, the kernel will die unexpectedly at this step. Often it will work again after restarting the kernel or your Jupyter session. Alternatively, you can try adding a `work_dir='temp'` argument to this function to save the data locally instead of in-memory, which will slow things down and take up space but might be more stable, especially with large queries.

### References:

While working as for the Government of BC, I wrote some code for VRI data analysis using DuckDB - I referenced this while writing these functions: [AFLB Analysis](https://github.com/northross-bcgov/WMB_Analysis/blob/main/CreateAFLB.py).

More code from my colleague Will Burt exploring using DuckDB and the VRI data: [DuckDB Exploration](https://github.com/bcgov/gis-pantry/blob/9bfbd190f752da99bc5466e623e34fadc54e538e/recipes/duckdb/duckdb-geospatial.ipynb#L104)

### Use of AI:
[Duck.ai](https://duckduckgo.com/?q=DuckDuckGo+AI+Chat&ia=chat&duckai=1) was occasionally used to troubleshoot errors but no AI-generated code was directly copied into this notebook.
