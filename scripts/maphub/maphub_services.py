import os
import configparser
import requests
import json
import sys
import logging
import datetime
logging.basicConfig(level=logging.DEBUG)

class Maphubs:
    '''description: this object can be used to add, delete features from feature services
                on esri arcgis online
        author: Will Burt
        history: Created July 7, 2019
        edited: Edited Dec 11, 2019
    '''

    def __init__(self,client,secret,root_url):
        self.token, self.http, self.expires= self.getTokenOauth2(client=client,secret=secret)
        self.hub_url = root_url

    def getTokenOauth2(self,client, secret): 
        """Generates a token."""
        referer = "http://www.arcgis.com/"
        query_dict = {'client_id': client,
                        'client_secret': secret,
                        'grant_type': 'client_credentials'}

        url = "https://www.arcgis.com/sharing/rest/oauth2/token" #?client={}&client_secret={}&grant_type=client_credentials".format(client,secret)
        r = requests.post(url,params=query_dict)
        token = r.json()

        if "access_token" not in token.keys():
            print(token['error'])
            sys.exit(1)
        else:
            
            return token['access_token'], 'https://www.arcgis.com/sharing/rest/oauth2/token', token['expires_in']


    def add_features(self,featureServiceLayer,features_json):
        ''' This function adds a features to your feature service
        featureService: feature service name(string) eg. my_test_points
        features_json: json template
        [
        {
        "geometry" : {"x" : -118.15, "y" : 33.80},
        "attributes" : {
            "OWNER" : "Joe Smith",
            "VALUE" : 94820.37,
            "APPROVED" : true,
            "LASTUPDATE" : 1227663551096
            }
        }
        ]
         '''
        data = {'f': 'pjson','token':self.token, 'features':json.dumps(features_json)}
        url = self.hub_url + '/' + featureServiceLayer+ '/FeatureServer/0/addFeatures'
        #r = requests.post(url + "?", data=data, verify=True)
        r = requests.post(url, data=data, verify=True)
        #returns the response as json
        return r.json()
    def delete_features(self,featureServiceLayer, objectIdList=None,query=None,geometry=None,geometryType=None):
        ''' 
        Delete features from feature service using one
        or a combination of parameters
        featureService: feature service name(string) eg. my_test_points
        objectIdList: list of existing objectid to be deleted eg. [148,248,567]
        query: where clause for selecting features eg 1=1 deletes all features
        geometry: https://developers.arcgis.com/documentation/common-data-types/geometry-objects.htm
        geometryType: The type of geometry specified by the geometry parameter.
            The geometry type can be an envelope, a point, a line, or a polygon. The default geometry type is an envelope.
            Values: esriGeometryPoint | esriGeometryMultipoint |
                esriGeometryPolyline | esriGeometryPolygon | esriGeometryEnvelope

        https://developers.arcgis.com/rest/services-reference/delete-features.htm
        '''
        query_dict = {'f': 'json','token':self.token}
        if query is not None:
            query_dict['where'] = query
        if objectIdList is not None:
            str_oidList = str(objectIdList.pop())
            if len(objectIdList)> 0:
                for oid in objectIdList:
                    str_oidList = str_oidList + "," + str(oid)
            query_dict['objectIds'] = str_oidList
        if geometry is not None:
            query_dict['geometry'] = geometry
        if geometryType is not None:
            query_dict['geometryType'] = geometryType
        url = self.hub_url + '/' + featureServiceLayer+ '/FeatureServer/0' + '/deleteFeatures'
        r = requests.post(url + "?", data=query_dict, verify=True)
        return r.json()
    def source_to_features(self, source, source_type='ESRI_FGDB'):
        pass
    def get_features(self,featureServiceLayer, query='1=1',sr='4326',return_geometry=True,fields='*'):
        data = {'f': 'json','token':self.token,
            'where':query,
            'outSR': sr,
            'returnGeometry':return_geometry,
            'outFields':fields,
            }
        url = self.hub_url + '/' + featureServiceLayer+ '/FeatureServer/0/query'
        r = requests.post(url + "?", data=data, verify=True)
        #returns the response as json
        return r.json()
    def get_features_by_geom(self,featureServiceLayer,fields='*', query='1=1',esri_geom_json=None,\
        geometryType='esriGeometryPoint',spatialRel='esriSpatialRelIntersects',\
            in_sr='4326',sr='4326'):
        # https://developers.arcgis.com/documentation/common-data-types/geometry-objects.htm
        # envelope
        # {"xmin" : -109.55, "ymin" : 25.76, "xmax" : -86.39, "ymax" : 49.94,
        # "spatialReference" : {"wkid" : 4326}}
        # Point
        # {"x" : -118.15, "y" : 33.80, "spatialReference" : {"wkid" : 4326}}
        data = {'f':'json','token':self.token,
            'where':query,
            'geometry': esri_geom_json,
            'geometryType':geometryType,
            'returnHiddenFields':True,
            'outFields':fields,
            'spatialRel':spatialRel,
            'outSR': sr
            }
        url = self.hub_url + '/' + featureServiceLayer+ '/FeatureServer/0/query'
        r = requests.post(url + "?", data=data, verify=True)
        #returns the response as json
        return r.json()

    def is_in_proximaty(self,featureServiceLayer, esri_geom_json,distance=1000,query='1=1',\
        geometryType='esriGeometryPoint',spatialRel='esriSpatialRelIntersects',\
            in_sr='4326',sr='4326'):
        data = {'f':'json','token':self.token,
            'where':query,
            'geometry': esri_geom_json,
            'geometryType':geometryType,
            'returnCountOnly':'true',
            'spatialRel':spatialRel,
            'outSR': sr
            }
        url = self.hub_url + '/' + featureServiceLayer+ '/FeatureServer/0/query'
        r = requests.post(url + "?", data=data, verify=True)
        count_response = False
        if r.json()['count']>0:
            count_response=True
        return count_response

    def update_features(self,featureServiceLayer,esri_json,rollback='false'):
        """
        Updates featureServiceLayer with esri_json. Object ids must match respective features on
        featuresServiceLayer
        """
        # updates features by object id 
        data = {'f': 'json','token':self.token,
            'features':json.dumps(esri_json),
            'rollbackOnFailure':rollback
            }
        url = self.hub_url + '/' + featureServiceLayer+ '/FeatureServer/0/updateFeatures'
        r = requests.post(url + "?", data=data, verify=True)
        #returns the response as json
        return r.json()
    def calculate_attributes(self,featureServiceLayer,def_query, expression):
        data = {'f':'pjson',
                'token':self.token,
                'where':def_query,
                'calcExpression': str(expression),
                'sqlFormat':'standard',
                'rollbackOnArithmaticError': 'false'
            }

        url = self.hub_url + '/' + featureServiceLayer+ '/FeatureServer/0/calculate'
        r = requests.post(url+'?', params=data)
        return r.json()
    def get_objectid_uniquefield_dict(self,featureServiceLayer,unique_field):
        """
        Get dictionary of {unique_field:objectID} for features in feature service layer
        Utility for updating attributes
        """
        r = self.get_features(featureServiceLayer=featureServiceLayer,return_geometry=False)
        features = r['features']
        oid_field = r['objectIdFieldName']
        fs_fields = [f["name"] for f in r['fields']]
        assert unique_field in fs_fields
        pair_dict = {}
        for f in features:
            pair_dict[f['attributes'][unique_field]]=f['attributes'][oid_field]
        return pair_dict

# if __name__ == "__main__":

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
print (myobj.get_features('StarrBasinBoundary'))
print (myobj.delete_features('test_points',objectIdList=[2]))
mulitpnt = [[-127.45802,54.13633],[-127.47041,54.4217]]
print (myobj.is_intersecting('StarrBasinBoundary',esri_geom_json=mulitpnt,geometryType='esriGeometryMultipoint'))


oidField = 'Wshd_ID'
for zone in [23,17]:
    def_query = "{} = {}".format(oidField,zone)
    expression=[{"field":"Status","value":'Closed'},
            {"field":"Chng_Date","value":datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')},
            {"field":"Update_On","value":datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')}]
    myobj.calculate_attributes(featureServiceLayer='management areas test',def_query=def_query,expression=expression)

