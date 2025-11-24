# Feature Service Updater

Python class for updating ArcGIS Online (AGOL) feature services from local sources.

## Description

This script updates AGOL feature services by exporting source data to a temporary File Geodatabase, zipping it, uploading to AGOL, and appending to the target feature service. It supports both upsert (update/insert) and truncate/append update methods, handles schema synchronization, and manages sync settings.

## Requirements

- ArcGIS Pro with arcpy
- arcgis Python API
- ArcGIS Online credentials

## Usage

```python
from feature_service_updater import FeatureServiceUpdater

# Initialize the updater
updater = FeatureServiceUpdater("username", "password")

# Update a feature service using upsert method
updater.overwrite(
    feature_class=r"C:\path\to\data.gdb\feature_class",
    item_id="your_agol_item_id",
    layer_or_table="layer",
    index=0,
    upsert=True,
    unique_field="unique_id_field",
    update_schema=True
)

# Update using truncate/append method
updater.overwrite(
    feature_class=r"C:\path\to\data.gdb\feature_class",
    item_id="your_agol_item_id",
    layer_or_table="layer",
    index=0,
    upsert=False,
    disable_sync=True,
    update_schema=True
)
```

## Parameters

**overwrite() method:**
- `feature_class`: Path to source feature class or table
- `item_id`: AGOL feature service item ID
- `layer_or_table`: Either "layer" or "table"
- `index`: Layer/table index in the feature service (default: 0)
- `upsert`: Use upsert method if True, truncate/append if False (default: False)
- `unique_field`: Field name for upsert matching (required if upsert=True)
- `disable_sync`: Disable sync to reset OBJECTIDs during truncate (default: False)
- `update_schema`: Synchronize schema between source and service (default: False)

## Notes

- Schema synchronization adds/removes fields to match source data
- Upsert method requires a unique field with unique index

## Author

LAPERRY, MCM MCAD Regional Operations  
Date Created: 2025-08-19

## References

Modified from: [Overwrite ArcGIS Online Feature Service Using ArcGIS API for Python](https://community.esri.com/t5/arcgis-online-documents/overwrite-arcgis-online-feature-service-using/ta-p/90445)
