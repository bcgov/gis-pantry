# Backup ArcGIS Online Data and Attachments to Object Storage
Emma Armitage\
August 29, 2024

## Overview
This script downloads data and associated attachments from ArcGIS Online as a GeoJSON file to Amazon S3 object storage.\
The script is currently written to backup two feature layers 

## Usage
You will need to configure the script with the following parameters:

> ### Parameters
In the `run_app()` function:\
`ago_layer_id`: ArcGIS Online Feature Layer ID\
`edited_ago_layer_id`: ArcGIS Online Feature Layer ID\
`layer_name`: ArcGIS Online feature layer name

In the `get_input_parameters()` function:\
`ago_user`: ArcGIS Online username\
`ago_pass`: ArcGIS Online password\
`obj_store_user`: Object Storage user id\
`obj_store_api_key`: Object Storage api key\
`obj_store_host`: Object Storage url

In the `Backup Data` class:\
`self.portal_url`: MapHub or other AGO portal url\
`self.bucket`: Object Storage bucket\
`self.bucket_prefix`: Object Storage "folder name"

> ### Execution
GitHub Actions is used to automate the running of the script. ArcGIS Online and Object Storage credentials are stored as Action secrets. 


