## -------------------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
## This is how to access values stored in an environment file ((with a specified path))
## -------------------------------------------------------------------------------------------------

import dotenv

# Put the credentials into a python dictionary...
CREDS = dotenv.dotenv_values(
    r"\\path\to\your\file...")

# Set your param...
CREDENTIAL_YOU_WANT = CREDS['NAME_OF_CREDENTIAL']

# Use it...
print(CREDENTIAL_YOU_WANT)

## -------------------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
## Alternatively one can use dotenv to load them into system environment variables
# then use sys.argv[] to access them
## -------------------------------------------------------------------------------------------------

# Import the necessary module
from dotenv import load_dotenv
import os

# Load environment variables from the .env file (if present)
load_dotenv(
    r"\\path\to\your\file..."
)

# Access environment variables using os.getenv()
SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

# Example usage
print(f'SECRET_KEY: {SECRET_KEY}')
print(f'DATABASE_URL: {DATABASE_URL}')
