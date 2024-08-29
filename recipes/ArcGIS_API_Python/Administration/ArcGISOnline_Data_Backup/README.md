# ArcGIS Online Dependency Checker
Emma Armitage
August 29, 2024

## Overview
This script downloads data and associated attachments from ArcGIS Online as a GeoJSON file to Amazon S3 object storage.

## Usage
You will need to configure the script with the following parameters:

> ### Parameters\
####In the function get_input_parameters():\
'ago_user:' ArcGIS Online username\
'ago_pass:' ArcGIS Online password\
'obj_store_user:' Object Storage user id\
'obj_store_api_key:' Object Storage api key\
>> 'obj_store_host:' Object Storage url\
> portal_url: MapHub or other AGO portal url\
> bucket: Object Storage bucket\
> bucket_prefix: Object Storage "folder name"\
> ago_layer_id: ArcGIS Online Feature Layer ID\
> edited_ago_layer_id: ArcGIS Online Feature Layer ID\
> layer_name: ArcGIS Online feature layer name\

There may be a number of relevant limitations. The script may not find all usages in all cases.
> ### Limitations


## Details of output


