# ArcGIS Online Recipies
Templates, examples and snippets using:
* HTML
* Arcade expressions
* Python (ArcGIS API for Python)

Example:

#### Custom Attribute Display using featuresets
```
// get the count for all trees in the Neighborhood

var trees = FeatureSetByName($map,"Urban Forestry")
var countTrees = Count(Intersects(trees,$feature))
return countTrees
```


#### Contents:
--------
1. AGO_AddFeatureClassAsJSON.py

*This script uploads all feature classes in a given file geodatabase (.gdb) to your ArcGIS Online (AGO) content page. It requires the ArcGIS Pro Python environment to run (needs access to arcgis.gis module). The ArcGIS Pro Python environment can be found on the BCGOV Geospatial Desktop.*