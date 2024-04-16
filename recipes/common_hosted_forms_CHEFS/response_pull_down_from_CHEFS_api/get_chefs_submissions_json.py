# --------------------------------------------------------------------------------------------------
# Author: Laurence Perry
# Ministry, Division, Branch: EMLI, MCAD, Regional Operations
# Updated: 2024-04-16
# Description:
#    A function to pull responses in JSON form from the Common Hosted Forms (CHEFS) API.
#    Note that a form ID and API token are required to access the API, this is demonstrated in the
#    read me in more detail.
# --------------------------------------------------------------------------------------------------
import requests
import base64

def get_chefs_submissions_json(form_id, api_token, version):
    """
    Returns the JSON response from the CHEFS API for the specified form ID, API token, and version.

    Args:
        form_id (str): The form ID. View read me for more information.
        api_token (str): The API token. View read me for more information.
        version (str): The version of the form.
    
    Returns:
        dict: The JSON response from the CHEFS API.
    """
    username_password = f'{form_id}:{api_token}'
    base64_encoded_credentials = base64.b64encode(username_password.encode("utf-8")).decode("utf-8")

    headers = {
        "Authorization": f"Basic {base64_encoded_credentials}"
    }
    url = f"https://submit.digital.gov.bc.ca/app/api/v1/forms/{form_id}/export"
    params = {
        "version": version,
        "format": "json",
        "type": "submissions",
    }

    response = requests.get(url, headers=headers, params=params)

    return response.json()