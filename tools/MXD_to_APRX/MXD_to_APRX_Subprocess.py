'''
-------------------------------------------------------------------------------
Title:       .MXD to .APRX File Worker Script
Authors:      Matt Graff, Jeremiah Podleski, Sophia Basanta
Created:     08/2023
File:        MXD_to_APRX_Worker.py

(c) 2023 Basemapping Team | Basemapping | GeoBC | MinWLRS
--------------------------------------------------------------------
# * SUMMARY
Converts each MXD into an APRX using the arc python.exe to create an environment 
that terminates hanging MXDs.

# - INPUTS:
Input parameters from the ArcPro GUI

# - OUTPUTS:
.APRX files for each .MXD file in user specified folder
--------------------------------------------------------------
'''
import arcpy
import sys
from pathlib import Path
import logging

# -- Import GeoBC Module
#sys.path.insert(0, r'\\spatialfiles.bcgov\WORK\ilmb\dss\dsswhse\Resources\Scripts\Python\Library')
# Append the path to where the geobc module is located.
_library_path = (r"\\spatialfiles.bcgov\WORK\ilmb\dss\dsswhse\Resources\Scripts\Python\Library")
sys.path.append(_library_path)
import geobc 
            
#cmd = [PRO_PYTHON, WORKER_SCRIPT, str(mxd_file), TEMPLATE_APRX, str(LOGFILE), str(bcgw_connection)]

# *** INPUT ARGUMENTS FROM CONTROLLER (ln 188) ***
mxd_file = Path(sys.argv[1])
template_aprx = sys.argv[2]
logfile = Path(sys.argv[3])
UNAME = sys.argv[4]
PWORD = sys.argv[5]
# bcgw_connection = sys.argv[4]

map_timeout_list = []
map_exists_list = []

# **** LOGGING ****
# Set up logging...(same logic as controller but creating a worker log)
logger = logging.getLogger("WORKER")
logger.setLevel(logging.DEBUG)

# remove inherited handlers (root)
for h in list(logger.handlers):
    logger.removeHandler(h)

file_handler = logging.FileHandler(logfile, mode="a", encoding="utf-8")
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s [%(name)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%b-%d %H:%M:%S"))

logger.addHandler(file_handler)
logger.propagate = False

# *** FUNCTIONS / CLASSES ***

def log(level, in_message):
        '''Write to console and the log file with one call..'''

        if level == 'debug':
                logger.debug(in_message)
                arcpy.AddMessage(in_message)
        elif level == 'warning':
                logger.warning(in_message)
                arcpy.AddWarning(in_message) 
        elif level == 'error':
                logger.error(in_message)
                arcpy.AddError(in_message) 

def main():
    # Starting messages
    log('debug', 'Starting new thread...')

    # Identify existing APRXs and skip associated MXDs
    aprx_file = mxd_file.with_suffix(".aprx")
    if aprx_file.exists():
        log("debug", f"APRX already exists. Skipping {aprx_file.name}")
        map_exists_list.append(aprx_file)
        return
    
    # Log into BCGW
    bcgw_object = geobc.BCGWConnection()
    create_success, my_connection_file = bcgw_object.create_bcgw_connection_file(
        UNAME, PWORD, output_location="T:", acdc="DC"
    )    
    # Attempt conversion of MXDs 
    try:
        # First, open the blank APRX so we can import the MXD into it
        aprx = arcpy.mp.ArcGISProject(template_aprx)

        # Import the MXD to the blank APRX file
        log("debug", f"importing mxd: {mxd_file.name}...")
        aprx.importDocument(str(mxd_file))
        
        # Save a copy of the APRX file, and done!
        log("debug", f">>>>>>>>>>>>> saving as {aprx_file.name}")
        aprx.saveACopy(str(aprx_file))

        # Notify the user if any errors occured - put info into log
        log("debug", ">>>>>>>>>>>>> Conversion complete...")
    except arcpy.ExecuteError:
        log("error", f"Failed to convert {mxd_file}")
        sys.exit(1)
    except Exception as e:
        log("error",f"An error occurred while converting {mxd_file}:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()