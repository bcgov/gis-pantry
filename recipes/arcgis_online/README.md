# ArcGIS Online Recipies
Templates, examples and snipits using html and Arcade expressions

Example:

Custom Attribute Display using featuresets
```
// get the count for all trees in the Neighborhood

var trees = FeatureSetByName($map,"Urban Forestry")

var countTrees = Count(Intersects(trees,$feature))

return countTrees
```