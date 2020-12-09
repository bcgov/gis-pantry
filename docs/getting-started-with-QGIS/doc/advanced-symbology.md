# Advanced symbology in QGIS

[home](readme.md)

Index
* [Getting Started](#getting-started)
* [Symbolizing the Road Layer](#symbolizing-the-road-layer)
* [Symbolizing the Parks Layer](#symbolizing-the-parks-layer)
* [Symbolizing the Trees Layer](#symbolizing-the-trees-layer)

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
When you first load the Digital Road Atlas you will notice that all the lines look more or less the same. The highways are recognizable because they have double lines but, other than that, every road type is symbolized identically.

* Right click the road layer and enter its Properties menu
* navigate to the Source tab
* Open the Query Builder and add the following Definition Query:

```sql
"ROAD_CLASS" IN ('arterial','collector','highway','local','unclassified','yield')
```

* Click Apply
* navigate to the Symbology tab
* Change the Symbol type to Categorized and the Column to ROAD_CLASS
* Click Classify to get a list of all possible values

![Categorize the Line Layer](../images/categorize_line_layer.gif "Wow!")

With the layer categorized you can start changing the line symbols.
* Double click the highway symbol to open its Symbol selector
* Click the green + button to add a new line
* Make the top line size 0.8 and yellow
* Make the lower line size 1.0 and black
* Click OK to exit the Symbol selector and OK to exit the Layer properties

![Change the Highway Symbology](../images/highway-symbology.gif "Wow!")

You'll notice that the line caps still show up at each section of the highway line. You can remove these in the Advanced section of the layer symbology properties by turning on Symbol levels.

* Click the Advanced button at the bottom right of the symbology window and from the drop down select Symbol levels...
* Ensure the Enable Symbol Levels checkbox is checked to turn enforce symbol levels for the layer
* Click OK in the box to leave everything as default

![Turn on Symbol Levels](../images/turn-on-symbol-levels.gif "Wow!")

* Make the yield roads the same as highways but slightly thinner with the yellow line as 0.5 and the black line as 0.7
* Make Collector roads solid black 0.4 and arterial roads solid black 0.3. Make local roads medium grey 0.3.

Unclassified roads on this map are trails. So you'll want to make their symbol smaller and less eye catching than the roads and with some indication that they are trails.
* Open the symbol properties for Unclassified roads and create two lines using the + button
* Set the Symbol layer type property to Marker line for both lines
* Set the interval of the upper line to 30
* In the lowest, third, symbol in the symbology tree, set the Symbol layer type to SVG marker
* Set the SVG as an image of a person hiking and increase the size to 3.0
* Set the second marker line as a brown dashed line with size 1.0
* Turn off rotation in the hiking person marker line

![Marker Lines](../images/marker-line.gif "Wow!")

## Symbolizing the Parks Layer
The parks layer contains polygons that show the locations and areas of parks within BC. The default symbology is a basic solid fill that doesn't have any indication of what the layer is symbolizing.

* Open the layer properties for the parks layer and navigate to the symbology tab
* Set the Fill type to Shapeburst Fill
* Set the first colour as dark green
* Set the second colour as a lighter green
* Change the Shading type from Whole shape to Set distance and make it 50 Meters at scale

![Shapeburst Fill](../images/adv_sym_shapeburstFill.gif "Wow!")

Now you can tell by the layer's symbology that it is likely a park but you can't see any information about the park. So, let's add a label with the park name.
* Open the layer's properties and navigate to the Labels tab
* Turn on Single Labels
* Set the Value as PARK_NAME
* Select a font you like and set the size to between 7 and 9 points
* Set the font colour to the same light green used for the area fill
* Navigate to the Buffer tab and add a dark green buffer around the text (size: 0.7 mm)
* Ensure Draw text buffer is checked in the buffer tab
* Navigate to the Formatting tab and set Wrap lines to 7 characters
* Navigate to the Rendering tab and at the bottom of the menu check Only draw labels which fit completely within the feature
* Navigate to the placement tab and set the Mode to Free (Angled)

![Turn on Labels](../images/adv_sym_labels.gif "Wow!")

## Symbolizing the Trees Layer
The trees layer is points that show the location of trees within Kamloops. QGIS offers several ways to display points that can be useful.

###### Single Symbol symbology
The first type of symbology we will analyze is the default style, Single Symbol, where one symbol shows all of the layers. This symbology is pretty basic but deserves some discussion.
Enter the layer properties for the Trees layer and try changing the Simple Marker drop down to SVG symbol, Vector symbol, and Font Marker and play with the colours and sizes. You'll notice that you can generally find a symbol that works well for large clusters of points while still working for individual points. Here, I will use an Simple marker of a dot to show each point and reduce it's size to .80 points.

![Turn on Labels](../images/adv_sym_simpleMarker.gif "Wow!")

You can also change the stroke width (the size of the outline around the point), x (left-right) and y (up-down) offset of the point, and stroke style of point. You can experiment with these settings throughout this guide as you see fit but, like colouring, they are very subjective and thus will not explicitly be covered. However, it is important that you know these settings exist.

###### Categorized symbology
Another useful symbol style for points is Categorized. This allows you to display different symbols for different categories of points and you will probably find that you use this more often than most others. Here we will symbolize the trees based on their TYPE field.

* Open the Properties dialog for the Trees layer and change the top dropdown to Categorized.
* Set the value to TYPE and then click classify.
* Adjust the symbology for each type of tree as you see fit.
* Click Apply or OK to see your changes.

![Turn on Labels](../images/adv_sym_categorized.gif "Wow!")

###### Graduated symbology
The graduated symbology style is very useful when you want to display points based on a meaningful numeric attribute such as buffer size, area, or height. In this case we know the spread of the tree from the SPREAD field and can use this as our graduated attribute.

* Enter the properties menu and change the top menu to Graduated.
* Change the value to SPREAD and the Method to Size.
* You can adjust the Symbol and Size from and To values as you see fit.
* You can adjust the classification Mode and change the number of classes to fit the data when appropriate.
* Click Apply or OK to view the symbols.

![Turn on Labels](../images/adv_sym_graduated.gif "Wow!")

###### Rule-based symbology
The last type of symbology in QGIS to be discussed in this section is Rule-Based. This is similar to Categorized except you can define your own categories using SQL code. This is the most advanced and most powerful classification technique.

* Enter the properties menu and change the top menu to Rule Based.
* Click the + button to add a rule.
* Label the rule as "Coniferous Trees > 7"
* Enter the expression:  "TYPE" LIKE  'CONIFEROUS' AND  "SPREAD" > 7
* Enter "Coniferous trees with greater than 7m spread" in the description
* Click OK
* Add another rule but this time label it as "Deciduous Trees > 1"
* Enter the expression:  "TYPE" LIKE  'DECIDUOUS' AND  "SPREAD" > 1
* Enter "Deciduous trees with greater than 1m spread in the description"
* Click OK
* Add another rule but this time select Else rather than entering an expression
* Label it as "other"
* Click OK

![Turn on Labels](../images/adv_sym_ruleBased.gif "Wow!")
