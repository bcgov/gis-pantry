## -------------------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
## This is how to access values stored in an environment file ((with a specified path))
## -------------------------------------------------------------------------------------------------

import dotenv
import someDB

# Put the credentials into a python dictionary...
CREDENTIALS_DICTIONARY = dotenv.dotenv_values(r"\\path\to\your\file...")

# Set your params...
DB_PASS = CREDENTIALS_DICTIONARY('DB_PASS')
DB_USER_NAME = CREDENTIALS_DICTIONARY('DB_USER_NAME')
DB_URL = CREDENTIALS_DICTIONARY('DB_URL')

# Use it...
database_connection = someDB.connect(DB_USER_NAME, DB_PASS, DB_URL)

## -------------------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
## Alternatively one can use dotenv to load them into system environment variables
# then use sys.argv[] to access them
## -------------------------------------------------------------------------------------------------

# Import the necessary module
from dotenv import load_dotenv
import os

# Load environment variables from the .env file (if present)
load_dotenv(r"\\path\to\your\file...")

# Access environment variables using os.getenv()
DB_PASS = os.getenv('DB_PASS')
DB_USER_NAME = os.getenv('DB_USER_NAME')
DB_URL = os.getenv('DB_URL')


# Example usage
database_connection = someDB.connect(DB_USER_NAME, DB_PASS, DB_URL)
