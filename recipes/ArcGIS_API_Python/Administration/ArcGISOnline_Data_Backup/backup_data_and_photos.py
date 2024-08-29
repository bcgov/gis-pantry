"""
Backup AGO Data and Attachments Script 
Backs up AGO feature layer data as geojson and attachments to object storage
Written to run in GitHub Actions

Currently written to backup data from two AGO feature layers

Author: Emma Armitage (some code adapted from Graydon Shevchenko)
Aug 29, 2024

"""
# imports 
import os
import boto3
from arcgis.gis import GIS 
from datetime import datetime

def run_app():

    ago_user, ago_pass, obj_store_user, obj_store_api_key, obj_store_host = get_input_parameters()
    report = BackupData(ago_user=ago_user, ago_pass=ago_pass, obj_store_user=obj_store_user, obj_store_api_key=obj_store_api_key, obj_store_host=obj_store_host)
    ago_item, ago_flayer, flayer_properties, flayer_data, edited_ago_item = report.get_feature_layer_data(ago_layer_id='', # add ago layer id here
                                                                                                          edited_ago_layer_id='', # add ago layer id here
                                                                                                          layer_name='') # add ago layer name here
    report.rename_attachments(ago_flayer=ago_flayer,
                              flayer_properties=flayer_properties,
                              flayer_data=flayer_data)
    report.download_attachments(ago_flayer=ago_flayer,
                                flayer_properties=flayer_properties,
                                flayer_data=flayer_data)
    
    item_list = [ago_item, edited_ago_item]
    counter = 1
    for item in item_list:
        geojson_path = report.download_geojson(item, counter)
        report.save_geojson_to_os(geojson_path, counter)
        counter +=1

    del report 

# get user login credentials
def get_input_parameters():
    """
    Function:
        Set up parameters

    Returns:
        tuple: user entered parameters required for tool execution
    """
    
    ago_user = os.environ['AGO_USER'] # arcgis online username
    ago_pass = os.environ['AGO_PASS'] # arcgis online password
    obj_store_user = os.environ['OBJ_STORE_USER'] # object storage user id
    obj_store_api_key = os.environ['OBJ_STORE_API_KEY'] # object storage api key
    obj_store_host = os.environ['OBJ_STORE_HOST'] # object storage url

    return ago_user, ago_pass, obj_store_user, obj_store_api_key, obj_store_host


# connect to AGOL and object storage
class BackupData:
    def __init__(self, ago_user, ago_pass, obj_store_user, obj_store_api_key, obj_store_host) -> None:
        self.ago_user = ago_user
        self.ago_pass = ago_pass
        self.obj_store_user = obj_store_user
        self.obj_store_api_key = obj_store_api_key
        self.object_store_host = obj_store_host

        self.portal_url = '' # add MapHub or other AGO url here

        self.bucket = '' # add the object storage bucket name here
        self.bucket_prefix = '' # add your bucket "folder name" here

        print("Connecting to MapHub")
        self.gis = GIS(url=self.portal_url, username=self.ago_user, password=self.ago_pass, expiration=9999)
        print("Connection successful")

        print("Connecting to object storage")
        self.boto_resource = boto3.resource(service_name='s3',
                                            aws_access_key_id=self.obj_store_user,
                                            aws_secret_access_key=self.obj_store_api_key,
                                            endpoint_url=f'https://{self.object_store_host}')
        
    def __del__(self) -> None:
        print("Disconnecting from MapHub")
        del self.gis
        print("Closing object storage connection")
        del self.boto_resource 

    # get feature layer data
    def get_feature_layer_data(self, ago_layer_id, layer_name):
        """
        Gets AGO feature layer, feature layer properties, and feature layer properties
        """
        ago_item = self.gis.content.get(ago_layer_id)
        if layer_name == '': # query for layer name
            ago_flayer = ago_item.layers[0]
        flayer_properties = ago_flayer.query()
        flayer_data = flayer_properties.features

        return ago_flayer, flayer_properties, flayer_data
        
    def list_contents(self) -> list:
        """
        Get a list of object storage contents

        Returns: list of object storage contents
        """
        obj_bucket = self.boto_resource.Bucket(self.bucket)
        lst_objects = []
        for obj in obj_bucket.objects.all():
            lst_objects.append(os.path.basename(obj.key))

        return lst_objects
        
    def download_attachments(self, ago_flayer, flayer_properties, flayer_data) -> None:
        """
        Function:
            Runs download attachment functions
        Returns:
            None
            
        """
        # get a list of pictures from object storage
        lst_pictures = self.list_contents()

        # copy new photos to object storage
        self.copy_to_object_storage(ago_flayer=ago_flayer, 
                                    flayer_properties=flayer_properties, 
                                    flayer_data=flayer_data, 
                                    picture="photo_name", lst_os_pictures=lst_pictures)

    def copy_to_object_storage(self, ago_flayer, flayer_properties, flayer_data, picture, lst_os_pictures) -> None:
        """
        Function:
            Downloads attachments from AGO feature layer and copies them to object storage.
        Returns:
            None
        """
        print(f"Downloading photos")
        
        if len(flayer_data) == 0:
            return
            
        # save all OIDs from the feature set in a list 
        lst_oids = flayer_properties.sdf["objectid"].tolist() # may need pandas for this but unsure

        # for each object id...
        for oid in lst_oids:
            # get a list of dictionaries containings information about attachments
            lst_attachments = ago_flayer.attachments.get_list(oid=oid)

            # check if there are attachments 
            if lst_attachments:

                # find the original feature 
                original_feature = [f for f in flayer_data if f.attributes["objectid"] == oid][0]

                # try to retrieve a list of picture attributes from the records in the feature layer 
                try:
                    lst_pictures = original_feature.attributes[picture].split(',')
                except:
                    # if there are no attachments associated with the record, create an empty list
                    lst_pictures = []

                # create a list of picture that are not already saved to object storage
                lst_new_pictures = [pic for pic in lst_pictures if pic not in lst_os_pictures]
                if not lst_new_pictures:
                    continue 

                # iterate through each attachment item
                for attach in lst_attachments:

                    # if the attachment's name is in the list of new pictures, copy the item to the object storage bucket
                    if attach['name'] in lst_new_pictures:
                        print(f"Copying {attach['name']} to object storage")
                        attach_id = attach['id']
                        attach_file = ago_flayer.attachments.download(oid=oid, attachment_id=attach_id)[0]
                        ostore_path = f"{self.bucket_prefix}/{attach['name']}"

                        self.boto_resource.meta.client.upload_file(attach_file, self.bucket, ostore_path)

    def download_geojson(self, ago_flayer, counter):
        """
        Downloads the AGO feature layer data as a GeoJSON

        The AGO export name depends on the counter variable and the order of ago items in item_list 
        --> see run_app() at top of script
        """
        now = datetime.now().strftime("%d-%m-%Y")
        
        if counter ==1:
            item_title = f'raw_data_{now}'
        else:
            item_title = f'edited_data_{now}'
        
        export_name = f'{item_title}_{now}'
        tmp_file_path = f'/tmp'

        # export the ago item as geojson
        ago_flayer.export(title=export_name,
                          export_format='GeoJson',
                          parameters=None,
                          wait=True)
        
        # search for the newly exported AGOL item
        geojson_item = self.gis.content.search(query=export_name, item_type='GeoJSON')
        geojson_id = geojson_item[0].id
        geosjon = self.gis.content.get(geojson_id)

        # download the ago item to GitHub Actions temporary directory
        print("Downloading AGO data as GeoJSON")
        geosjon.download(save_path=tmp_file_path,
                         file_name=f"{export_name}.geojson")
        
        # get the downloaded geojson's path
        geojson_path = os.path.join(tmp_file_path, f"{export_name}.geojson")
        
        # delete the downloaded file in AGO
        print("Deleting temporary GeoJSON in AGO")
        geosjon.delete()

        return geojson_path

    def save_geojson_to_os(self, geojson_path, counter):
        """
        Saves the geojson to object storage. 
        
        The object storage path depends on the counter variable and the order of ago items in item_list 
        --> see run_app() at top of script
        """
        now = datetime.now().strftime("%d-%m-%Y")

        if counter == 1:

            ostore_path = f'backup_data/survey123_raw_backup_data_{now}.geojson'

        else:
            ostore_path = f'backup_data/survey123_edited_backup_data_{now}.geojson'

        bucket_name = self.bucket

        try:
            with open(geojson_path, 'rb') as data:
                s3_object = self.boto_resource.Object(bucket_name, ostore_path)
                s3_object.put(
                    Body=data,
                    ContentType='application/geo+json'
                )
            print(f"GeoJSON data has been uploaded to s3://{bucket_name}/{ostore_path}")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == '__main__':
    run_app()
