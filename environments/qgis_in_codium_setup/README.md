# Connecting VS Codium to QGIS Environment
Create a new VS profile and edit the profile settings 
Ctrl+Shift+P to open Preferences: Open User Settings (JSON)
and for your settings copy in the settings found in the profile.json

Then in a script, import bcgov_qgis_boiler_plate, It can also be found in P:/corp
- and i need to add this in a way where they are linked...
- who manages it now?
- should they add it for versioning sake?
- I have questions.
- but i am not sure what they all are because I do not know enough about this yet...

import sys
sys.path.append("P:/corp/script_whse/python/Analysis/Ready/qgis_environment")
import bcgov_qgis_boiler_plate

Voila! You should be able to use QGIS headless in your script or notebook and swap in and out of profiles easily.