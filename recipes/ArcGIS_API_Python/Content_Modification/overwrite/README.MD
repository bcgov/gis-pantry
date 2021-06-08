# overwrite_FS.py
# Background
This module has a class that allows users to overwrite existing feature services using ArcGIS API. This module is a modified version of a script posted by Jake Skinner, ESRI on [Esri community](https://community.esri.com/t5/arcgis-online-documents/overwrite-arcgis-online-feature-service-using-truncate-and/ta-p/904457) forum.


This script can be used independetly (i.e. run at ```__name__ == __main__``` towards the end of the script) or imported into existing script as a module. Assuming you have it in the same directory as the main script, add ```import overwrite_FS``` statement to your main script.
# Usage
1. Instantiate AGO object using your ArcGIS Online username. You will be prompted to enter your password.
```
import overwrite_FS
username = input("AGO Username: ")
password = getpass.getpass()
ago_obj = overwrite_FS.AGO(username,getpass)
```

2. Now you can use the ```ago_obj``` instantiated above to call the ```overwrite()``` method to overwrite online feature layer (or a table). It takes two positional arguments: ```featureclass_path``` and  ```featurelayer_id```.

```
featureclass_path = r'W:\data\test.gdb\test_featureclass'
featurelayer_id = '5e3e867ebf4940c4b100cc4dc977b011'

ago_obj.overwrite(featureclass_path,featurelayer_id)
```