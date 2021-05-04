# Libaries for accessing and interacting with S3 Objects

## create_presigned_url_for_s3_objects.py

This script is an example of using the BOTO3 python client libraries for generating a token based expiry URL to access objects in S3 Storage buckets.

   Data: 2021-05-03
   Author: michelle.douville@gov.bc.ca
   
   usage: python create_presigned_url_for_s3_objects.py

   example: 
```bash
python create_presigned_url_for_s3_objects.py
```

   NOTES:  (currently there are no command line configs, but looks for env vars for AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY, 
   and the endpoint URL/bucket name are parameters with a default)
   This script returns, an URL that provides access to a S3 object for a pre-determined amount of time (expiration)
 

## python libraries required
* boto3
* os

## parameters 
# provide the default parameters for expirary, endpoint, and bucketname for the S3 Object
expiration = 3600 # default is 1 hour
endpoint_url='https://nrs.objectstore.gov.bc.ca:443/' # endpoint for S3 Object Storage -- if this isn't specified it will try and go to Amazon S3
bucketname = 'nrs-iit'

# this script requires access to secret/secure information store as environment variables that are picked up at runtime
AWS_SERVER_PUBLIC_KEY = os.environ.get('AWS_ACCESS_KEY_ID')  # access key for s3 object storage 
AWS_SERVER_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY') # secret ky for S3 object storage
