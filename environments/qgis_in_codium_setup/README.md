# Connecting VS Codium to the QGIS Python Environment in any VDI

This guide shows how to set up your Codium environment to write QGIS scripts in 
Codium instead of using the QGIS Python console.

**Why Code QGIS In Codium?**
- Linting & code completion
- Debugging
- Notebooks

## Setup
### Create A New VS Codium Profile
- Navigate to the bottom left Settings cog in Codium > Profile(current profile) > Profiles. <br>
- Select New Profile. <br>
- Update the profile Name and Icon if you like.<br>
- Optional: If you have a profile with extentions you like to use regulary, such as Better Comments, Todo Tree, or autoDocstring, copy the extentions from that profile during setup so you do not have to reinstall them.
- If you are not copying extentions from another profile, install the Python extention. It is the only extention required for this setup. 


### Edit The Profile Settings
After you have created your new profile, make sure it is active and use
Ctrl+Shift+P to open the menu and select `Preferences: Open User Settings (JSON)`
to open your new profile settings. 
Copy in the settings found in the profile.json

After saving your profile settings, check the correct python interpreter is selected:
Ctrl+Shift+P then select (or type to find) `Python: Select Interpreter`
It should have <mark>C:/Program Files/QGIS 3.40.7/apps/Python312/python.exe</mark> highlighted. If not, navigate to it for the first time.

## Scripting
In your scripts, `import bcgov_qgis_boiler_plate`, it can also be found in P:/corp. <br>
You should see `"Boilerplate ran OK:  "` on successful import.

The boiler plate:<br>
- Configures the QGIS environment paths and variables. Including library paths for:
    - GDAL
    - PROJ
    - Qt
    - Qgis Processing tools
- Initializes PyQGIS
- Runs QGIS headlessly (No desktop application open)


**Voila!** 
You should be able to run QGIS headless in a script or notebook and be able to switch bewtween Python environments by changing your active profile!