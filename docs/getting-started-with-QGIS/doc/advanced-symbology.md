# Advanced symbology in QGIS

[home](readme.md)

Index
* [Getting Started](#getting-started)
* [Symbolizing the Road Layer](#symbolizing-the-road-layer)
* [Symbolizing the Parks Layer](#symbolizing-the-parks-layer)

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

With the layer categorized you can start changing the line symbols. Double click the highway symbol to open its Symbol selector. Click the green + button to add a new line. Make the top line size 0.8 and yellow. Make the lower line size 1.0 and black. Click OK to exit the Symbol selector and OK to exit the Layer properties.

![Change the Highway Symbology](../images/highway-symbology.gif "Wow!")

You'll notice that the line caps still show up at each section of the highway line. You can remove these in the Advanced section of the layer symbology properties by turning on Symbol levels.

![Turn on Symbol Levels](../images/turn-on-symbol-levels.gif "Wow!")

Make the yield roads the same as highways but slightly thinner with the yellow line as 0.5 and the black line as 0.7. Make Collector roads solid black 0.4 and arterial roads solid black 0.3. Make local roads medium grey 0.3.

Unclassified roads on this map are trails. So you'll want to make their symbol smaller and less eye catching than the roads and with some indication that they are trails. To do this open the symbol properties for this layer and create two lines using the + button. Change the Symbol layer type of both lines to Marker line. Change the interval of the upper line to 30 and then make it an SVG marker and make the SVG the image of the person hiking and increase the size to 3.0. Make the second marker line a brown dashed line with size 1.0. Turn off rotation in the hiking person marker line.

![Marker Lines](../images/marker-line.gif "Wow!")

## Symbolizing the Parks Layer
The parks layer contains simple polygons that show the locations and areas of parks within BC. The default symbology is a basic solid fill that doesn't really have any indication of what the layer is symbolizing.

Open the layer properties for the parks layer and navigate to the symbology tab. You can examine and experiment with the different fill types here. For this exercise, pick the Shapeburst Fill type. Change the colours to dark green for the first colour and lighter green for the second colour. Change the Shading type from Whole shape to Set distance and make it 50 Meters at scale.

![Shapeburst Fill](../images/adv_sym_shapeburstFill.gif "Wow!")

Now you can tell by the layer's symbology that it is likely a park but you can't see any information about the park. So, let's add a label with the park name. Open the layer's properties and navigate to the Labels tab. Turn on Single Labels and set it to PARK_NAME. Change the font to one you like and set the size to 7 points. Change the font colour to the same light green used for the fill and add a dark green buffer around the text (size: 0.7 points). Make sure the lines wrap at 7 characters and that only labels that fit inside the park are displayed and change the placement to Free (optional).

![Turn on Labels](../images/adv_sym_labels.gif "Wow!")
