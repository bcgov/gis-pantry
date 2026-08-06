# Connecting VS Codium to the QGIS Python Environment (For VDIs QGIS install)

This guide shows how to set up your Codium environment to write QGIS scripts in 
Codium instead of using the QGIS Python console.

### Why code QGIS in Codium?
- linting & code completion
- debugging
- notebooks

### Create a new profile for this environment 
By creating a new profile for QGIS settings swaping between environments becomes easy.

## Setup
### Create a new Codium Profile
To make set up easier when you are creating a new profile, 
copy the extentions from another profile you have already set up.
Otherwize, the main extention you need is Python. 

### Edit your new profile
After you have created your new profile, make sure it is active and use
Ctrl+Shift+P to open the menu and select Preferences: Open User Settings (JSON)
to open your new profile settings. 
Copy in the settings found in the profile.json

After saving your profile settings, check the correct python interperter is selected:
Ctrl+Shift+P then select (or type to find) Python: Select Interperter
It should have C:/Program Files/QGIS 3.40.7/apps/Python312/python.exe highlighted.

## Scripting
In your scripts, import bcgov_qgis_boiler_plate, it can also be found in P:/corp
You should see "Boilerplate ran OK:  " on sucessful import.
The boiler plate:
- Configures the QGIS environment paths and variables. Including library paths for:
    - GDAL
    - PROJ
    - Qt
    - Qgis Processing tools
- Initializes PyQGIS
- Runs QGIS headlessly (No desktop application open)

### *!!!! TODO look into this*
# and i need to add this in a way where they are linked...
# who manages it now?
# should they add it for versioning sake?
# I have questions.
# but i am not sure what they all are because I do not know enough about this yet...

import sys
sys.path.append("P:/corp/script_whse/python/Analysis/Ready/qgis_environment")
import bcgov_qgis_boiler_plate

**Voila! You should be able to run QGIS headless in your script or notebook and be able to switch bewteen Python environments by changing your active profile!**