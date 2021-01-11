# Expressions and Filter Queries

[home](../readme.md)

## Index
* [Definition Query / Filter](#Definition-Query-/-Filter)
  * [Basic queries](#basic-queries)
  * [Queries on multiple columns with AND](queries-on-multiple-columns-with-and)
  * [Queries on multiple columns with OR](queries-on-multiple-columns-with-or)
* [Select by attribute query](#Select-By-Attribute-Query)
* [Geometry Expressions](#geometry-expressions)
* [Geometry Generator (Layer Style)](#geometry-generator-(layer-style))
   *  [Getting Started](#getting-started)
   *  [The Centroid Function](#the-centroid-function)
   *  [The Area Function](#the-area-function)
   *  [The Scale Function](#the-scale-function)
* [Label Expressions](#label-expressions)
   *  [Adding a dynamic date variable](adding-a-dynamic-date-variable)
   *  [Adding an attribute from a layer](adding-an-attribute-from-a-layer)
   *  [Aggregating the length of multiple road sections](aggregating-the-length-of-multiple-road-sections)
   *  [Iterators and Multiple Rows of data](iterators-and-multiple-rows-of-data)
   *  [Start and End Points and Coordinate System Transformations](start-and-end-points-and-coordinate-system-transformations)

## Definition Query / Filter

## Basic queries

* open QGIS and add the [Kamloops Trees Point Layer](https://mydata-kamloops.opendata.arcgis.com/datasets/trees)
* double click the layer in the layer tree to open its properties menu
* click the **Query Builder** button to open the menu to add a new query
* enter the following Query:

```sql
"SPECIES" IN ('apple','arborvitae')
```

![accessing the definition query menu](../images/exp_IN.gif "Wow!")

* Navigate back to the query and change it to:

```sql
"SPECIES" NOT IN ('apple','arborvitae')
```

## Queries on multiple columns with AND

* Navigate back to the query and change it to:

```sql
"SPECIES" IN ('apple','arborvitae') AND "SPREAD" > 2
```

## Queries on multiple columns with OR

* Navigate back to the query and change it to:

```sql
"SPECIES" IN ('apple','arborvitae') OR "SPREAD" = 2
```

Some common query operators are:

* =       *Field value is exactly equal to the specified value*
* <>      *Field value is not equal to the specified value*
* !=      *Field value is not equal to the specified value*
* LIKE    *Field text value is equal or partially equal (using fuzzy logic) to the specified value*
* AND     *Allows adding multiple queries that must all be met*
* OR      *Allows adding multiple queries where one or more must be met*

Wildcards can be used to substitute any other characters in a string using the LIKE operator. Some common operators are:

* %       *Replaces an unlimited number of characters or no characters - characters can be numbers or letters*
* _       *Replaces a single character in a string*
* [list]  *Matches characters in a list*
* [^list] *Matches characters not specified in a list*
* [!list] *Matches characters not specified in a list*

* Navigate back to the query and change it to:

```sql
"SPECIES" LIKE 'a%'
```

For more information on all operators available in QGIS see the [QGIS documentation](https://docs.qgis.org/3.16/en/docs/user_manual/working_with_vector/vector_properties.html?highlight=query%20builder#query-builder)

## Select by attribute query

## Geometry Expressions

## Geometry Generator (Layer Style)

## Getting Started

QGIS allows feature data types to be changed without creating a new layer through the geometry generator.

[The following examples use the layers below:](#adding-data-from-layer-library)
* [WHSE_LAND_AND_NATURAL_RESOURCE.PROT_HISTORICAL_FIRE_POLYS_SP](https://catalogue.data.gov.bc.ca/dataset/fire-perimeters-historical#edc-pow)
* [WHSE_ADMIN_BOUNDARIES.ADM_NR_DISTRICTS_SP](https://catalogue.data.gov.bc.ca/dataset/natural-resource-nr-district#edc-pow)

Query the Historical Fire layer to only show fires from 2017.
```sql
"FIRE_YEAR" = 2017
```
Make sure the fire layer is displayed above the NR District layer.

![Filter the Fire Layer](../images/filterFireLayer.gif "Wow!")

## The Centroid Function
The Centroid function is used to convert polygons to points based on the centroid coordinates of the polygon. It is used for data conversion purposes.

Double click the Historical Fire layer to enter its layer properties and navigate to the symbology tab. Change the symbology from Simple fill to Geometry generator and set the Geometry type to Point / MultiPoint.

Click the Epsilon button beside the code block to open the Expression Dialog window if it doesn't automatically appear. You can take some time at this point to explore different expressions that are displayed in the centre block of the dialog.

In the code block, enter the following code:
```python
Centroid($geometry)
```

Click Apply and OK to exit the window.

Now every fire on the map is displayed as a point and you should be able to see some fires that weren't visible before.

![Using the Centroid function in Geometry Generator](../images/geometryGeneratorPolyToPoint.gif "Wow!")


## The Area Function
The $area function is used to give the area of a polygon feature as a real number. It has lots of uses but, when using it in the Geometry Generator, it is generally reserved for conditional statements.

Open the properties of the Historical Fire layer and create a Geometry generator symbol with the Geometry type Point / MultiPoint if this does not already exist. Add the following code to the code block:

```sql
if(
	$area / 10000 < 1000,
	centroid($geometry),
	Null
)
```

This will make fires smaller than 1,000 hectares display as points on the map but not display the fires larger than 1,000 hectares.

Add another Geometry generator below the Point / MultiPoint symbol. Leave the settings as default and enter the Expression Dialog. Enter the following expression:

```sql
if(
	$area/10000 >= 1000,
	$geometry,
	Null
)
```

This will make all the polygons larger than or equal to 1,000 hectares appear as polygons on the map.

![Using the Area function in Geometry Generator](../images/geometryGeneratorArea.gif "Wow!")

## The Scale Function

The Geometry Generator can also support scale dependent geometry with the @map_scale function. @map_scale returns the numerical scale of the current map and can be used for conditionals that change how layers are displayed when you zoom in or out of a map.

If you haven't already, create two geometry generators in the Historical Fire layer. Make one have the Geometry type Point / MultiPoint and the other Polygon / MultiPolygon.

Enter the following code into the Expression Dialog for the Point / MultiPoint layer:

```sql
if(
	@map_scale > 250000,
	if(
		$area/10000 < 1000,
		centroid($geometry),
		Null
	),
	Null
)
```

Now enter the following code into the Expression Dialog for the Polygon / MultipPolygon layer:

```sql
if(
	@map_scale > 250000,
	if(
		$area/10000 >= 1000,
		$geometry,
		Null
	),
	$geometry
)
```

Press Apply and OK to exit the Layer Properties. Now into and out of the map. Notice how the points turn to polygons when you zoom in beyond 1:250,000 in scale.

## Label Expressions

Label expressions are sets of code that are written directly in labels in QGIS map layouts. They range from simple expressions that automatically update the date when a map is opened to complex expressions that read and alter values stored in a layer's attribute table and/or geometry.

To start you'll need to open a blank map and create a print layout. If you aren't familiar with creating print layouts please see the [making maps](https://github.com/bcgov/gis-pantry/blob/master/docs/getting-started-with-QGIS/doc/making-maps.md) section of this guide.

## Adding a dynamic date variable
* Create a blank map layout
* Add a label by selecting Add Label from the Add Item dropdown list
* Select the label and then click the Insert an Expression... button in the label properties
* for the expression, enter the following text:
```sql
format_date(now(),'MMMM dd, yyyy')
```
* Click OK

You should see that the textbox automatically prints todays date as Month day, year (November 19, 2020). The reason it prints this way is because MMMM tells the system to print the month as text. dd prints the day as a two digit day and yyyy prints the year as a four digit year. For more information on formatting dates see the [QGIS documentation section 14.3.7.6](https://docs.qgis.org/3.16/en/docs/user_manual/working_with_vector/functions_list.html#date-and-time-functions).

To break this date code down further it uses two functions: format_date and now().

The format_date function is simple. It is written as format_date(datetime,format*,language*) with language being an optional variable for languages other than your QGIS installation language. The datetime variable can be set as an actual date such as '2020-11-01' or can use a function such as now(). The format is written as an expression as listed in the QGIS documentation linked above or by searching format_date in the QGIS Expression window.

## Adding an attribute from a layer
Adding attributes from a layer is only slightly more difficult that adding a date because you have to reference a layer and a field and sometimes an aggregate function.

To follow along with this section you will need the [FTEN road section lines dataset](https://catalogue.data.gov.bc.ca/dataset/forest-tenure-road-section-lines#edc-pow).

* Load the road section lines data set into the map
* Add a definition query to the layer:

if using the shapefile downloaded from the BC government data directory:
```sql
"FFID" LIKE 'R23206'
```

if using the Oracle database layer:
```sql
"FOREST_FILE_ID" LIKE 'R23206'
```

* Add a new label to the print layout
* Select the label and then click the Insert an Expression... button in the label properties
* Enter the following expression:

if using the shapefile downloaded from the BC government data directory:
```sql
aggregate('layer_name','max',"FFID")
```

if using the Oracle database layer:
```sql
aggregate('layer_name','max',"FOREST_FILE_ID")
```

replace layer_name with your layer's name which can be found in the Map Layers menu as shown below.

![Aggregate layer name](../images/exp_aggregate1.gif "Wow!")

* Click OK and look at your label. It should now show the road's code - R23206

To break this expression down. You are creating a label that shows a text attribute from a layer that has a definition query limiting it to one road code but multiple sections. The aggregate function tells QGIS that there is more than one section - it still works with just one section - and that you only want to return a single label. The max aggregate was used but min would return the same thing in this situation as we know there is only one ID.

This is a false aggregate. You know you want to return a single label and that each line of this attribute is the same so you can just use the min or max functions to return the label you want. But, sometimes, you want to return an aggregate from a field with different values.

## Aggregating the length of multiple road sections
In this example you will use the same road sections but rather than printing the road ID you will print the sum, min, and max length of the sections.

* Add a new label anywhere on the print layout
* Enter the Insert Label Expression... window
* Enter the following code:

if using the shapefile downloaded from the BC government data directory:
```sql
'Max: '
+
to_string(
	aggregate('layer_name'
,'max'
,"FEAT_LEN"))
+
'\nMin: '
+
to_string(
	aggregate('layer_name'
,'min'
,"FEAT_LEN"))
+
'\nSum: '
+
to_string(
	aggregate('layer_name'
,'sum'
,"FEAT_LEN"))
```

if using the Oracle database layer:
```sql
'Max: '
+
to_string(
	aggregate('layer_name'
,'max'
,"FEATURE_LENGTH_M"))
+
'\nMin: '
+
to_string(
	aggregate('layer_name'
,'min'
,"FEATURE_LENGTH_M"))
+
'\nSum: '
+
to_string(
	aggregate('layer_name'
,'sum'
,"FEATURE_LENGTH_M"))
```

Again, replace layer_name with your layer's name.

This code looks more intimidating than the previous example but it is actually mostly the same. The main difference is that it has multiple code sections and text sections separated with the + symbol which tells QGIS to join the sections as text. Also, the to_string() function tells the system to print the result as a string.

The result you should see in the label is a list of numbers similar to:

Max: 5997.0419
Min: 461.0144
Sum: 10222.712800000001

You'll notice the significant digits for the sum are very long. You can fix this by changing the code to:

if using the shapefile downloaded from the BC government data directory:
```sql
'\nSum: '
+
to_string(
	round(
		aggregate(
			'FTEN_RS_LN_line_229d83ad_5760_451c_b997_b7205739a282'
			,'sum'
			,"FEAT_LEN"
		),2
	)
)
```

if using the Oracle database layer:
```sql
'\nSum: '
+
to_string(
	round(
		aggregate(
			'FTEN_RS_LN_line_229d83ad_5760_451c_b997_b7205739a282'
			,'sum'
			,"FEATURE_LENGTH_M"
		),2
	)
)
```

## Iterators and Multiple Rows of data

Sometimes, rather than aggregating all the rows of data, you will need to show information from each individual row. This can be accomplished by using an iterator (function that reads and writes data from each row) rather than an aggregate. In QGIS, iterators are stored as aggregates with the concatenate attribute. They are written as:

```sql
aggregate(
	layer:='your_layer',
	aggregate:='concatenate',
	expression:=[your_expression]
)
```

where [your_expression] is an sql expression without the brackets.

Using our road layer, you could write a simple expression to show the length of each segment of road and its section label using the following code:

if using the shapefile downloaded from the BC government data directory:
```sql
aggregate(
	layer:='FTEN_RS_LN_line_229d83ad_5760_451c_b997_b7205739a282'
	,aggregate:='concatenate'
	,expression:="RD_SECT_ID" + ' ( Length: ' + to_string ("FEAT_LEN" / 1000) + 'Km )\n'
)
```

if using the Oracle database layer:
```sql
aggregate(
	layer:='FTEN_RS_LN_line_229d83ad_5760_451c_b997_b7205739a282'
	,aggregate:='concatenate'
	,expression:="ROAD_SECTION_ID" + ' ( Length: ' + to_string ("FEATURE_LENGTH" / 1000) + 'Km )\n'
)
```

A couple of things to note with this expression are: (1) all numbers need to be converted to strings to be displayed as text; (2) The layer name has a code generated after it that is unique to your map - always get your layer name from the Map Layers list in your expression dialogue box.

## Start and End Points and Coordinate System Transformations

The previous example is a simple starting point but it gets more complicated when you want to show start and end points of a line in a different coordinate system than the data is stored in. Luckily, QGIS allows you to perform data transformations within your label expression so you don't have to make copies of your data in separate files.

Lets edit our previous expression to do this:

if using the shapefile downloaded from the BC government data directory:
```sql
aggregate(
	layer:='FTEN_RS_LN_line_229d83ad_5760_451c_b997_b7205739a282'
	,aggregate:='concatenate'
	,expression:="RD_SECT_ID"
	+
	' ( Length: '
	+
	to_string(
		"FEAT_LEN" / 1000
	)
	+
	'Km )'
	+
	'PofC UTM10'
	+
	to_string(
		to_int(
			x(
				transform(
					point_n(
						$geometry, 1
					),
					'EPSG:3005', 'EPSG:26910'
				)
			)
		)
	)
	+
	'PofT UTM10'
	+
	to_string(
		to_int(
			x(
				transform(
					point_n(
						$geometry, -1
					),
					'EPSG:3005', 'EPSG:26910'
				)
			)
		)
	)
	+
	'\n'
)
```

if using the Oracle database layer:
```sql
aggregate(
	layer:='FTEN_RS_LN_line_229d83ad_5760_451c_b997_b7205739a282'
	,aggregate:='concatenate'
	,expression:="ROAD_SECTION_ID"
	+
	' ( Length: '
	+
	to_string(
		"FEATURE_LENGTH" / 1000
	)
	+
	'Km )'
	+
	'PofC UTM10'
	+
	to_string(
		to_int(
			x(
				transform(
					point_n(
						$geometry, 1
					),
					'EPSG:3005', 'EPSG:26910'
				)
			)
		)
	)
	+
	'PofT UTM10'
	+
	to_string(
		to_int(
			x(
				transform(
					point_n(
						$geometry, -1
					),
					'EPSG:3005', 'EPSG:26910'
				)
			)
		)
	)
	+
	'\n'
)
```
This code looks complicated but it is fairly easy once you begin to understand the functions. to_string and to_int are conversions: to_int converts the data to a integer rather than a decimal number; to_string converts the integer to a string that can be printed in the label.

x [x(geom)] tells the system that we want the x coordinate of the object.

transform [transform(geom,source_auth_id,dest_auth_id)] is a conversion that changes the coordinate system. In this case, the line 'EPSG:3005', 'EPSG:26910' tells the system that we are converting the data from EPSG:3005 (BC Albers) to EPSG:26910 (UTM 10N).

point_n [point_n(geometry,index)] returns a specific node from a geometry - in this case a road section line - and the index is the point on the line you want to print. The index can be any node along the line and 1 always represents the start point while -1 always represents the end point.

$geometry [$geometry] returns the geometry of the current feature that is used as the layer in the aggregate function and is used for processing in the other functions.

In this case we only printed the x coordinates but by replacing x with y in this code we could print the y coordinates instead.
