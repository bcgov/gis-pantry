# Libaries for accessing and interacting with S3 Objects

## create_presigned_url_for_s3_objects.py

This script is an example of using the BOTO3 python client libraries for generating a token based expiry URL to access objects in S3 Storage buckets.
NOTE: If your s3 bucket is public, you do not need to use pre-signed url generation script - (ie just go to something like this url - https://nrs.objectstore.gov.bc.ca/<bucket name>/<object name>)
   IDIR authentication link for more information - https://apps.nrs.gov.bc.ca/int/confluence/display/OPTIMIZE/NRM+Object+Storage+Service
    •specifici to BC Object Storage solution - ECS Rest API Reference http://doc.isilon.com/ECS/3.6/API/index.html
 
      Data: 2021-05-03
   Author: michelle.douville@gov.bc.ca
   
   usage: python create_presigned_url_for_s3_objects.py

   example: 
```bash
python create_presigned_url_for_s3_objects.py
```

NOTES:
* currently there are no command line configs 
* the script looks for env vars for AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY 
* there are script variables for endpoint URL, expiration (seconds) and bucket name (all with defaults)
* This script returns a read only URL that provides access to a S3 object for a pre-determined amount of time (expiration)
* example url: https://nrs.objectstore.gov.bc.ca/nrs-iit/test.txt?AWSAccessKeyId=nrs-iit-user&Signature=K0RNRj84b3IR8uYwdShwFcbbCmY%3D&Expires=1620086854 .. 
* this is a time based access key (3600s = 1 hr) expires Mon May 03 2021 17:07:34 GMT-0700 (Pacific Daylight Time) 
* expiration date format see (https://www.unixtimestamp.com/index.php)  
* there are other options for upload/write etc. (Ie Simialr functions to FTP)- it uses boto3 python libraries although minio libs are fun too.  
* see https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html

 
## python libraries required
* boto3
* os

## parameters 
### provide the default parameters for expirary, endpoint, and bucketname for the S3 Object
* expiration = 3600 # default is 1 hour
* endpoint_url='https://nrs.objectstore.gov.bc.ca:443/' # endpoint for S3 Object Storage -- if this isn't specified it will try and go to Amazon S3
* bucketname = 'nrs-iit'

### this script requires access to secret/secure information store as environment variables that are picked up at runtime
* AWS_SERVER_PUBLIC_KEY = os.environ.get('AWS_ACCESS_KEY_ID')  # access key for s3 object storage 
* AWS_SERVER_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY') # secret ky for S3 object storage
