# PyQt Apps

[Home](../README.md)

## Index

* [Accessing Python 3 in the GTS](#accessing-python-3-in-the-gts)
* [Setting up the GUI](#setting-up-the-gui)
* [Adding User Inputs](#adding-user-inputs)
* [Adding Buttons](#adding-buttons)
* [Adding Functions](#adding-functions)
* [PIP3, QGIS, and the BCGW](#pip3-qgis-and-the-BCGW)

## Accessing Python 3 in the GTS

*NOTE: In order to get the scripts to work on GTS 10.6 and 10.8 you will need to run through a batch script.*

QGIS uses Python 3 - a newer version of Python than ArcGIS Desktop - and this is not the default Python language used on the GTS. 
To use Python 3 in the 10.6 and 10.8 servers you will need to run your code through a batch script.
The batch script is very basic as shown below: 

```bat
if exist E:\sw_nt\QGIS_3.10\ (
  setlocal
  set PYTHONPATH=E:\sw_nt\QGIS_3.10\apps\Python37;E:\sw_nt\QGIS_3.10\apps\qgis-ltr\python
  set PATH=E:\sw_nt\QGIS_3.10\bin;E:\sw_nt\QGIS_3.10\apps\qgis-ltr\bin;E:\sw_nt\QGIS_3.10\apps\Qt5\bin;
  set QT_QPA_PLATFORM_PLUGIN_PATH=E:\sw_nt\QGIS_3.10\apps\Qt5\plugins
  E:\sw_nt\QGIS_3.10\apps\Python37\python \path\to\yourScript.py
) else (
  setlocal
  set PYTHONPATH=E:\sw_nt\QGIS_3.16\apps\Python37;E:\sw_nt\QGIS_3.16\apps\qgis-ltr\python
  set PATH=E:\sw_nt\QGIS_3.16\bin;E:\sw_nt\QGIS_3.16\apps\qgis-ltr\bin;E:\sw_nt\QGIS_3.16\apps\Qt5\bin;
  set QT_QPA_PLATFORM_PLUGIN_PATH=E:\sw_nt\QGIS_3.16\apps\Qt5\plugins
  E:\sw_nt\QGIS_3.16\apps\Python37\python \path\to\yourScript.py
)
```

Copy the above code into a text editor and save it as runProgram.bat

A brief explanation of this code is warranted here. The batch script simply tells your PC where to look for several programs needed to run
Python 3 scripts on a PC setup to use Python 2 by default. It also tells the PC to check if QGIS is installed in one of two possible folders. 
Using a batch script to run your Python code ensures that the code will work the same way regardless of which GTS server it is run on and is 
good practice.

Of course, replace \path\to\yourScript.py with the path to your script that you will create below.

*Having an issue with this code or have a suggestion on how to make it better? Submit an [issue report](https://github.com/bcgov/gis-pantry/issues/new) and be sure to tag @jdavid05*

## Setting up the GUI

One of the wonderful things about making standalone scripts with PyQt and QGIS - as opposed to ArcGIS standalone scripts - is that PyQt 
has a beautiful system for making user friendly GUIs. These can range from very simple to extremely complex. To start, we're going to make 
a basic GUI that simply opens a window on our screens.

Use the code below to open a simple GUI window:

```python
# -*- coding: cp1252 -*-
# Python modules
import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel, QFileDialog, QDialog, QTableView, QCheckBox
from PyQt5.QtGui import QIcon, QColor, QFont
from PyQt5.QtCore import *
from PyQt5.QtXml import *

# The server sometimes installs QGIS in folder QGIS_3.10 and other times in
#  QGIS_3.16 so a check must be done.
path = Path('E:\\sw_nt\\QGIS_3.10')
if path.exists():
    sys.path.append('E:\\sw_nt\\QGIS_3.10\\apps\\qgis-ltr\\python\\plugins')
else:
    sys.path.append('E:\\sw_nt\\QGIS_3.16\\apps\\qgis-ltr\\python\\plugins')
    
# initialize application class for oop
class App(QMainWindow):
    # Constructor with window object dimensions
    def __init__(self):
        super().__init__()
        self.title = 'Test Window'
        self.left = 100
        self.top = 100
        self.width = 400
        self.height = 340
        self.initUI()
    # Constructor with object GUI
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        # Run the code when the Run button is clicked
        #  Add all modules here in same structure
        self.show()

if __name__ == '__main__':
    # You need one (and only one) QApplication instance per application.
    # Pass in sys.argv to allow command line arguments for your app.
    # If you know you won't use command line arguments QApplication([]) works too.
    app = QApplication(sys.argv)
    ex = App()
    # Start the event loop.
    app.exec()
    # Your application won't reach here until you exit and the event
    # loop has stopped.

```

Save the file as test.py in the same folder as runProgram.bat. 
Now, update runProgram.bat so the line \path\to\yourScript.py is the path to test.py (ex\ \\spatialfiles2.bcgov\work\test.py).
When you double click runProgram.bat you should now see the command line open and an empty window should pop up.

*Having an issue with this code or have a suggestion on how to make it better? Submit an [issue report](https://github.com/bcgov/gis-pantry/issues/new) and be sure to tag @jdavid05*

## Adding User Inputs

The above script simply creates a blank window that doesn't do anything. But what if we want to add spaces for the user to actually interact 
with the system?

The first step in this process is to add some dialogue boxes where the user can enter data.

There are several types of dialogue boxes you can add with PyQt but the most common would of course be the textbox. 
In this case, we're going to make a simple application that creates a report of tenures impacted by the fire selected by the user so we will have 4 textboxes:

1. An input for the fire number
2. An input for the directory where the report will be saved
3. An input to hold the username
4. An input to hold the password

A basic text input can be added using the following code which can be slotted in the initUI function above the self.show() line:

```python
self.txt_fireNumber = QLineEdit(self) #add the textbox
self.txt_fireNumber.move(120, 20) #move the textbox to a useful position
self.txt_fireNumber.resize(200, 32) #resize the textbox to fit the window
```

Of course, you will want to prompt the user for an input so they know what each textbox holds so the above code should be edited to look like this:

```python
# Create textbox for Fire Number variable
# Type = text
self.lbl_fireNumber = QLabel(self)
self.lbl_fireNumber.setText('Fire Number:')
self.txt_fireNumber = QLineEdit(self)

# Move + Resize textbox for Fire Number
self.txt_fireNumber.move(120, 20)
self.txt_fireNumber.resize(200, 32)
self.lbl_fireNumber.move(20, 20)
```

To add all four textboxes, we will need to our initUI function to this:

```python
def initUI(self):
    self.setWindowTitle(self.title)
    self.setGeometry(self.left, self.top, self.width, self.height)

    # Create textbox for Fire Number variable
    # Type = text
    self.lbl_fireNumber = QLabel(self)
    self.lbl_fireNumber.setText('Fire Number:')
    self.txt_fireNumber = QLineEdit(self)

    # Move + Resize textbox for Fire Number
    self.txt_fireNumber.move(120, 20)
    self.txt_fireNumber.resize(200, 32)
    self.lbl_fireNumber.move(20, 20)

    # Create textbox for Output Folder path variable
    # Type = text
    self.lbl_outFolder = QLabel(self)
    self.lbl_outFolder.setText('Output Folder:')
    self.txt_outFolder = QLineEdit(self)

    # Move + Resize textbox for Output folder
    self.txt_outFolder.move(120, 70)
    self.txt_outFolder.resize(200, 32)
    self.lbl_outFolder.move(20, 70)

    # Create textbox for user name
    # Type = text
    self.lbl_userName = QLabel(self)
    self.lbl_userName.setText('User Name:')
    self.txt_userName = QLineEdit(self)

    # Move + Resize textbox for user name
    self.txt_userName.move(120, 120)
    self.txt_userName.resize(200, 32)
    self.lbl_userName.move(20, 120)

    # Create textbox for password
    # Type = hidden text
    self.lbl_password = QLabel(self)
    self.lbl_password.setText('Password (BCGW):')
    self.txt_password = QLineEdit(self)
    self.txt_password.setEchoMode(QLineEdit.Password)

    # Move + Resize textbox for user name
    self.txt_password.move(120, 170)
    self.txt_password.resize(200, 32)
    self.lbl_password.move(20, 170)
    
    # Run the code when the Run button is clicked
    #  Add all modules here in same structure
    self.show()
```

Go ahead and re-run the batch script now to launch the new window. You should see four new textboxes where you can enter data.

*Having an issue with this code or have a suggestion on how to make it better? Submit an [issue report](https://github.com/bcgov/gis-pantry/issues/new) and be sure to tag @jdavid05*

## Adding Buttons

Now that we have some user inputs we will need to create a way to have them do something. For that to happen, we'll want to add some buttons.
For this script, we probably want two buttons.

1. A button to run some code
2. A button where the user can select the output folder so they don't have to type or copy it in.

Buttons are added using this code:

```python
# Add button to run code
# When the RUN button is clicked it will run all modules
self.btn_run = QPushButton('Run', self)
self.btn_run.move(20,240)
```

In the above code we create a button named btn_run with the text Run printed inside of it and move it to the bottom of the window. 
This code should go below the password input added above and above the self.show() line.

We'll also need to add a button to select the output directory. We can do that with the following code:

```python
# Create button for opening a directory dialog used to
#  select a directory to save outputs in using file manager
self.btn_selectFolder = QPushButton("", self)
#self.btn_selectFolder.setIcon(QIcon(("\\\\spatialfiles2.bcgov\\path\\to\\folderIcon.png")))
self.btn_selectFolder.move(340,70)
self.btn_selectFolder.resize(50,32)
```

If you want to add an icon to the select folder button, uncomment the self.btn_selectFolder.setIcon line and replace the path with the path to your folder icon. 
Remeber to use double '\'s to escape the string in the file path. 

You can paste this code above the run button code.

If you run the batch script now you should see the buttons have been added to the window.

*Having an issue with this code or have a suggestion on how to make it better? Submit an [issue report](https://github.com/bcgov/gis-pantry/issues/new) and be sure to tag @jdavid05*


## Adding Functions

Even if you're familiar with Python, you probably aren't familiar with some of the code above. 
Luckily, other than the button press events, functions in PyQt are just like regular functions.

Right now we have two functions:

1. __init__ which is loaded when the script runs
2. initUI which is also loaded at startup

Here we'll add a third function that will allow the user to select a folder and store it as a variable. 
We'll call the function getFolder and the output outFolder.

```python
@pyqtSlot()
def getFolder(self):
    self.outFolder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
    self.txt_outFolder.setText(self.outFolder)
```

This function is pretty simple. The first line that says @pyqtSlot() is simply a line that informs Python that it will be calling C++.
It is not neccesary for the code to run but could make it run faster. 
After that, the line for setting the outFolder variable is just a basic PyQt command while last line just sets the text in the dialogue box.

You can slot this function below the initUI function.

To call this function we'll need to update our initUI function to add the line:

```python
self.btn.clicked.connect(self.getFolder)
```

You can add this just above the self.show() line at the bottom of the initUI function

Let's run the batch script again and check out our new funciton. You should now be able to click the button beside the Output Folder box 
and select a folder to populate the box.

This is a really simple function but, of course, the function to create the report will be much more complex.

Having an issue with this code or have a suggestion on how to make it better? Submit an [issue report](https://github.com/bcgov/gis-pantry/issues/new) and be sure to tag @jdavid05


## PIP3, QGIS, and the BCGW

To make an Excel report we'll need to have the xlsxwriter module installed in Python 3. Unfortunately, it isn't by default. 
To remedy this, we'll have to add some code to our imports at the top of the script that checks if xlsxwriter is installed and, if not, installs it.

Update your imports to match the code below:

```python
# -*- coding: cp1252 -*-
# Python modules
import sys
import subprocess
import time
import datetime
import os
import csv
import re
try:
    import xlsxwriter
    print("module 'xlsxwriter' is already installed")
except ModuleNotFoundError:
    print("module 'xlsxwriter' is not installed")
    # or
    subprocess.check_call([sys.executable, "-m", "pip", "install", "XlsxWriter"])
    import xlsxwriter
from pathlib import Path
from qgis.core import *
from qgis.gui import QgsMapCanvas, QgsVertexMarker, QgsMapCanvasItem, QgsRubberBand, QgsLayerTreeMapCanvasBridge
from qgis.utils import iface
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel, QFileDialog, QDialog, QTableView, QCheckBox
from PyQt5.QtGui import QIcon, QColor, QFont
from PyQt5.QtCore import *
from qgis.PyQt.QtXml import QDomDocument
from PyQt5.QtXml import *

# The server sometimes installs QGIS in folder QGIS_3.10 and other times in
#  QGIS_3.16 so a check must be done.
path = Path('E:\\sw_nt\\QGIS_3.10')
if path.exists():
    sys.path.append('E:\\sw_nt\\QGIS_3.10\\apps\\qgis-ltr\\python\\plugins')
else:
    sys.path.append('E:\\sw_nt\\QGIS_3.16\\apps\\qgis-ltr\\python\\plugins')
```

I've added some other imports here too that will be used in the fuctions we will use to create the reports.

Similarly, you'll need to update the code in the if __name__ == '__main__': statement to:

```python
if __name__ == '__main__':
    # You need one (and only one) QApplication instance per application.
    # Pass in sys.argv to allow command line arguments for your app.
    # If you know you won't use command line arguments QApplication([]) works too.
    app = QApplication(sys.argv)
    # Gotta set some paths here. Bad python 3 install on this server
    if path.exists():
        QgsApplication.setPrefixPath("E:\\sw_nt\\QGIS_3.10\\apps\\qgis-ltr", True)
        os.environ['QGIS_PREFIX_PATH'] = 'E:\\sw_nt\\QGIS_3.10\\apps\\qgis-ltr'
    else:
        QgsApplication.setPrefixPath("E:\\sw_nt\\QGIS_3.16\\apps\\qgis-ltr", True)
        os.environ['QGIS_PREFIX_PATH'] = 'E:\\sw_nt\\QGIS_3.16\\apps\\qgis-ltr'
    # A lot of this stuff looks like it could be moved to the top of this
    # script. It can't be.
    # !DO NOT CLEAN THIS CODE OR MOVE MODULE IMPORTS OR SCRIPT WILL BREAK!
    qgs = QgsApplication([], False)
    qgs.initQgis()
    import processing
    from processing.core.Processing import Processing
    Processing.initialize()
    from qgis.analysis import QgsNativeAlgorithms
    QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
    ex = App()
    # Start the event loop.
    app.exec()
    # Your application won't reach here until you exit and the event
    # loop has stopped.
    qgs.exitQgis()
```

This just adds some other imports that need to be in this section of the code. 
If you move the procesing import, for example, to the top the code will not run.

Now we can get into the fun stuff: Adding the functions to import data from the BCGW. 
If you're used to ArcGIS scripting, you're going to realize that QGIS is a little cumbersome in its Oracle imports.

Let's add the code to import the fire data layer from Oracle under the getFolder() function:

```python
#####################################################################
# function: loadFire                                                #
# inputs:  self.user (username for BCGW),                           #
#           self.pWord (password for BCGW)                          #
# outputs:  LYR2 (Fire Layer - Queried)                             #
#####################################################################
def loadFire(self):  
    # similar to loadTenures function but sets SQL Query before
    #  loading data
    uri = QgsDataSourceUri()
    uri.setConnection('bcgw.bcgov', '1521', 'idwprod1.bcgov', self.user, self.pWord)
    connInfo = uri.connectionInfo()
    uri.setPassword(self.pWord)
    uri.setUsername(self.user)
    uri.setDataSource("WHSE_LAND_AND_NATURAL_RESOURCE", "PROT_CURRENT_FIRE_POLYS_SP", "SHAPE")
    uri.setWkbType(QgsWkbTypes.Polygon)
    uri.setSrid('3005')
    uri.setKeyColumn('OBJECTID')
    uri.setUseEstimatedMetadata(True)
    # Query to only extract the selected fire (provided in fire number
    #  textbox by user input
    uri.setSql("FIRE_NUMBER LIKE '" + self.txt_fireNumber.text() + "'")
    self.LYR2 = QgsVectorLayer(uri.uri(), "LYR2", "oracle")
    QgsProject.instance().addMapLayer(self.LYR2)
```

As you can see, it's a lot of code to load the Oracle layer. If you want more information on uri settings I suggest you visit [this site](https://qgis.org/pyqgis/3.0/core/Data/QgsDataSourceUri.html#qgis.core.QgsDataSourceUri.setWkbType).

You'll need to add two more functions that load tenures layers:

```python
#####################################################################
# function: loadTenures                                             #
# inputs:                                                           #
# outputs: self.user (username for BCGW),                           #
#           self.pWord (password for BCGW), LYR (Tenures Layer)     #
#####################################################################
def loadTenures(self):
    # load crown tenures layer from the BCGW
    # Loading data from Oracle requires setting the username,
    #  password, data source, WKB type, Srid, Primary Key, and
    #  metadata estimation (default is false)
    self.user = self.txt_userName.text()
    self.pWord = self.txt_password.text()
    uri = QgsDataSourceUri()
    uri.setConnection('bcgw.bcgov', '1521', 'idwprod1.bcgov', self.user, self.pWord)
    connInfo = uri.connectionInfo()
    uri.setPassword(self.pWord)
    uri.setUsername(self.user)
    uri.setDataSource("WHSE_TANTALIS", "TA_CROWN_TENURES_SVW", "SHAPE")
    uri.setWkbType(QgsWkbTypes.Polygon)
    uri.setSrid('3005')
    uri.setKeyColumn('OBJECTID')
    uri.setUseEstimatedMetadata(True)
    self.LYR = QgsVectorLayer(uri.uri(), "LYR", "oracle")
    QgsProject.instance().addMapLayer(self.LYR)
		
#####################################################################
# function: loadTenureHolder                                        #
# inputs:  self.user (username for BCGW),                           #
#           self.pWord (password for BCGW)                          #
# outputs:  LYR3 (Interest Holder)                                  #
#####################################################################
def loadTenureHolder(self):  
    # load the Tenure holder non-spatial table
    uri = QgsDataSourceUri()
    uri.setConnection('bcgw.bcgov', '1521', 'idwprod1.bcgov', self.user, self.pWord)
    connInfo = uri.connectionInfo()
    uri.setPassword(self.pWord)
    uri.setUsername(self.user)
    uri.setDataSource("WHSE_TANTALIS", "TA_INTEREST_HOLDER_VW", None)
    #uri.setWkbType(QgsWkbTypes.Polygon)
    #uri.setSrid('3005')
    uri.setKeyColumn('ROW_UNIQUEID')
    uri.setUseEstimatedMetadata(True)
    self.LYR3 = QgsVectorLayer(uri.uri(), "LYR3", "oracle")
    QgsProject.instance().addMapLayer(self.LYR3)
```

We'll also have to add some functions to run some analysis. Firstly, we'll need to clip the tenures layer to the fire:

```python
#####################################################################
# function: runClip                                                 #
# inputs:  self.user, self.pWord, LYR, LYR2                         #
# outputs:  clipped polygon of tenures inside of fire as shape      #
#####################################################################
def runClip(self):
    # set input and output file names
    firePath = self.LYR2
    tenurePath = self.LYR
    clipPath = "memory:"
    # run the clip
    clipFile = processing.run("native:clip", {'INPUT':tenurePath, 'OVERLAY':firePath, 'OUTPUT':clipPath})
    layer = QgsProject.instance().addMapLayer(clipFile['OUTPUT'])
    # Can't export binary fields - delete them
    res = layer.dataProvider().deleteAttributes([22])
    # Calculate the ha of tenures found in the fire
    layer.dataProvider().addAttributes([QgsField("hafire", QVariant.Double)])
    layer.updateFields()
    # The context variable is just an expression
    # $area simply calculates the area of the features in a layer
    #  in the projected coordinate unit (metres in 3005)
    context = QgsExpressionContext()
    context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))
    expression1 = QgsExpression('$area')
    with edit(layer):
        for f in layer.getFeatures():
            context.setFeature(f)
            f['hafire'] = expression1.evaluate(context)
            layer.updateFeature(f)
    #testing
    shpField='INTRID_SID'
    csvField='INTERESTED_PARTY_SID'
    result = processing.run('native:joinattributestable', {'INPUT':layer, 'INPUT_2':self.LYR3, 'FIELD':shpField, 'FIELD_2':csvField, 'OUTPUT':clipPath})
    layer = QgsProject.instance().addMapLayer(result['OUTPUT'])
    layer.dataProvider().addAttributes([QgsField("holder", QVariant.String, 'text', 254)])
    layer.updateFields()
    # Get the Tenure holders into a single text field
    context = QgsExpressionContext()
    context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))
    expression1 = QgsExpression('if( "ORGANIZATIONS_LEGAL_NAME" IS NOT NULL,  "ORGANIZATIONS_LEGAL_NAME",  "INDIVIDUALS_FIRST_NAME" +  \' \'  + "INDIVIDUALS_LAST_NAME")')
    with edit(layer):
        for f in layer.getFeatures():
            context.setFeature(f)
            f['holder'] = expression1.evaluate(context)
            layer.updateFeature(f)
    #end testing
    crs=QgsCoordinateReferenceSystem("epsg:3005")
    # Check if the path the user selected exists or make it
    Path(os.path.join(self.txt_outFolder.text(), "shapes")).mkdir(parents=True, exist_ok=True)
    # Export clipped tenures as a shape
    save_options = QgsVectorFileWriter.SaveVectorOptions()
    save_options.driverName = "ESRI Shapefile"
    save_options.fileEncoding = "UTF-8"
    transform_context = QgsProject.instance().transformContext()
    QgsVectorFileWriter.writeAsVectorFormatV2(layer,
                                              os.path.join(self.txt_outFolder.text(), "shapes", self.txt_fireNumber.text() + "_clipped"),
                                              transform_context,
                                              save_options) 
    self.clipLayer = QgsVectorLayer(os.path.join(self.txt_outFolder.text(), "shapes", self.txt_fireNumber.text() + "_clipped.shp"), "layer_shp", "ogr")
```

With the function that clips the tenures to the fire added we can now add the function to create the report:

```python
#####################################################################
# function: updateWorksheet                                         #
# inputs:  self.user, self.pWord                                    #
# outputs:  excel report                                            #
#####################################################################     
def updateWorksheet(self):
    self.clipLayer = QgsVectorLayer(os.path.join(self.txt_outFolder.text(), "shapes", self.txt_fireNumber.text() + "_clipped.shp"), "layer_shp", "ogr")
    # update the status text
    # Lets create a report for tenures inside the fire
    workbook = xlsxwriter.Workbook(os.path.join(self.txt_outFolder.text(), self.txt_fireNumber.text() + '.xlsx'))
    worksheet = workbook.add_worksheet()
    # Format the title row to make it pretty
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'text_wrap': 'vjustify'})
    worksheet.merge_range('A1:A3', 'Crown Lands File Number ', merge_format)
    worksheet.merge_range('B1:B3', 'Tenure Holder Name', merge_format)
    worksheet.merge_range('C1:C3', 'Tenure Type', merge_format)
    worksheet.merge_range('D1:D3', 'Tenure Subtype', merge_format)
    worksheet.merge_range('E1:E3', 'Tenure Purpose', merge_format)
    worksheet.merge_range('F1:F3', 'Tenure Subpurpose', merge_format)
    worksheet.merge_range('G1:G3', 'Tenure Total Area (ha)', merge_format)
    worksheet.merge_range('H1:H3', 'Tenure Area within 2021 Fire Perimeter (ha)', merge_format)
    worksheet.merge_range('I1:I3', '% of Tenure Within Fire Perimeter', merge_format)
    worksheet.set_column(0,1,15)
    worksheet.set_column(1,1,15)
    worksheet.set_column(2,1,15)
    worksheet.set_column(3,1,15)
    worksheet.set_column(4,1,15)
    worksheet.set_column(5,1,15)
    worksheet.set_column(6,1,15)
    worksheet.set_column(7,1,15)
    worksheet.set_column(8,1,15)
    clipAtt = self.clipLayer.getFeatures()
    # xi is just a number for adding the clipped tenures
    #  data to the Excel sheet. Start at four based on
    #  formatting
    xi = 4
    ha_format = workbook.add_format({'num_format': '###,###,###,##0.00'})
    for att in clipAtt:
        attrs = att.attributes()
        # variable 'attrs' is a qvariant and thus is a
        #  C++ attribute. Must perform NULL check or will
        #  fail. Check is if then variable name (if attrs[#])
        if attrs[7]:
            print(attrs[7])
            worksheet.write('A' + str(xi), attrs[7])
        if attrs[33]:
            print(attrs[33])
            worksheet.write('B' + str(xi), attrs[33])
        if attrs[3]:
            print(attrs[3])
            worksheet.write('C' + str(xi), attrs[3])
        if attrs[4]:
            print(attrs[4])
            worksheet.write('D' + str(xi), attrs[4])
        if attrs[5]:
            print(attrs[5])
            worksheet.write('E' + str(xi), attrs[5])
        if attrs[6]:
            print(attrs[6])
            worksheet.write('F' + str(xi), attrs[6])
        if attrs[19]:
            print(attrs[19]/10000)
            worksheet.write('G' + str(xi), attrs[19]/10000, ha_format)
        if attrs[5]:
            print(attrs[5])
            worksheet.write('H' + str(xi), attrs[22]/10000, ha_format)
            print(attrs[5])
            worksheet.write('I' + str(xi), attrs[22]/attrs[19]*100, ha_format)
        # increment xi
        xi = xi + 1
    # Close the workbook - no need to save
    workbook.close()
```

To make these functions run when we click the Run button we can just call them in the initUI() function in the order we want them to run. 
Update the initUI function to:

```python
def initUI(self):
    self.setWindowTitle(self.title)
    self.setGeometry(self.left, self.top, self.width, self.height)

    # Create textbox for Fire Number variable
    # Type = text
    self.lbl_fireNumber = QLabel(self)
    self.lbl_fireNumber.setText('Fire Number:')
    self.txt_fireNumber = QLineEdit(self)

    # Move + Resize textbox for Fire Number
    self.txt_fireNumber.move(120, 20)
    self.txt_fireNumber.resize(200, 32)
    self.lbl_fireNumber.move(20, 20)

    # Create textbox for Output Folder path variable
    # Type = text
    self.lbl_outFolder = QLabel(self)
    self.lbl_outFolder.setText('Output Folder:')
    self.txt_outFolder = QLineEdit(self)

    # Move + Resize textbox for Output folder
    self.txt_outFolder.move(120, 70)
    self.txt_outFolder.resize(200, 32)
    self.lbl_outFolder.move(20, 70)

    # Create textbox for user name
    # Type = text
    self.lbl_userName = QLabel(self)
    self.lbl_userName.setText('User Name:')
    self.txt_userName = QLineEdit(self)

    # Move + Resize textbox for user name
    self.txt_userName.move(120, 120)
    self.txt_userName.resize(200, 32)
    self.lbl_userName.move(20, 120)

    # Create textbox for password
    # Type = hidden text
    self.lbl_password = QLabel(self)
    self.lbl_password.setText('Password (BCGW):')
    self.txt_password = QLineEdit(self)
    self.txt_password.setEchoMode(QLineEdit.Password)

    # Move + Resize textbox for user name
    self.txt_password.move(120, 170)
    self.txt_password.resize(200, 32)
    self.lbl_password.move(20, 170)

    # Create button for opening a directory dialog used to
    #  select a directory to save outputs in using file manager
    self.btn = QPushButton("", self)
    #self.btn.setIcon(QIcon(("\\\\spatialfiles2.bcgov\\WORK\\FOR\\RSI\\DMH\\General_User_Data\\DavidsonJoe\\TEMPLATES\\PYTHON\\FlatFolderIcon.png")))
    self.btn.move(340,70)
    self.btn.resize(50,32)

    # Add button to run code
    # When the RUN button is clicked it will run all modules
    self.button = QPushButton('Run', self)
    self.button.move(20,240)

    # Run the getFolder function when folder button is clicked
    self.btn.clicked.connect(self.getFolder)

    # Run the code when the Run button is clicked
    #  Add all modules here in same structure
    self.button.clicked.connect(self.loadTenures)
    self.button.clicked.connect(self.loadFire)
    self.button.clicked.connect(self.loadTenureHolder)
    self.button.clicked.connect(self.runClip)
    self.button.clicked.connect(self.updateWorksheet)
    
    # Run the code when the Run button is clicked
    #  Add all modules here in same structure
    self.show()
```

The final python script in its entirety should be as follows:

```python
# -*- coding: cp1252 -*-
# Python modules
import sys
import subprocess
import time
import datetime
import os
import csv
import re
try:
    import xlsxwriter
    print("module 'xlsxwriter' is already installed")
except ModuleNotFoundError:
    print("module 'xlsxwriter' is not installed")
    # or
    subprocess.check_call([sys.executable, "-m", "pip", "install", "XlsxWriter"])
    import xlsxwriter
from pathlib import Path
from qgis.core import *
from qgis.gui import QgsMapCanvas, QgsVertexMarker, QgsMapCanvasItem, QgsRubberBand, QgsLayerTreeMapCanvasBridge
from qgis.utils import iface
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel, QFileDialog, QDialog, QTableView, QCheckBox
from PyQt5.QtGui import QIcon, QColor, QFont
from PyQt5.QtCore import *
from qgis.PyQt.QtXml import QDomDocument
from PyQt5.QtXml import *
# The server sometimes installs QGIS in folder QGIS_3.10 and other times in
#  QGIS_3.16 so a check must be done.
path = Path('E:\\sw_nt\\QGIS_3.10')
if path.exists():
    sys.path.append('E:\\sw_nt\\QGIS_3.10\\apps\\qgis-ltr\\python\\plugins')
else:
    sys.path.append('E:\\sw_nt\\QGIS_3.16\\apps\\qgis-ltr\\python\\plugins')
    
# initialize application class for oop
class App(QMainWindow):
    # Constructor with window object dimensions
    def __init__(self):
        super().__init__()
        self.title = 'Test Window'
        self.left = 100
        self.top = 100
        self.width = 400
        self.height = 340
        self.initUI()
    # Constructor with object GUI
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create textbox for Fire Number variable
        # Type = text
        self.lbl_fireNumber = QLabel(self)
        self.lbl_fireNumber.setText('Fire Number:')
        self.txt_fireNumber = QLineEdit(self)

        # Move + Resize textbox for Fire Number
        self.txt_fireNumber.move(120, 20)
        self.txt_fireNumber.resize(200, 32)
        self.lbl_fireNumber.move(20, 20)

        # Create textbox for Output Folder path variable
        # Type = text
        self.lbl_outFolder = QLabel(self)
        self.lbl_outFolder.setText('Output Folder:')
        self.txt_outFolder = QLineEdit(self)

        # Move + Resize textbox for Output folder
        self.txt_outFolder.move(120, 70)
        self.txt_outFolder.resize(200, 32)
        self.lbl_outFolder.move(20, 70)

        # Create textbox for user name
        # Type = text
        self.lbl_userName = QLabel(self)
        self.lbl_userName.setText('User Name:')
        self.txt_userName = QLineEdit(self)

        # Move + Resize textbox for user name
        self.txt_userName.move(120, 120)
        self.txt_userName.resize(200, 32)
        self.lbl_userName.move(20, 120)

        # Create textbox for password
        # Type = hidden text
        self.lbl_password = QLabel(self)
        self.lbl_password.setText('Password (BCGW):')
        self.txt_password = QLineEdit(self)
        self.txt_password.setEchoMode(QLineEdit.Password)

        # Move + Resize textbox for user name
        self.txt_password.move(120, 170)
        self.txt_password.resize(200, 32)
        self.lbl_password.move(20, 170)

        # Create button for opening a directory dialog used to
        #  select a directory to save outputs in using file manager
        self.btn = QPushButton("", self)
        #self.btn.setIcon(QIcon(("\\\\spatialfiles2.bcgov\\WORK\\FOR\\RSI\\DMH\\General_User_Data\\DavidsonJoe\\TEMPLATES\\PYTHON\\FlatFolderIcon.png")))
        self.btn.move(340,70)
        self.btn.resize(50,32)

        # Add button to run code
        # When the RUN button is clicked it will run all modules
        self.button = QPushButton('Run', self)
        self.button.move(20,240)

        # Run the getFolder function when folder button is clicked
        self.btn.clicked.connect(self.getFolder)

        # Run the code when the Run button is clicked
        #  Add all modules here in same structure
        self.button.clicked.connect(self.loadTenures)
        self.button.clicked.connect(self.loadFire)
        self.button.clicked.connect(self.loadTenureHolder)
        self.button.clicked.connect(self.runClip)
        self.button.clicked.connect(self.updateWorksheet)
        
        # Run the code when the Run button is clicked
        #  Add all modules here in same structure
        self.show()

    @pyqtSlot()
    def getFolder(self):
        self.outFolder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.txt_outFolder.setText(self.outFolder)

    #####################################################################
    # function: loadFire                                                #
    # inputs:  self.user (username for BCGW),                           #
    #           self.pWord (password for BCGW)                          #
    # outputs:  LYR2 (Fire Layer - Queried)                             #
    #####################################################################
    def loadFire(self):  
        # similar to loadTenures function but sets SQL Query before
        #  loading data
        uri = QgsDataSourceUri()
        uri.setConnection('bcgw.bcgov', '1521', 'idwprod1.bcgov', self.user, self.pWord)
        connInfo = uri.connectionInfo()
        uri.setPassword(self.pWord)
        uri.setUsername(self.user)
        uri.setDataSource("WHSE_LAND_AND_NATURAL_RESOURCE", "PROT_CURRENT_FIRE_POLYS_SP", "SHAPE")
        uri.setWkbType(QgsWkbTypes.Polygon)
        uri.setSrid('3005')
        uri.setKeyColumn('OBJECTID')
        uri.setUseEstimatedMetadata(True)
        # Query to only extract the selected fire (provided in fire number
        #  textbox by user input
        uri.setSql("FIRE_NUMBER LIKE '" + self.txt_fireNumber.text() + "'")
        self.LYR2 = QgsVectorLayer(uri.uri(), "LYR2", "oracle")
        QgsProject.instance().addMapLayer(self.LYR2)

    #####################################################################
    # function: loadTenures                                             #
    # inputs:                                                           #
    # outputs: self.user (username for BCGW),                           #
    #           self.pWord (password for BCGW), LYR (Tenures Layer)     #
    #####################################################################
    def loadTenures(self):
        # load crown tenures layer from the BCGW
        # Loading data from Oracle requires setting the username,
        #  password, data source, WKB type, Srid, Primary Key, and
        #  metadata estimation (default is false)
        self.user = self.txt_userName.text()
        self.pWord = self.txt_password.text()
        uri = QgsDataSourceUri()
        uri.setConnection('bcgw.bcgov', '1521', 'idwprod1.bcgov', self.user, self.pWord)
        connInfo = uri.connectionInfo()
        uri.setPassword(self.pWord)
        uri.setUsername(self.user)
        uri.setDataSource("WHSE_TANTALIS", "TA_CROWN_TENURES_SVW", "SHAPE")
        uri.setWkbType(QgsWkbTypes.Polygon)
        uri.setSrid('3005')
        uri.setKeyColumn('OBJECTID')
        uri.setUseEstimatedMetadata(True)
        self.LYR = QgsVectorLayer(uri.uri(), "LYR", "oracle")
        QgsProject.instance().addMapLayer(self.LYR)
                    
    #####################################################################
    # function: loadTenureHolder                                        #
    # inputs:  self.user (username for BCGW),                           #
    #           self.pWord (password for BCGW)                          #
    # outputs:  LYR3 (Interest Holder)                                  #
    #####################################################################
    def loadTenureHolder(self):  
        # load the Tenure holder non-spatial table
        uri = QgsDataSourceUri()
        uri.setConnection('bcgw.bcgov', '1521', 'idwprod1.bcgov', self.user, self.pWord)
        connInfo = uri.connectionInfo()
        uri.setPassword(self.pWord)
        uri.setUsername(self.user)
        uri.setDataSource("WHSE_TANTALIS", "TA_INTEREST_HOLDER_VW", None)
        #uri.setWkbType(QgsWkbTypes.Polygon)
        #uri.setSrid('3005')
        uri.setKeyColumn('ROW_UNIQUEID')
        uri.setUseEstimatedMetadata(True)
        self.LYR3 = QgsVectorLayer(uri.uri(), "LYR3", "oracle")
        QgsProject.instance().addMapLayer(self.LYR3)

    #####################################################################
    # function: runClip                                                 #
    # inputs:  self.user, self.pWord, LYR, LYR2                         #
    # outputs:  clipped polygon of tenures inside of fire as shape      #
    #####################################################################
    def runClip(self):
        # set input and output file names
        firePath = self.LYR2
        tenurePath = self.LYR
        clipPath = "memory:"
        # run the clip
        clipFile = processing.run("native:clip", {'INPUT':tenurePath, 'OVERLAY':firePath, 'OUTPUT':clipPath})
        layer = QgsProject.instance().addMapLayer(clipFile['OUTPUT'])
        # Can't export binary fields - delete them
        res = layer.dataProvider().deleteAttributes([22])
        # Calculate the ha of tenures found in the fire
        layer.dataProvider().addAttributes([QgsField("hafire", QVariant.Double)])
        layer.updateFields()
        # The context variable is just an expression
        # $area simply calculates the area of the features in a layer
        #  in the projected coordinate unit (metres in 3005)
        context = QgsExpressionContext()
        context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))
        expression1 = QgsExpression('$area')
        with edit(layer):
            for f in layer.getFeatures():
                context.setFeature(f)
                f['hafire'] = expression1.evaluate(context)
                layer.updateFeature(f)
        #testing
        shpField='INTRID_SID'
        csvField='INTERESTED_PARTY_SID'
        result = processing.run('native:joinattributestable', {'INPUT':layer, 'INPUT_2':self.LYR3, 'FIELD':shpField, 'FIELD_2':csvField, 'OUTPUT':clipPath})
        layer = QgsProject.instance().addMapLayer(result['OUTPUT'])
        layer.dataProvider().addAttributes([QgsField("holder", QVariant.String, 'text', 254)])
        layer.updateFields()
        # Get the Tenure holders into a single text field
        context = QgsExpressionContext()
        context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))
        expression1 = QgsExpression('if( "ORGANIZATIONS_LEGAL_NAME" IS NOT NULL,  "ORGANIZATIONS_LEGAL_NAME",  "INDIVIDUALS_FIRST_NAME" +  \' \'  + "INDIVIDUALS_LAST_NAME")')
        with edit(layer):
            for f in layer.getFeatures():
                context.setFeature(f)
                f['holder'] = expression1.evaluate(context)
                layer.updateFeature(f)
        #end testing
        crs=QgsCoordinateReferenceSystem("epsg:3005")
        # Check if the path the user selected exists or make it
        Path(os.path.join(self.txt_outFolder.text(), "shapes")).mkdir(parents=True, exist_ok=True)
        # Export clipped tenures as a shape
        save_options = QgsVectorFileWriter.SaveVectorOptions()
        save_options.driverName = "ESRI Shapefile"
        save_options.fileEncoding = "UTF-8"
        transform_context = QgsProject.instance().transformContext()
        QgsVectorFileWriter.writeAsVectorFormatV2(layer,
                                                  os.path.join(self.txt_outFolder.text(), "shapes", self.txt_fireNumber.text() + "_clipped"),
                                                  transform_context,
                                                  save_options) 
        self.clipLayer = QgsVectorLayer(os.path.join(self.txt_outFolder.text(), "shapes", self.txt_fireNumber.text() + "_clipped.shp"), "layer_shp", "ogr")

    #####################################################################
    # function: updateWorksheet                                         #
    # inputs:  self.user, self.pWord                                    #
    # outputs:  excel report                                            #
    #####################################################################     
    def updateWorksheet(self):
        self.clipLayer = QgsVectorLayer(os.path.join(self.txt_outFolder.text(), "shapes", self.txt_fireNumber.text() + "_clipped.shp"), "layer_shp", "ogr")
        # update the status text
        # Lets create a report for tenures inside the fire
        workbook = xlsxwriter.Workbook(os.path.join(self.txt_outFolder.text(), self.txt_fireNumber.text() + '.xlsx'))
        worksheet = workbook.add_worksheet()
        # Format the title row to make it pretty
        merge_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': 'vjustify'})
        worksheet.merge_range('A1:A3', 'Crown Lands File Number ', merge_format)
        worksheet.merge_range('B1:B3', 'Tenure Holder Name', merge_format)
        worksheet.merge_range('C1:C3', 'Tenure Type', merge_format)
        worksheet.merge_range('D1:D3', 'Tenure Subtype', merge_format)
        worksheet.merge_range('E1:E3', 'Tenure Purpose', merge_format)
        worksheet.merge_range('F1:F3', 'Tenure Subpurpose', merge_format)
        worksheet.merge_range('G1:G3', 'Tenure Total Area (ha)', merge_format)
        worksheet.merge_range('H1:H3', 'Tenure Area within 2021 Fire Perimeter (ha)', merge_format)
        worksheet.merge_range('I1:I3', '% of Tenure Within Fire Perimeter', merge_format)
        worksheet.set_column(0,1,15)
        worksheet.set_column(1,1,15)
        worksheet.set_column(2,1,15)
        worksheet.set_column(3,1,15)
        worksheet.set_column(4,1,15)
        worksheet.set_column(5,1,15)
        worksheet.set_column(6,1,15)
        worksheet.set_column(7,1,15)
        worksheet.set_column(8,1,15)
        clipAtt = self.clipLayer.getFeatures()
        # xi is just a number for adding the clipped tenures
        #  data to the Excel sheet. Start at four based on
        #  formatting
        xi = 4
        ha_format = workbook.add_format({'num_format': '###,###,###,##0.00'})
        for att in clipAtt:
            attrs = att.attributes()
            # variable 'attrs' is a qvariant and thus is a
            #  C++ attribute. Must perform NULL check or will
            #  fail. Check is if then variable name (if attrs[#])
            if attrs[7]:
                print(attrs[7])
                worksheet.write('A' + str(xi), attrs[7])
            if attrs[33]:
                print(attrs[33])
                worksheet.write('B' + str(xi), attrs[33])
            if attrs[3]:
                print(attrs[3])
                worksheet.write('C' + str(xi), attrs[3])
            if attrs[4]:
                print(attrs[4])
                worksheet.write('D' + str(xi), attrs[4])
            if attrs[5]:
                print(attrs[5])
                worksheet.write('E' + str(xi), attrs[5])
            if attrs[6]:
                print(attrs[6])
                worksheet.write('F' + str(xi), attrs[6])
            if attrs[19]:
                print(attrs[19]/10000)
                worksheet.write('G' + str(xi), attrs[19]/10000, ha_format)
            if attrs[5]:
                print(attrs[5])
                worksheet.write('H' + str(xi), attrs[22]/10000, ha_format)
                print(attrs[5])
                worksheet.write('I' + str(xi), attrs[22]/attrs[19]*100, ha_format)
            # increment xi
            xi = xi + 1
        # Close the workbook - no need to save
        workbook.close()

if __name__ == '__main__':
    # You need one (and only one) QApplication instance per application.
    # Pass in sys.argv to allow command line arguments for your app.
    # If you know you won't use command line arguments QApplication([]) works too.
    app = QApplication(sys.argv)
    # Gotta set some paths here. Bad python 3 install on this server
    if path.exists():
        QgsApplication.setPrefixPath("E:\\sw_nt\\QGIS_3.10\\apps\\qgis-ltr", True)
        os.environ['QGIS_PREFIX_PATH'] = 'E:\\sw_nt\\QGIS_3.10\\apps\\qgis-ltr'
    else:
        QgsApplication.setPrefixPath("E:\\sw_nt\\QGIS_3.16\\apps\\qgis-ltr", True)
        os.environ['QGIS_PREFIX_PATH'] = 'E:\\sw_nt\\QGIS_3.16\\apps\\qgis-ltr'
    # A lot of this stuff looks like it could be moved to the top of this
    # script. It can't be.
    # !DO NOT CLEAN THIS CODE OR MOVE MODULE IMPORTS OR SCRIPT WILL BREAK!
    qgs = QgsApplication([], False)
    qgs.initQgis()
    import processing
    from processing.core.Processing import Processing
    Processing.initialize()
    from qgis.analysis import QgsNativeAlgorithms
    QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
    ex = App()
    # Start the event loop.
    app.exec()
    # Your application won't reach here until you exit and the event
    # loop has stopped.
    qgs.exitQgis()
```

You should now see a report and shapes folder in your output directory after you run the script. 
If the report is empty there were no tenures impacted by that fire. Try fire number C41602.

This is a simple application with no error checking and only text inputs but more complicated apps can be created. 
If this seems confusing at first, give it some time. Once you get used to it it is much more powerful and end user friendly than non-GUI apps.
