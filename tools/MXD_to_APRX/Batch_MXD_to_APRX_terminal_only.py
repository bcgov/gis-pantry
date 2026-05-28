
'''
-------------------------------------------------------------------------------
Title:       Batch MXD to APRX
Author:      Matt Graff, Jeremiah Podleski
Created:     08/2023

(c) 2023 Basemapping Team | Basemapping | GeoBC | MinWLRS
--------------------------------------------------------------------
# * SUMMARY

Creates an APRX file for each MXD found within the input directory structure (incl. subfolders)
Uses the name of the MXD for the new APRX

Creates a log file to record the status of each conversion, including items skipped and why.

The script will skip MXD's if their matching APRX already exists, OR if the process
timeout is reached.

# - INPUTS:
Input directory to search for .MXD files

# - OUTPUTS:
.APRX files for each .MXD file in user specified folder
A log file within the target directory called: mxd_to_aprx

--------------------------------------------------------------
# * POSSIBLE IMPROVEMENTS

*! Make this a Pro tool

* add ability to y/n to subfolder searching (not just archive/index)

-------------------------------------------------------------------------------
# * HISTORY

     Date   Initial/IDIR  Description
| -------------------------------------------------------------------------------
  2023-08-18    MGraff    Cleaned up code and added comments / documentation
  2023-11-15    jpodlesk  added better logging, cleaned up comments,
                          re-organized to improve ease of use, tested more thoroughly, 
                          and improved code. Deleted the blank map that was showing up 
                          from the template, skip and report maps that exist, etc...
  2023-12-27    jpodlesk  much faster file skipping for files already converted
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
'''

# *** IMPORTS ***
import arcpy
import os
from pathlib import Path
import sys
import multiprocessing
import logging

# *** SCRIPT PARAMETERS ***
DEC = '=+'*50

# *** ENVIRONMENTS ***

arcpy.env.overwriteOutput = True


# -- Import GeoBC Module
# sys.path.insert(0, r'\\GISWHSE.ENV.GOV.BC.CA\whse_np\corp\python3916\python.exe')
# Append the path to where the geobc module is located.
_library_path = (
    r"\\spatialfiles.bcgov\work\ilmb\dss\dsswhse\Resources\Scripts\Python\Library"
)
sys.path.append(_library_path)
import geobc

# *** PARAMETERS ***

# - USER PARAMETERS
#! Update these params for each run
TARGET_DIRECTORY = Path(
r'\\spatialfiles.bcgov\ilmb\dss\projects\Mmah\Administrative_Boundaries_Project\Thompson_Nicola_Regional_District\__projects__'
)
TIMEOUT = 300 # seconds - script reports map name and moves on if it takes longer than timeout
EXCLUDE = set(['__archive__','archive', 'index', '__archive__']) # list of folders to exclude -- ENTER ALL LOWER CASE

# - STATIC PARAMETERS
TEMPLATE_APRX = r'\\spatialfiles.bcgov\ilmb\vic\geobc\Workarea\jpodlesk\_MySCRIPTING_\MXD_to_APRX\temp.aprx'
map_timeout_list = []
map_exists_list = []

# **** LOGGING ****
# Log to terminal and a file...
logging.basicConfig(
    level=logging.DEBUG,
    encoding='utf-8',
    format="%(name)s: %(asctime)s [%(levelname)s] %(message)s",
    datefmt='%Y-%b-%d %H:%M:%S',
    #handlers=[logging.FileHandler("debug.log", mode='w'), logging.StreamHandler(sys.stdout)],
    handlers=[logging.FileHandler(f'{TARGET_DIRECTORY}\mxd_to_aprx.log', mode='a')],
)
logger = logging.getLogger('LOG')

# debug statement for the terminal
print('\nstarting new thread...')

# *** FUNCTIONS / CLASSES ***

def log(level, in_message):
    '''Simple function to make writing to console and the log file easy with one call..'''

    if level == 'debug':
        arcpy.AddMessage(in_message)
        logger.debug(in_message)
    elif level == 'warning':
        arcpy.AddWarning(in_message) 
        logger.warning(in_message)
    elif level == 'error':
        arcpy.AddError(in_message) 
        logger.error(in_message)

def convert_mxd_to_aprx(mxd_file):
    '''function to convert an mxd to aprx file...'''
    # -- Log into BCGW
    # Required or importDocument() will not work. Basically, this is how credentials are
    # made available to the mxd we are importing... with this arcpy is logged in... 
    # Without this, the importDocument() function will just hang... No error, no nothing... 

    uname = "sfreelan" 
    pword = "GeoBC99!"
    bcgw_object = geobc.BCGWConnection()
    create_success, my_connection_file = bcgw_object.create_bcgw_connection_file(
        uname, pword, output_location="T:", acdc="DC"
    )

    try:
        # First, open the blank APRX so we can import the MXD in it
        aprx = arcpy.mp.ArcGISProject(TEMPLATE_APRX)
        
        # Create the output filename of the new APRX
        in_file = str(mxd_file)
        aprx_file = Path(in_file.replace('.mxd','.aprx'))

        # Make a new aprx if one doesn't exist. Else: skip, report, and move on...
        if not aprx_file.exists():
            # Import the MXD to the blank APRX file
            log('debug', f'importing mxd: {mxd_file.name}...')
            aprx.importDocument(mxd_file)
            
            # Save a copy of the APRX file, and done!
            log('debug', f'>>>>>>>>>>>>> saving as {aprx_file.name}')
            aprx.saveACopy(aprx_file)
            
            # Notify the user if any errors occured - put info into log
            log('debug',f'>>>>>>>>>>>>> Conversion complete...')
        else:
            log('debug', f'APRX already exists. Skipping {aprx_file.name}')
            map_exists_list.append(aprx_file)

    except arcpy.ExecuteError:
        log('error',f'Failed to convert {mxd_file}')
    except Exception as e:
        log('error',f'An error occurred while converting {mxd_file}:\n{e}')
        return False

    return True

def main():
    '''
    find mxd's in target directory
    call mxd to aprx function using multithreading to allow a timeout on maps that hang
    '''

    log('debug', f'{DEC}\nStarting conversionsions...\n{DEC}')
    # Walk through the TARGET_DIRECTORY in order (topdown parameter)
    for folder_path, subfolders, filenames in os.walk(TARGET_DIRECTORY, topdown=True):
        
        # If user specifies ignore directories, remove them.
        [subfolders.remove(sf) for sf in list(subfolders) if sf.lower() in EXCLUDE]
            
        #check if file has .mxd extension
        for file in filenames:
            if file.endswith('.mxd'):
                
                # Get the mxd_file path so we can pass it into the convert_mxd_to_aprx
                mxd_file = Path(f'{folder_path}\\{file}')

                # check to see if the file exists. If so report. If not convert it!
                existing_file_check = mxd_file.with_suffix('.aprx')
                
                if existing_file_check.exists():
                    print(f'skipping {mxd_file.name} ... It already has a matching aprx.')
                    map_exists_list.append(mxd_file.name)

                else:

                    # Define and start map conversion process, and join a timeout...
                    p = multiprocessing.Process(target=convert_mxd_to_aprx, args=(mxd_file,)) #Leave comma in parameter call!
                    p.start()
                    p.join(timeout=TIMEOUT)
                    
                    # If main process is still running, report error, end it, carry on to next...
                    if p.is_alive():
                        log('warning',f"Timeout occurred while converting {mxd_file.name}. Skipping...")
                        map_timeout_list.append(mxd_file)
                        p.terminate()

# *** MAIN ***
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log('error', e)
    finally:
        log('debug', '+=+=+=+=+= finished conversionsions! +=+=+=+=+=')

        # Print the maps that were skipped for whatever reason...
        # Maps that timed out...
        if len(map_timeout_list) > 0:
            log('The following maps timed-out...')
            for i in map_timeout_list:
                log('debug',i)
            log(DEC)
        else:
            log('debug','No timeout warnings...')
        # Maps that already existed by name...
        if len(map_exists_list) > 0:
            log('The Following maps were skipped because they already exit...')
            for i in map_exists_list:
                log('debug',i)
            log(DEC)
        else:
            log('debug','No skipped maps...')
