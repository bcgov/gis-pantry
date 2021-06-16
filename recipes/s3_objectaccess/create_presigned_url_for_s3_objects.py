"""example of using the BOTO3 python client libraries for generating a token based expiry URL to access objects in S3 Storage buckets
   Data: 2021-05-03
   Author: michelle.douville@gov.bc.ca
   
   usuage: python create_presigned_url_for_s3_objects.py

   NOTES:  (currently there are no command line configs, but looks for env vars for AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY, 
   and the endpoint URL/bucket name are parameters with a default)
   This script returns, an URL that provides access to a S3 object for a pre-determined amount of time (expiration)
 """

# see https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html

import logging
import boto3
from botocore.exceptions import ClientError
import os

object2share = 'test.txt' # name of object to share

# provide the default parameters for expirary, endpoint, and bucketname for the S3 Object
expiration = 3600 # default is 1 hour
endpoint_url='https://nrs.objectstore.gov.bc.ca:443/' # endpoint for S3 Object Storage -- if this isn't specified it will try and go to Amazon S3
bucketname = 'nrs-iit'

# this script requires access to secret/secure information store as environment variables that are picked up at runtime
AWS_SERVER_PUBLIC_KEY = os.environ.get('AWS_ACCESS_KEY_ID')  # access key for s3 object storage 
AWS_SERVER_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY') # secret ky for S3 object storage


# use third party object storage
s3 = boto3.resource('s3', endpoint_url=endpoint_url,
  aws_access_key_id = AWS_SERVER_PUBLIC_KEY,
  aws_secret_access_key = AWS_SERVER_SECRET_KEY)

# defint the function for create the URL, the script if it works will return a shareable URL in the print output
def create_presigned_url(bucket_name, object_name, endpoint_url, expiration=expiration):
    
    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3',endpoint_url=endpoint_url, 
      aws_access_key_id = AWS_SERVER_PUBLIC_KEY,
      aws_secret_access_key = AWS_SERVER_SECRET_KEY)
    
    try:
        response = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket_name,'Key': object_name},ExpiresIn=expiration)
        print(response)

    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response

# run the function with the give parameters.
create_presigned_url(bucketname, object2share, endpoint_url)