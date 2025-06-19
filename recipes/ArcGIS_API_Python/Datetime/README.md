# Working with Datetime in ArcGIS Online (AGOL)  
This tutorial is intended for python and AGOL users, for extracting and populating a date field from an ArcGIS Online feature layer. 
Author: Emma Armitage (emma.armitage@gov.bc.ca)

## Table of Contents
[AGOL Date Field Basics](#agol-date-field-basics)  
[Extract Datetimes from AGOL](#workflow-1-extract-datetimes-from-agol)   
[Upload Datetimes to AGOL](#workflow-2-upload-datetimes-to-agol)    
[Full Code Snippets](#full-code-snippets)  

## AGOL Date Field Basics
[Return to top](#working-with-datetime-in-arcgis-online-agol)  
- Dates are stored in [**Universal Time Coordinated (UTC)**](https://www.wpc.ncep.noaa.gov/html/FAQs_1.html#:~:text=UTC%20literally%20stands%20for%20Universal,%20and%20Zulu%20(Z).).
- AGOL displays datetimes localized to the user’s timezone.
- `MM/DD/YYYY hh:mm:ss` is the default format. If no time is provided, `hh:mm:ss` defaults to **12:00 AM**.

**More info:**  
- [ESRI Docs](https://doc.arcgis.com/en/arcgis-online/manage-data/work-with-date-fields.htm) 

---

## Workflow 1: Extract Datetimes from AGOL  
[Return to top](#working-with-datetime-in-arcgis-online-agol)  
Start by typing this code in your preferred IDE, such as Visual Studio Code or a jupyter notebook.  

### Step 1 - Connect to ArcGIS Online and Load Your Feature Layer
```python
from arcgis import GIS

gis = GIS(url=MAPHUB_URL, username=USERNAME, password=PASSWORD)
ago_item = gis.content.get(AGOL_ITEM_ID)                            # the AGOL item 
ago_flayer = ago_item.layers[0]                                     # load the first layer
```

### Step 2 - Load the AGOL Layer to a FeatureSet. 
**OPITONAL** pass a SQL query to only include certain features in the returned FeatureSet.  
See below for more information about formatting datetime queries.

```python
ago_fset = ago_flayer.query(where=SQL_QUERY)                        # Optional: filter with SQL
```

#### SQL Date Query Examples:
- `DateField = DATE 'YYYY-MM-DD'`
- `DateField >= TIMESTAMP 'YYYY-MM-DD HH:MI:SS'`

Any operator (>=, <=, >, <, <>) is supported.  

#### What timezone should I query in? 
If the feature service is timezone-aware, issue the query using the data's timezone.  
- e.g. if the feature service is in PST, the date and time in the WHERE clause should be in PST.  

If the feature service is not timezone-aware, issue the query in UTC. 

**More info:** 
- [ESRI Datetime Query Guide](https://www.esri.com/arcgis-blog/products/api-rest/data-management/querying-feature-services-date-time-queries)
- [Choosing the correct WHERE clause timezone](https://developers.arcgis.com/rest/services-reference/enterprise/query-feature-service-layer/)

### Step 3 - Convert FeatureSet to Spatial DataFrame
```python
ago_sdf = ago_fset.sdf                                              # convert layer to spatial dataframe
```

### Step 4 - Convert and Localize Datetime Fields
If you print out the values from any date columns in `ago_sdf`, they will be in UTC time and likely unformatted. The code snippet below shows how to convert the datetime fields to local timezone and format the time strings.

#### Step 4a - Convert to pandas datetime format
Here, the datetimes are formatted like YYYY-MM-DD hh:mm:ss. You can modify the `format` parameter in the `.to_datetime` function to format the date values differently.  
```python
import pandas as pd

ago_sdf[COLUMN_NAME] = pd.to_datetime(ago_sdf[COLUMN_NAME], format='%Y-%m-%d %H:%M:%S')
```
**More info:**  
- [Pandas to_datetime documentation](https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html)  

#### Step 4b - Localize to UTC if not timezone-aware 
Datetimes must be timezone aware before they can be converted to a different timezone. Choose the timezone of the current date values. Since dates and times are UTC in AGOL, we should localize these fields to UTC.  
```python

if ago_sdf[COLUMN_NAME].dt.tz is None:
    ago_sdf[COLUMN_NAME] = ago_sdf[COLUMN_NAME].dt.tz_localize('UTC')
```
**More info:**  
- [Pandas tz_localize documentation](https://pandas.pydata.org/docs/reference/api/pandas.Series.tz_localize.html)  
- [Timezone syntax](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) 

#### Step 4c - Convert to desired timezone (e.g., PST)
```python
ago_sdf[COLUMN_NAME] = ago_sdf[COLUMN_NAME].dt.tz_convert('America/Vancouver')
```
**More info:**  
- [tz_convert documentation](https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.tz_convert.html)

**[Link to full code snippet](#code-snippets)**
---

## Workflow 2: Upload Datetimes to AGOL  
[Return to top](#working-with-datetime-in-arcgis-online-agol)  
Start by typing this code in your preferred IDE, such as Visual Studio Code or a jupyter notebook.  

### Step 1 - Load and Prepare Your DataFrame
Pandas can read and write many filetypes. 

**More info:**  
- [Pandas read/write filetypes](https://pandas.pydata.org/docs/user_guide/io.html)

```python
import pandas as pd

# Replace with the path to your csv, or data in another format
df = pd.read_csv('path_to_your_file.csv')
```

### Step 2 - Convert to datetime
Here, the datetimes are formatted like `YYYY-MM-DD hh:mm:ss`. You can modify the `format` parameter in the `.to_datetime` function to format the date values differently. 
```python
import pandas as pd

df[COLUMN_NAME] = pd.to_datetime(df[COLUMN_NAME], format='%Y-%m-%d %H:%M:%S')
```
**More info:**  
- [Pandas to_datetime documentation](https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html)

### Step 3 - Localize to source timezone (e.g., PST)
Datetimes must be timezone aware before they can be converted to a different timezone. Choose the timezone of the current date values. In the example below, timezones in the csv document are recorded in PST. Therefore, we should localize the datetimes to `America/Vancouver`.   
```python
import pandas as pd

if df[COLUMN_NAME].dt.tz is None:
    df[COLUMN_NAME] = df[COLUMN_NAME].dt.tz_localize('America/Vancouver')
```

**More info:**  
- [Pandas tz_localize documentation](https://pandas.pydata.org/docs/reference/api/pandas.Series.tz_localize.html)  
- [Timezone syntax](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) 

### Step 4 - Convert to UTC for AGOL upload
Datetimes must be UTC to accurately display in AGOL. 
```python
import pandas as pd

df[COLUMN_NAME] = df[COLUMN_NAME].dt.tz_convert('UTC')
```
**More info:**  
- [tz_convert documentation](https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.tz_convert.html)

### Step 5 - Format and Upload to AGOL
#### Convert dataframe to AGOL-compatible features: 
Features added to an existing AGOL feature layer follow json format below. Replace the fields, values, and coordinates with data from the dataframe. I often loop through the dataframe to do so.  
```json
{
  "geometry": {
    "x": longitude, 
    "y": latitude,
    "spatialReference": {"wkid": 4326}
    },

  "attributes": {
    "FIELD1": "Value1",
    "FIELD2": "Value2",
    "FIELD3": "Value3",
    "FIELD4": "Value4"
  }
}
```
##### Here is an example function that converts a dataframe to AGOL json format:
Example dataframe:
| DATETIME_FIELD1 | DATETIME_FIELD2 | OTHER_FIELD | LATITUDE | LONGITUDE |
| --------------- | --------------- | ----------- | -------- | --------- |
| DATETIME1_VAL1 | DATETIME2_VAL1 | VALUE1 | LATITUDE1 | LONGITUDE1 |
| DATETIME1_VAL2 | DATETIME2_VAL2 | VALUE2 | LATITUDE2 | LONGITUDE2 |
| DATETIME1_VAL3 | DATETIME2_VAL3 | VALUE3 | LATITUDE3 | LONGITUDE3 |

Example function:
```python
import geopandas as gpd
import logging

def convert_df_to_agol_json_format(df):
    """Converts a pandas DataFrame with LONGITUDE and LATITUDE columns 
    into a list of features formatted for ArcGIS Online (AGOL) upload."""

    # convert to geopandas geodataframe with Point geometry
    gdf = gpd.GeoDataFrame(df.copy(), 
                            geometry=gpd.points_from_xy(df.LONGITUDE, df.LATITUDE), 
                            crs="EPSG:4326")
    logging.info("..successfully converted to geodataframe")

    # list to hold new features
    new_features = []

    # iterate through each row of the geodataframe
    for idx, row in gdf.iterrows():
        # convert row to plain dictionary (detaches from GeoDataFrame context)
        row_dict = row.to_dict()

        # extract and remove geometry from the dictionary
        geom = row_dict.pop("geometry", None)

        # dictionary to hold non-spatial feature attributes. The key is the field name and the value is the field value
        attributes = {}

        # iterate through each item in the plain dictionary
        for col, val in row_dict.items():

            # if the value is datetime or a pandas Timestamp, ensure it is in ISO format
            if isinstance(val, (datetime, pd.Timestamp)):
                attributes[col] = val.isoformat()
            else:
                attributes[col] = val

        # create the feature dictionary
        feature = {
            "attributes": attributes,
            "geometry": {
                "x": geom.x,
                "y": geom.y,
                "spatialReference": {"wkid": 4326}
            } if geom else {}
        }

        # append the feature to the list of new features
        new_features.append(feature)

    logging.info("..converted geodataframe to json format for upload to AGOL")

    return new_features
```
**More info:**  
- [Feature Attributes Documentation](https://developers.arcgis.com/rest/services-reference/enterprise/feature-object/) 

#### Append to data feature layer:
Inputs:  
- `new_features`: a list of features to append to the feature layer. See json format above for more details.
- `ago_flayer`: the AGOL feature layer, read in using the API

```python
import logging
from arcgis import GIS

def upload_to_ago(ago_flayer, new_features):
    """Appends features to AGOL layer."""

    # upload new features to existing AGOL feature layer
    result = ago_flayer.edit_features(adds=new_features)
    
    # error handling and logging of editing result
    try:
        # check if all the features were added successfully
        if all(res.get('success') for res in result.get('addResults', [])):
            # log a success message with the number of features added
            logging.info(f"..{len(new_features)} features added successfully.")
        else:
            # log an error if one or more features failed to add
            logging.error("..some features failed to add.")
            # log the full result object for debugging purposes
            logging.error(f"..full result: {result}")
    except Exception as e:
        # catch any unexpected errors during the result handling process and log the full exception traceback for easier debugging
        logging.exception(f"..unexpected error: {e}")
```
**More info:**  
- [Editing Features Documentation](https://developers.arcgis.com/python/latest/guide/editing-features/#adding-features)  

## Full Code Snippets
[Return to top](#working-with-datetime-in-arcgis-online-agol)  
### Workflow 1: Extract Datetimes from AGOL
```python
from arcgis import GIS
import pandas as pd

# load data from AGOL
gis = GIS(url=MAPHUB_URL, username=USERNAME, password=PASSWORD)
ago_item = gis.content.get(AGOL_ITEM_ID)                            # the AGOL item 
ago_flayer = ago_item.layers[0]                                     # load the first layer
ago_fset = ago_flayer.query(where=SQL_QUERY)                        # load the layer to a FeatureDataset with optional SQL query
ago_sdf = ago_fset.sdf                                              # convert FeatureDataset to spatial dataframe

# convert column to datetime data type
ago_sdf[COLUMN_NAME] = pd.to_datetime(ago_sdf[COLUMN_NAME], format='%Y-%m-%d %H:%M:%S')

# localize the datetime if not already timezone aware
if ago_sdf[COLUMN_NAME].dt.tz is None:
    ago_sdf[COLUMN_NAME] = ago_sdf[COLUMN_NAME].dt.tz_localize('UTC')

# convert the datetimes to the desired timezone
ago_sdf[COLUMN_NAME] = ago_sdf[COLUMN_NAME].dt.tz_convert('America/Vancouver')
```  

### Workflow 2: Upload Data to an Existing AGOL Feature Layer
```python
import pandas as pd
from arcgis import GIS
import logging

# read AGOL feature layer
gis = GIS(url=MAPHUB_URL, username=USERNAME, password=PASSWORD)
ago_item = gis.content.get(AGOL_ITEM_ID)                            # the AGOL item 
ago_flayer = ago_item.layers[0]                                     # load the first layer

# convert file to pandas dataframe (in this case we read a csv)
df = pd.read_csv('path_to_your_file.csv')                           # Replace with the path to your csv, or data in another format

# convert date column to datetime data type
df[COLUMN_NAME] = pd.to_datetime(df[COLUMN_NAME], format='%Y-%m-%d %H:%M:%S')

# localize source data time zone, if not assigned already
if df[COLUMN_NAME].dt.tz is None:
    df[COLUMN_NAME] = df[COLUMN_NAME].dt.tz_localize('America/Vancouver')

# convert timezone to UTC for upload to AGOL
df[COLUMN_NAME] = df[COLUMN_NAME].dt.tz_convert('UTC')

# loop through items in the dataframe and create a list of features for upload to AGOL. This will depend on your data structure
def convert_df_to_agol_json_format(df):
    """Converts a pandas DataFrame with LONGITUDE and LATITUDE columns 
    into a list of features formatted for ArcGIS Online (AGOL) upload."""

    # convert to geopandas geodataframe with Point geometry
    gdf = gpd.GeoDataFrame(df.copy(), 
                            geometry=gpd.points_from_xy(df.LONGITUDE, df.LATITUDE), 
                            crs="EPSG:4326")
    logging.info("..successfully converted to geodataframe")

    # list to hold new features
    new_features = []

    # iterate through each row of the geodataframe
    for idx, row in gdf.iterrows():
        # convert row to plain dictionary (detaches from GeoDataFrame context)
        row_dict = row.to_dict()

        # extract and remove geometry from the dictionary
        geom = row_dict.pop("geometry", None)

        # dictionary to hold non-spatial feature attributes. The key is the field name and the value is the field value
        attributes = {}

        # iterate through each item in the plain dictionary
        for col, val in row_dict.items():

            # if the value is datetime or a pandas Timestamp, ensure it is in ISO format
            if isinstance(val, (datetime, pd.Timestamp)):
                attributes[col] = val.isoformat()
            else:
                attributes[col] = val

        # create the feature dictionary
        feature = {
            "attributes": attributes,
            "geometry": {
                "x": geom.x,
                "y": geom.y,
                "spatialReference": {"wkid": 4326}
            } if geom else {}
        }

        # append the feature to the list of new features
        new_features.append(feature)

    logging.info("..converted geodataframe to json format for upload to AGOL")

    return new_features

# upload features to existing AGOL feature layer
def upload_to_ago(ago_flayer, new_features):
    """Appends features to AGOL layer."""

    # upload new features to existing AGOL feature layer
    result = ago_flayer.edit_features(adds=new_features)
    
    # error handling and logging of editing result
    try:
        # check if all the features were added successfully
        if all(res.get('success') for res in result.get('addResults', [])):
            # log a success message with the number of features added
            logging.info(f"..{len(new_features)} features added successfully.")
        else:
            # log an error if one or more features failed to add
            logging.error("..some features failed to add.")
            # log the full result object for debugging purposes
            logging.error(f"..full result: {result}")
    except Exception as e:
        # catch any unexpected errors during the result handling process and log the full exception traceback for easier debugging
        logging.exception(f"..unexpected error: {e}")

```
