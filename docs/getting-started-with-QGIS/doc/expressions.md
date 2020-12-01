# Expressions and Filter Queries

[home](../readme.md)

## Definition Query / Filter

Definition Queries are strings that can make data layers more readable by telling the layer to exclude certain data based on attributes. For example you may only want to see data for parks of a certain size or exclude roads that aren't highways from a dataset.

Here, I will provide a few examples of how to filter data based on attributes using the IN, LIKE, =, <>, AND, and OR operators. For more information on all operators available in QGIS see the [QGIS documentation](https://docs.qgis.org/3.16/en/docs/user_manual/working_with_vector/vector_properties.html?highlight=query%20builder#query-builder)

* Open QGIS and add the [Kamloops Trees Point Layer](https://mydata-kamloops.opendata.arcgis.com/datasets/trees)
* Double click the layer in the layer tree to open its properties menu
* Click the Query Builder button to open the box to create a new query

![Using the Area function in Geometry Generator](../images/exp_IN.gif "Wow!")

* Enter the following Query:
```sql
"SPECIES" IN ('apple','arborvitae')
```
You'll notice that the number of points on the map is dramatically reduced. This is because the data set now only shows apple and arborvitae trees and excludes everything else.

* Navigate back to the query and change it to:

```sql
"SPECIES" NOT IN ('apple','arborvitae')
```

Now every tree that is not an apple or arborvitae tree is shown on the map. The IN function allows you to provide a list of attributes to include, or exclude, from a data set by typing them inside parenthesis. Text field values should be surrounded by single quotes while number fields should not have quotes.

If you want to have queries on multiple fields you can do this using the AND or OR operators.

* Navigate back to the query and change it to:

```sql
"SPECIES" IN ('apple','arborvitae') AND "SPREAD" > 2
```

Notice that the spread attribute does not have quotes because it is a number field.
This query returns all of the apple and arborvitae trees that have a spread that is greater than 2. If you replace AND with OR it will return all the apple and arborvitae trees as well as all the trees with a spread greater than 2 regardless of their species.

* Navigate back to the query and change it to:

```sql
"SPECIES" IN ('apple','arborvitae') AND "SPREAD" = 2
```

The = operator returns numbers or text that are exactly equal to the number or text provided. For text fields, it is generally accepted that the LIKE operator should be used in place of = but both work, however, only the LIKE operator allows the use of wildcards. Replacing = with <> or != changes it to not equal to which finds all the values not equal to the number or text provided. NOT LIKE does the same thing but only with text fields.

* Navigate back to the query and change it to:

```sql
"SPECIES" LIKE 'a%'
```

This query filters the layer to only show species of trees that start with the letter a. The % wildcard tells the layer to look for any number of letters or numbers. Adding the letter a before % says look for strings starting with a and then containing anything after that regardless of the length of the string or whether it has letters, numbers, or both.

Other wildcard operators include _ (any character)

## Select by attribute query

## Geometry Expressions

## Geometry Generator (Layer Style)

Index
* [Getting Started](#getting-started)
* [The Centroid Function](#the-centroid-function)
* [The Area Function](#the-area-function)
* [The Scale Function](#the-scale-function)

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

###### Adding a dynamic date variable
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

###### Adding an attribute from a layer
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

###### Aggregating the length of multiple road sections
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
