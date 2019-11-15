# BCTS Route Card (TOC)
## Usage
**Terms**
Route Card – A term used in the TOC region for a spatial and non spatial check to ensure any planned blocks and roads are not impeding on areas where there are constraints on the land or areas where harvesting is not allowed.

**Overview and Background**
The Route Card pilot project was started to assist the Planners in the BCTS Okanagan and Columbia Business Area with the Route Card creation. This tool is not to be used as the final authority on information reported on Route Cards but rather a tool that allows the Planners to see the initial overlays of a block and all information that is spatially related to it, additional information must be filled in by the signing authority of the Route Card. 

## Requirements
Requires ESRI ArcView licensing & ArcMap 10.x.

## Getting Help or Reporting an Issue
Use the Issues tab to get help or report any issues.

## Tool Description:

This tool was developed to be as simple as possible for the planners who will be using it on a day to day basis, it was  developed to have minimal inputs from the user as well as originally work in conjunction with the Cengea GEO environment that is already being used by the Business Area. Since the initial design the Route Card tool is now a stand-alone map product that runs based off of a single selected feature in the defined road and block feature class.
This tool was developed using Python coding language with a majority of the variables being stored in an external database table. The variables have been stored in an external table for future developments, if this tool is to be used by other business area’s (BA)  it is best to have a dynamic script that reads a table that can be updated and changed based on the BA’s needs. The tool only requires the user has access to a ArcVIew (Basic) license level for ESRI ArcMap. It is planned that for the majority of the assessments, the tool will use the geometry elements[<sup>1</sup>](: http://desktop.arcgis.com/en/arcmap/10.3/analyze/arcpy-classes/geometry.htm) stored within each layer. It also must use the “in_memory” workspace[<sup>2</sup>](: http://desktop.arcgis.com/en/arcmap/10.3/analyze/modelbuilder/the-in-memory-workspace.htm) , so no additional data is saved and stored. 

## Concerns and Assumptions:
**Assumptions**

- The end user has a basic knowledge of the ESRI ArcMap Software
- That the map document will be created to allow for data to be updated automatically
- Developed for the license level of ArcView in ESRI ArcMap.
- All layers used are up to date and as accurate as can be. 
- All layers are loaded into the map, and can be accessed by the end user.
- Outputs can potentially rely on multiple layers. 
    - In some cases if an overlap is achieved it is not necessary to view the other layers.
- Tool only ‘looks’ at items in that have been marked in the ‘legal location’in the processing look up table.
- The BA has created a ‘Legal Location’ feature class that outlines what route card parameters need to be run.

**Concerns**
- If changes are to be made it may take significant time.
- Some of the script is hard coded and the values are not dynamic, meaning that if any values the script relies on change it may cause the tool to break.
- The tool may take a significant amount of time depending on the connections to the server and the user’s computer. 

## Planning Route Card Deliverables

A single script and ESRI ArcMap Map Document (MXD) that when used in conjunction with each other can create an output of an excel document that clearly outlines what spatial data is a concern to the Block in as well as a PDF of the overlapping data. The PDF mapping output is created so there is a ‘snapshot’ of what the data looked like at the time of the assessment.

## Tool Supporting Data

The tool currently relies on various components that must be set up ahead of time for it to work correctly. Those components are, (they also must be stored at the same relative path as stated below):
`<RouteCardToolPath>\MapDocumentExample.mxd`(can be located anywhere, as long as the toolbox is loaded to the map.)
`<RouteCardToolPath>\Supporting Data\SupportingData.gdb\LUT_Processing, \LUT_ScriptControls, \LegalAreas`
`<RouteCardToolPath>\Supporting Data\ShapeOfInterest.lyr`
`<RouteCardToolPath>\Supporting Data\SearchBuffer.lyr`
`<RouteCardToolPath>\Supporting Data\ProposedRoadEvents.lyr`
`<RouteCardToolPath>\RouteCardToolbox.tbx\Route Card Tool.py`
`<RouteCardToolPath>\PlanningRoute.py`

-----

### LegalAreas Polygons Feature Class

This feature class contains the spatial extent of the different FSP, LRMP and other regulatory controls that are mandated. Each area defined by a polygon would have different constraints from the other spatial areas in the featureclass. 

The following fields are included in the table:

#### PRC_Comments
This field is to record how the spatial extents have been created.
*Ie. Legal Area comprised of the following TSAs: Golden, Revelstoke,Cascadia*

#### LegalArea
Contains the field name that is added to the LUT_Processing table and defines what constraints it will be looking at as well as the order. This value MUST be added to the **LUT Processing table** and **MUST** be spelled the same.

-----

### LUT_Processing Table

This table is the processing driver for the tool. This is the location that all processes, items and layers to be used are defined.

The following fields are included in the table:

#### Item
Contains a text value of what is to be displayed in the output excel file. 

#### Processing
Contains a text value that defines what processing the layers that are associated with this item will go through.
Will contain the following values:

**title**: This value is used if the item is a title of a grouping of analysis  ie: LRMP Orders. This does not require any analysis but needs to be displayed in the output excel file.

**BEC**: Output value is dependent on what BEC Zone, Subzone, Variant and Phase the block overlaps with. This process MUST include values in the Query_Values field that define what BEC values are applicable.

**contains_overlap_layers (Polygon Layers Only)**: Output value is determined if any Polygons overlap with the Block of Interest. It will give either a `Y`/Applicable (If overlapping), `N`/Not Applicable(If not overlapping) or `X`/Within 100m (if there is no overlap but a polygon in the layer in question is within 100m of the Block of Interest).

**overlap_touching (Polygon Layers Only**): Output value is determined if any polygon is touching or overlapping the boundary of the Block of Interest. It will give either a `Y`/Applicable (If overlapping or touching), `N`/Not Applicable (If not overlapping or touching) or X/Within 100m (if there is no overlap but a polygon in the layer in question is within 100m of the Block of Interest).
	
**polygon_coverages ( Coverage Layers Only)**: A coverage layer does not have the same functionality that is being used in the contains_overlap_layers, this is a way of determining if there is overlaps with coverage files.

**point_line_layers (Point and Line Layers Only)**: This process determines if any lines or points are within the boundary of the Block of Interest.

**UngulateWinterRange**: Output value is dependent on what UWR_NUMBER the block overlaps with. This process MUST include values in the Query_Values field that define what UWR_NUMBER values are applicable.

**special_processing**: This process is items that cannot fit into the above sections and must be written to a separate script file, this area is hardcoded. (ex. Landscape Level Biodiversity: Max Cutblock Size)

**special_processing_no_layer**: This process is when items values are determined by other values, if Grizzly Bear habitat is `Y` then Grizzly Bear Range is `Y`, these items cannot fit into the above sections and must be written to a separate script file, this area is hardcoded.

**default_to_yes**: These items are automatically populated to a `Y` value. This is so the planners do not have to remember to add a `Y` value when finalizing the table.

#### Layer_List
Contains a text string that lists all applicable Layers the item relies on to determine if the item is applicable or not. The layers must be written as they are seen in the Table of Contents in the mxd and they must also be separated by a Semi Colon **with NO spaces in-between values**. If you would like attribute values to appear in the output you must put the layer then the fields you would like to report on. **There must be a COLON between Layers and Fields, and separate fields by a COMMA with NO spaces in-between values.**
    ie:`Layer1;Layer:FIELDNAME,FIELDNAME`

![layerList](./images/layerList.png?raw=true)
##### If there is sensitive data that CANNOT be shown on a map export, preface the layer name with ‘SensativeData_’ in the map table of contents as well as in the Layer List. This will ensure the data is turned off before exporting to PDF.

#### Query_Values
Contains a text string that lists all values that are needed to query the tabular data, used specifically in BEC analysis and  Ungulate Winter Range analysis. Individual **values MUST be separated by a comma with NO SPACES**.
In some cases BEC is only defined by the Zone or SubZone in those cases a `wildcard (*)` is used to state that any value occurring in the text before the `wildcard (*)` will be searched for. (ie: `IDFxh*` will look for `IDFxh1 and IDFxh2` etc.)

![layerList](./images/queryValues.png?raw=true)

#### Comments
Contains any comments the Planners or GIS persons would like to include with each process.

#### Legal Location ie. Okanagan or Columbia: 
Contains a numeric value that defines what order the items will be displayed in the final excel output. Items do not need to appear in order when adding new rows, as the tool reorders them into ascending order while running. 

-----

### LUT_ScriptControls Table

This table is used to control variables used within the script. It should only be edited once to step up each BA’s variables.
The following fields are included in the table:

#### Script_Variable 
Contains any variable calls that the script uses, this field is NOT TO BE EDITED. If changed in the slightest the tool will crash and not continue to work.
	
**OutputLocation**: The path to the output folder that all outputs will be saved to.

    ie: `<path-to-folder>\Planning Route Card\SpatialRouteCard`

**InputBlockFeatureClass**: The feature class that will be used to select blocks as it appears in the Table of Contents.
    ie: `Selectable Blocks`

**InputBlockField**: The field within the ‘InputBlockFeatureClass’ that is a unique is found in.
    ie: `CUTB_SEQ_NBR`

**InputBlockTitleFields**: List any fields that occur in the ‘InputBlockFeatureClass’ that will be used to name the output documents as well as a title in the map.
    ie: `LICENCE_ID,UBI`

**InputRoadFeatureClass**: The feature class that will be used to select roads as it appears in the Table of Contents.
    ie: `Selectable Road Events`

**InputRoadField**: The field within the ‘InputRoadFeatureClass’ that is a unique is found in.
    ie: `ROAD_SEQ_NBR`
	
**InputRoadTitleFields**: List any fields that occur in the ‘InputRoadFeatureClass’ that will be used to name the output documents as well as a title in the map.
    ie: `ROAD_ROAD_NAME,RSTA_START_METRE_NBR,RSTA_END_METRE_NBR`

**ExtentDistance**: The distance in meters that defines how far from the Block of Interest that the Processing Extent is set.
    ie: `200`

**DataframeScale**: Controls the output scale of the DataFrame.
    ie: `15000`

**SearchBufferDistance**: The Search Distance outside the block to look for items if they do not occur within the block.
    ie: `100`
	
#### Variable_Value
Contains the values that are to be used for each variable. This field can be edited to change where the output file location is, what the buffer search distance is etc.

#### Comments 
Contains any comments the GIS persons would like to include with each Variable.

## Running “CreateRouteCardbyUBI” tool
**Step 1: Open ArcMap**
1. Open ArcVIEW in the Citrix Application
2. Open the Route Card Map Document

**Step 2: Select your Road or Block**
1. Using the selection tool, select a single block or road that you would like to run through the tool.

**Step 3: Open the Tool**
1. Fill in the Parameters
    1. Type is Road or Block
    2. Your Name
2. Press start

**Step 4: Start Tool**
This should start working immediately. Should take approzimately 5 minutes to run, however may take longer depending on the size of the data it has to search and the connection to the servers.

**Step 5: Do additional Analysis on Output**
Once the Tool is complete all analysis outputs will be created in a predetermined area where all outputs are sent to. The planner must then use these values to do further analysis before signing off.

## Initial Set Up of the Tool within a new BA
The set up process may take a while but once done it does not need much work.

**Set Up LUT_ScriptControls**
1. Update the LUT_ScriptControl Table based on the values outlined in Section Tool Supporting Data and that are appropriate for your BA
    1. This should only need to be changed once when moved to a new user.

**Set Up LegalAreas Feature class**
1.	Add new shapes that determine the areas that have different constraint values, if your whole BA is constrained by the same items create one polygon.
2.	Fill in the `LegalArea` field with a name that is meaningful but follow the ArcGIS field naming guidelines  ex. in TOC we associated out “Legal_Locations” with what FSP they fall under ie. “Okanagan” or “Columbia”.

**Set up LUT_Processing**
1.	Add a field for each “Legal_Location” named in the LegalAreas FeatureClass ensure it is exactly the same.
2.	For each row populate the following fields
    1.	Item
    2.	Processing, 
        1.	Can only be one of the processes listed in “Tool Suppoting Data” section.
    3.	Layer_List
        1.	Ensure you follow the naming convention
        2.	Layers are split by semi colons
        3.	Any Field names you would like to report on are listed after the associated layer with a colon separating the field list and the layer name and commas between the fields. `ie: LayerName:FIELD1,FIELD2;LayerName2`
4.	Query_Field
    1.	For Ungulate Winter Ranges and BEC the Query_Field will need to be filled in with the associated field that the values listed in the Query_Values table would be found in.
5.	Query_Values
    1.	List all BEC units or TAG-ID’s that are associated with the item being searched. There must be no spaces and separated by a space. 
6.	Comments
7. `Legal_Location`
    1.	This is a numeric value that will order how your items appear in the final output. It does not have to be in order in the table the script will order it smallest to largest.

**Set up MXD Template**
1.	All layers listed in the Layer_List must be loaded into the mxd.
2.	Update the map layout
    1.	Do not change the legend, it is set to automatically populate based on the tool.
    2.	Add text elements for all fields that are in the “InputRoadTitleFields” and ‘InputBlockTitleFields’
        1.	Ensure that the element names are the same name as the fields in the above field.
        
        ![element](./images/elementName.png?raw=true)

        2.	If you would like any text to preface the information in the ‘Title Field’ Add it to the text of the element.
        3.	If Road and Block labels need to occur in the same location on the map, overlap the elements. The tool will turn them ‘on or off’ depending on if its “roads” or “blocks” being run.

## IMPORTANT ITEMS IN THE SCRIPT
Anything that is in sections `Special ProcessingNoLayer (~line 840)` OR `SpecialProcessing (~Line 720)` in the script is TOC specific. Please edit these values to suit your needs to delete them. DO NOT DELETE THE SECTIONS.

## License
    Copyright 2015-2016 Province of British Columbia

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at 

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
