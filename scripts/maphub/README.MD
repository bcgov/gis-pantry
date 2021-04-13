# maphub_services.py
This module has a few methods for working with ArcGIS online featureclasses from python 3.x. This may also work with python 2.7 although it is untested. This is still a work in progress and some features may not work correctly in any/all cases.

# usage
create maphub services object with 
```
mh = Maphubs(user,password,serviceurl)
```

delete all features from a feature service
```
mh.delete_features(featureServiceLayer='my featureservice name',query='1=1')
```

add features to a feature service

```
# features_json is esri structured json. ESRI users can use arcpy.FeatureSet().JSON() to produce this from a dataset.   
mh.add_features(featureServiceLayer='my featureservice name',features_json=mynewfeature_json)
```
# example with configparser for credentials

```
config = configparser.ConfigParser()
config.read('H:/Secrets/caribouApp_updater.ini')
appId = config['CaribouApp']['AppID']
secret = config['CaribouApp']['secret']
redirectUri = config['CaribouApp']['secret']
service_url = 'https://services6.arcgis.com/ubm4tcTYICKBpist/arcgis/rest/services'


myobj = Maphubs(appId,secret,'https://services6.arcgis.com/ubm4tcTYICKBpist/arcgis/rest/services')
testFs = 'https://services6.arcgis.com/ubm4tcTYICKBpist/arcgis/rest/services/test_points/FeatureServer/0'
new_feature = [
    {
    "geometry" : {"x" : -127.47041, "y" : 54.4217,"spatialReference" : {"wkid" : 4326}},
    "attributes" : {
        "idCollar":'my test addition'
        }
    }
]

y = 54.13633
x = -127.45802
print (myobj.get_features('my feature service name'))
print (myobj.delete_features('test_points',objectIdList=[2]))
mulitpnt = [[-127.45802,54.13633],[-127.47041,54.4217]]
print (myobj.is_intersecting('my feature service name',esri_geom_json=mulitpnt,geometryType='esriGeometryMultipoint'))


oidField = 'Wshd_ID'
for zone in [23,17]:
    def_query = "{} = {}".format(oidField,zone)
    expression=[{"field":"Status","value":'Closed'},
            {"field":"Chng_Date","value":datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')},
            {"field":"Update_On","value":datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')}]
    myobj.calculate_attributes(featureServiceLayer='management areas test',def_query=def_query,expression=expression)
```
