# Author: Jeremiah Podleski
# Ministry, Division, Branch: FIT (Foundational Information and Technology) - GeoBC Atlas Unit
# Created Date: 2025-05-08
# ------------------------------------------------------------------------------
# SUMMARY

# Useful Logging Template
# Use this to set up logging for scripts as desired
# Copy, paste, modify, GO...

# This set up logs to the terminal, to a .log file, and to a special filtered .log file. 
# It also has a function defined that makes most log calls as simple as a print statement

# It's also possible to set up logging using config files. 
# This provides an easy way to set up logging without having to put the configuration
# within each script using code. 
# If I create a config file in the future, then I will add it along with sample code to use it...

# USEFUL REFERENCES
# https://docs.python.org/3/library/logging.html#formatter-objects
# https://realpython.com/python-logging/
# 

# REQUIREMENTS // INPUTS / OUTPUTS // NOTES
# You need to define an output location for the .log file(s)

# ------------------------------------------------------------------------------
# FUTURE IMPROVEMENTS

# Create a logging .conf file and sample code that shows how to use it... (in separate files)

# ------------------------------------------------------------------------------
# HISTORY
# using project level Git...
# ------------------------------------------------------------------------------

# ** IMPORTS

from pathlib import Path
import logging

# ** LOGGING

script_dir = Path(__file__).parent # root directory of this script

# define filters (optional)...
class Filter_01(logging.Filter):
    def filter(self, record):
        # Filter logic goes here
        # For example, let's filter out records with a certain attribute
        return hasattr(record, 'my_attribute')

# Setup logger...
logger_name = "Logger.main" if __name__ == "__main__" else f"{__name__}.main"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG) # this logger will handle all messages at this level or above...
logger.handlers.clear() # clear previous handlers... Avoids message repetition from multiple handlers...
logger.propagate = False # stop messages from getting propogated up to root logger... optional

# set formatters...
# # # logFormatter = logging.Formatter("%(asctime)s %(name)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
# file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_formatter = logging.Formatter('{asctime} - {name} - {levelname} - {message}', style='{')
console_formatter = logging.Formatter("{message}", style='{')

# set and add handlers...
log_file_path = script_dir / f'{Path(__file__).stem}.log' # use script name
fileHandler = logging.FileHandler(log_file_path, mode='a') # w = overwrite a = append
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(file_formatter)
logger.addHandler(fileHandler)

log_file_path = script_dir / f'{Path(__file__).stem}_filtered.log' # use script name
fileHandler_filtered = logging.FileHandler(log_file_path, mode='a') # w = overwrite a = append
fileHandler_filtered.setLevel(logging.DEBUG)
fileHandler_filtered.setFormatter(file_formatter)
fileHandler_filtered.addFilter(Filter_01()) # Add filter to limit what goes in this log...
logger.addHandler(fileHandler_filtered)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO) # terminal will not print debug
consoleHandler.setFormatter(console_formatter)
logger.addHandler(consoleHandler)

# ** FUNCTIONS

def log(msg:str, level=logging.INFO):
    '''make logging easy!'''
    logger.log(level, msg)

# ** EXAMPLE USAGE
# These examples take advantage of the setup above...

print('\n+_+') # use print() for things you don't need/want the logger to handle...

# log messages using the logger... 
log('hello world (DEBUG)', logging.DEBUG) # this will only go to the log file
log('hello world (default - aka:INFO)') # no need for 2nd arg if we are leaving this will be INFO level
log('hello world (WARNING)', logging.WARNING)
log('hello world (ERROR)', logging.ERROR)
log('Hello world (CRITICAL)', logging.CRITICAL)

# log a message that will also get filtered into the special log file...
# the filter can filter in a myriad of ways... this one uses a user defined attribute
logger.info('This is a debug message filtered using my_attribute', extra={'my_attribute': True})
