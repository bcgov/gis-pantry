# Advanced symbology in QGIS

[home](../readme.md)


Index
* [Getting Started](#getting-started)
* [Symbolizing the Road Layer](#symbolizing-the-road-layer)
* [The Area Function](#the-area-function)
* [The Scale Function](#the-scale-function)



## Getting Started

The type of symbology you should use on a map is dependent on many factors but the main factors are geometry type (point, line, or polygon), scale, and density.

Point Symbols
Point symbols are features that cannot be represented by their true geometry or features where the true geometry has not been captured. Examples include trees, windmills, and even houses at small scales. Point symbols can be divided into three symbology classes:
1) Plan symbols are the most common and simply show features as a dot, square, or other shape that doesn’t give any information about the feature.
2) Profile symbols give 2D representations of flattened features that show a rough depiction of the feature
3) Functional symbols show an action taking place. These are commonly used on park maps where a square with a person fishing, cycling, or swimming depicts that these activities are allowed at the park.

Line Symbols
Line symbols are features that have 1 dimension: length. They can have a width attribute but it is not inherent to their geometry as it would be with a polygon. Lines are sometimes depicted as a single line but are more commonly depicted as multiple lines wherein a train track would have a thin black centre line and cross hatches running through it at a set interval.

Polygon Symbols
Polygons are 2D shapes that have a length and a width attribute. In terms of symbology they usually are depicted with a light coloured fill and a slightly darker outline around their perimeter.

Symbology on Your Map
For this exercise you will need three layers:

* [Kamloops Trees Point Layer](https://mydata-kamloops.opendata.arcgis.com/datasets/trees)
* [The Digital Road Atlas](https://catalogue.data.gov.bc.ca/dataset/digital-road-atlas-dra-master-partially-attributed-roads#edc-pow)
* [The Local and Regional Greenspaces Polygons](https://catalogue.data.gov.bc.ca/dataset/local-and-regional-greenspaces)

Load the three layers listed above to a blank map and ensure the Coordinate System is set to BC Albers (EPSG: 3005).

Once you’ve loaded the layers you will want to zoom in to an area in Kamloops with some parks. I chose the area surrounding of Valleyview Nature Park in Kamloops but any area in Kamloops will work.

## Symbolizing the Road Layer
When you first load the DRA you will notice that all the lines look more or less the same. The highways are recognizable because they have double lines but, other than that, every road type is symbolized identically.
Right click the road layer and go to its Properties and in the Properties box navigate to its Source. Open the Query Builder and add the Definition Query:

```sql
"ROAD_CLASS" IN ('arterial','collector','highway','local','unclassified','yield')
```

Click Apply and then navigate to the Symbology tab in the properties menu.
Change the Symbol type to Categorized and the Column to ROAD_CLASS. Click Classify.

![Categorize the Line Layer](../images/categorize_line_layer.gif "Wow!")
