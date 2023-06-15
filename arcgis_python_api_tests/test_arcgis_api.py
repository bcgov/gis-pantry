'''
test_arcgis_api.py
description: methods for testing arcgis python api

Copyright 2023 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at 

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

'''

import os
import sys
from arcgis.gis import GIS

userid = os.environ['MH_USER']
usercred = os.environ['MH_PASSWORD']
arcgis_online_url = r"https://governmentofbc.maps.arcgis.com"

def test_arcgis_gis_anonymous():
    ''' Connection to arcgis online can be made anonymously'''
    mh = GIS()
    assert mh._is_agol

def test_arcgis_gis_with_user():
    ''' Connection to arcgis online can be made by user'''
    mh = GIS(username=userid,password=usercred)
    assert mh._is_agol

def test_listing_maphub_content():
    ''' Connection to arcgis online can be made by user'''
    mh = GIS(username=userid,password=usercred)
    c = mh.content.search(query="owner:Province.Of.British.Columbia",max_items=1200)
    assert len(c) > 500

def test_get_item_by_id():
    ''' Get content by id'''
    mh = GIS(username=userid,password=usercred)
    item = mh.content.get('d3fef65386df4e63b02d6e23bb98a1ee')
    assert item is not None

def test_item_export_download():
    ''' Export and download content'''
    mh = GIS(username=userid,password=usercred)
    item = mh.content.get('d3fef65386df4e63b02d6e23bb98a1ee')
    dl = item.export(title='pytest_canada_download',export_format="GeoJson",wait=True)
    result = dl.download()
    assert result is not None

def test_for_separatists():
    ''' layer.query() returns expected results'''
    mh = GIS(username=userid,password=usercred)
    item = mh.content.get('d3fef65386df4e63b02d6e23bb98a1ee')
    d = item.layers[0].query()
    assert len(d.features)==13

