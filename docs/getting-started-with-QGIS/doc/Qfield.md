# QFIELD application in QGIS


## Index
* [What is QFIELD](#What-is-QFIELD)
* [Basic steps from QGIS to QFIELD](#What-is-QFIELD)
* [QFIELD and Geodatpackages](#Quick-Mapservices-Plugin)
* [Qfield Best Practices](#Qfield-Best-Practices)
* [QField Sync Plugin](#QField-Sync-Plugin)
   * [Project Configuration](#Project-Configuration)
   * [Preferences](#Preferences)
   * [Package for QField](#Package-for-QField)
   * [Syncronize from QField](#Syncronize-from-QField)
* [Making a QGIS project for QField](#Making-a-QGIS-project-for-QField)

## What is QFIELD

QField is a mobile application built on QGIS open source software platform. The user makes a mapping project in QGIS then converts it to a QFIELD mobile project. The user can then assess or collect data in the field and then syncronize it back to the master QGIS data sources that the mapping project was created from. The Qfield interface is simple to use as most of the set up is completed in the QGIS project before exporting to a QField project.

Currently Qfield is only built for Android operating systems, though Apple IOS is currently in development.

## Qfield and GeodataPackages


## Basic steps from QGIS to QFIELD and Back
 For new users to QGIS or QField, the basic steps for using QField is as follows.
 1. Create a new QGIS project in a project folder
 2. Add features from data sources into QGIS and theme appropriately
 3. Load the Qsync plugin
 4. Run the Package for Qfield. Selecting how you want layers to be used as offline or editable. Export the package to a new folder
 5. Take the new package folder and move it to your mobile device
 6. Open Qfield on your tablet and open the .qgs file in the package folder
 7. Collect field work, copy Qfield package from feild device to computer

## Qfield Best Practices
QField is an effective mobile mapping solution, however there are some best practices to make the application work effectively and minimize .

1. Set your QGIS project to relative paths.
2. Use Geodatapackages. Other formats can be used, though reliability has not been tested
3. Projections: QGIS and QField can use different projection sources in the data, though if issues arise a common projection of data may be beneficial.


## QField Sync Plugin

### Configure Current Project (QField Sync Project Properties)
Allows the user to control how data will be used when packaged for QField
Choices include:
1. Lock Geometry for data copied to Qfield
2. Action: (Copy) data for use in QField
3. Action: (Offline Editing) Allow user to edit data in QField
4. Action: (Remove) Do not Package data for use in QField
5. Action: (Keep Existent) If data is already in a previous QField package then keep the existing data.
![QField Configure](../images/QField_Configure.jpg)
6. Base Map. An image basemap can be created from an image layer. **This may require the image to be in the same projection as the data or it may not work.
7. Offline editing. Only copy features in the Map Area of Interest Window.

### Preferences
Where you can set your default import and export directories

### Package For QField

1. Select export directory
2. Select Extent by zooming in view window the area of data you would like to export to QField.
![QField Configure](../images/QField_Package.jpg)

### Syncronize from QField
1. Open the Original QGIS project then select folder where import data from the field was placed. 
2. Then Syncronize and original QGIS data will be updated with data from field.
![QField Syncronize](../images/QField_Syncronize.jpg)


# Making a QGIS project for QField

### License
    Copyright 2019 BC Provincial Government

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
