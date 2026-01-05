#------------------------------------------------------
# Purpose: Extracts data from CHEFS (Common Hosted Forms) api and converts it to a pandas dataframe. Optionally, download attachments
#
# Requirements: (1) CHEFS form ID
#               (2) CHEFS version ID
#
# Author: Emma Armitage
#
# Last Updated: 2026-01-05
#------------------------------------------------------

import requests
import pandas as pd
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

FORM_ID = ''                                            # CHEFS form ID (string)
API_KEY = ''                                            # CHEFS API key (string)
BASE_URL = "https://submit.digital.gov.bc.ca"           # CHEFS base URL (string)
CHEFS_HIDDEN_FIELDS = []                                # list of hidden field names to include in the data extraction (list of strings)

# create a session object to persist certain parameters across requests
session = requests.Session()
session.auth = (FORM_ID, API_KEY)
# timeout settings for requests (connect timeout, read timeout)
TIMEOUT = (5, 60)

def chefs_api_request(base_url, resource_path, form_id, endpoint, params=None):
    """
    Makes a GET request to the CHEFS API.

    Returns: the JSON response if the request is successful, otherwise logs an error and exits.

    base_url: the base URL for the CHEFS API
    resource_path: the resource path for the CHEFS API e.g. "app/api/v1/forms"
    form_id: the CHEFS form ID
    endpoint: the api endpoint to be accessed e.g. "version", "submissions"
    params: optional dictionary of query parameters to include in the request (in this case, used to specify fields to be returned)
    """

    url = f"{base_url}/{resource_path}/{form_id}/{endpoint}"

    r = session.get(url, params=params, timeout=TIMEOUT)

    if r.status_code == 200:
        logging.info(f"Request to {endpoint} successful")
        return r.json()
    else:
        logging.error(f"Failed to fetch {url}: {r.status_code} - {r.text}")
        sys.exit()

def get_data_from_chefs(BASE_URL, FORM_ID):
    """
    Fetches CHEFS form data from the published version and returns a pandas DataFrame.

    BASE_URL: the base URL for the CHEFS API
    FORM_ID: the CHEFS form ID
    """
    logging.info("Fetching the published version ID of the CHEFS form")
    version_data = chefs_api_request(base_url=BASE_URL, 
                                     resource_path="app/api/v1/forms",
                                     endpoint="version", 
                                     form_id=FORM_ID)
    
    # extract version ID from the response
    version_id = version_data['versions'][0]['id']
    logging.info(f"Published version ID: {version_id}")

    logging.info("Fetching the published version ID of the CHEFS form")
    field_name_data = chefs_api_request(base_url=BASE_URL,
                                        resource_path="app/api/v1/forms",
                                        endpoint=f"versions/{version_id}/fields",
                                        form_id=FORM_ID)
    
    # add hidden fields to the list of field names as they are not returned by the API
    if CHEFS_HIDDEN_FIELDS:
        for hidden_field in CHEFS_HIDDEN_FIELDS:
            field_name_data.append(hidden_field)
    # format the field names into a comma-separated string
    chefs_fields = ",".join(field_name_data)

    logging.info("Fetching CHEFS submissions")
    chefs_data = chefs_api_request(base_url=BASE_URL,
                                   resource_path="app/api/v1/forms",
                                   endpoint="submissions",
                                   form_id=FORM_ID,
                                   params={"fields": chefs_fields})
    
    # convert json reponse to dataframe
    chefs_df = pd.json_normalize(chefs_data)
    # remove deleted submissions from the dataframe
    chefs_df = chefs_df[chefs_df['deleted'] == False]

    return chefs_df

def download_attachments(df, photo_field_name, base_url, save_path):
    """
    Downloads attachments from CHEFS submissions.

    df: pandas DataFrame containing CHEFS submissions
    photo_field_name: the name of the field in the DataFrame that contains the attachment info
    base_url: the base URL for the CHEFS API
    save_path: the directory where downloaded attachments will be saved. Defaults to the current working directory
    """

    file_submission_list = df[photo_field_name].to_list()

    # iterate through each submission
    for submission in file_submission_list:
        if submission:
            # iterate through each file in the submission
            for file in submission:
                # get file URL and original name from CHEFS submission
                file_url = file['url']
                photo_name = file['originalName']
                # construct the download URL for the CHEFS API
                download_url = f"{base_url}/{file_url}"
                # directory where the photo will be saved 
                if save_path is None:
                    save_path_full = photo_name
                else:
                    save_path_full = f"{save_path}/{photo_name}"
                logging.info(f"Downloading photo: {photo_name}")
                try:
                    with session.get(url=download_url, stream=True, timeout=TIMEOUT) as response:
                        response.raise_for_status()
                        # download the file
                        with open(save_path_full, 'wb') as out_file:
                            # download the file in 1MB chunks
                            for chunk in response.iter_content(chunk_size=1024 * 1024):
                                if chunk:
                                    out_file.write(chunk)
                except requests.exceptions.HTTPError as e:
                    status = e.response.status_code if e.response is not None else "no-response"
                    logging.error(f"HTTP error downloading {photo_name} ({status}): {e.response.text}")
                except requests.exceptions.RequestException as e:
                    logging.error(f"Network error downloading {photo_name}: {e}")

chefs_df = get_data_from_chefs(BASE_URL, FORM_ID)
download_attachments(df=chefs_df, 
                     photo_field_name="",           # name of the field containing attachment info (string)
                     base_url=BASE_URL, 
                     save_path=None)                # directory to save attachments (string). If None, saves to current working directory