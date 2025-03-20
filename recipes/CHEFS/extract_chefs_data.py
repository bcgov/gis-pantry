#------------------------------------------------------
# Purpose: Extracts data from CHEFS (Common Hosted Forms) api and converts it to a pandas dataframe
#
# Requirements: (1) CHEFS form ID
#               (2) CHEFS version ID
#
# Author: Emma Armitage
#
# Last Updated: 2025-03-20
#------------------------------------------------------

import base64
import urllib3
import json
import pandas as pd

form_id = ""                                                        # the form ID
api_key = ""                                                        # the api key
version_id = ""                                                     # the form version ID
base_url = "https://submit.digital.gov.bc.ca/app/api/v1/forms"      # the url from which to make the api call

# submission metadata (ex: date and time created, confirmation ID)
form_data_url = f"{base_url}/{form_id}/versions/{version_id}/submissions/discover"
# submission data
get_form_submission_url = f"{base_url}/{form_id}/submissions"

# initialize HTTP pool manager
http = urllib3.PoolManager()

# encode username and password for basic authentication
hash_string = base64.b64encode(f"{form_id}:{api_key}".encode()).decode()

# set headers for authorization
headers = {"Authorization": f"Basic {hash_string}"}

fields = {"fields":""}               # a comma seperated list of the field names you want to retrieve

# make the request
response_data = http.request("GET", form_data_url, fields=fields, headers=headers)
response_submissions = http.request("GET", get_form_submission_url, headers=headers)

# test the response
print(response_data.status)         # response status
print(response_data.data)           # response data

# convert response to json
response_data_decode = json.loads(response_data.data.decode("utf-8"))
response_submission_data = json.loads(response_submissions.data.decode("utf-8"))

# convert response to pandas dataframe
response_data_df = pd.DataFrame(response_data_decode)
response_submission_df = pd.DataFrame(response_submission_data)

# merge dataframes to get the ConfirmationID and the CreatedAt fields
merged_df = pd.merge(response_submission_df, response_data_df, left_on='submissionId', right_on='id')
