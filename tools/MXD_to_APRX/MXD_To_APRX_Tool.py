'''
-------------------------------------------------------------------------------
Title:       .MXD to .APRX File Tool
Author:      Matt Graff, Jeremiah Podleski, Sophia Basanta
Created:     08/2023
File:        MXD_to_APRX_Tool.py

(c) 2023 Basemapping Team | Basemapping | GeoBC | MinWLRS
--------------------------------------------------------------------
# * SUMMARY

Creates an APRX file for each MXD found within the input directory structure (including subfolders)
Uses the name of the MXD for the new APRX

Creates a log file to record the status of each conversion, including if an item was skipped and why.

The script will skip MXD's if their matching APRX already exists, OR if the process
timeout is reached.

# - INPUTS:
Input directory to search for .MXD files

# - OUTPUTS:
.APRX files for each .MXD file in user specified folder
A log file within the target directory called: mxd_to_aprx

--------------------------------------------------------------
# * POSSIBLE IMPROVEMENTS

* add flag to disable recursive subfolder searching (not just archive/index)
* find a way to use without importing bcgw every process?
    *We have tried multiple methods and have failed

* Add terminal input of BCGW credentials

-------------------------------------------------------------------------------
# * HISTORY

     Date   Initial/IDIR  Description
| -------------------------------------------------------------------------------
  2023-08-18    MGraff    Cleaned up code and added comments / documentation
  2023-11-15    jpodlesk  added better logging, cleaned up comments,
                          re-organized to improve ease of use, tested more thoroughly, 
                          and improved code. Deleted the blank map that was showing up 
                          from the template, skip and report maps that exist, etc...
  2026-04-28    sbasanta  Rewrote the script in arcpy tool formatting, switching from the
                          multiprocessing module to the subprocess module, including 
                          arc-specific formatting (e.g. rewriting key variables as parameters and including messaging 
                          configuration). Improved a handful of lines re pathway config.
                          Each MXD is now converted individually within the subprocess module 
                          using the python.exe interpreter and terminates any hanging MXDs.  
  2026-05-28    slester   Created swecond script to work with tool ui using subprocess
                          and finished tool interface. Added it to GIS pantry, initialized git                        
-------------------------------------------------------------------------------
'''

# *** IMPORTS ***
import arcpy
import os
import sys
from pathlib import Path
import subprocess
import logging

# *** ENVIRONMENTS ***

arcpy.env.overwriteOutput = True


# *** STATIC PARAMETERS ***
TEMPLATE_APRX = (r"\\spatialfiles.bcgov\WORK\ilmb\dss\dsswhse\Resources\Scripts\Tools_ArcPro\General\MXD_to_APRX\temp.aprx")
CENTRAL_PY = (r"P:\corp\central_clones\python_geospatial\python.exe")
WORKER_SCRIPT = (r"\\spatialfiles.bcgov\WORK\ilmb\dss\dsswhse\Resources\Scripts\Tools_ArcPro\General\MXD_to_APRX\MXD_to_APRX_Subprocess.py")

# Can launch script from terminal or atbx
'''
# | - LAUNCHER
# Where are we launching the tool from (terminal or script tool)
if len(arcpy.GetParameterAsText(0)) > 0:
     we are running from the script tool... Use parameters set in the tool UI...
    logger.log(
        "WARN",
        "\nRunning from tool environment...\n")
    RUN_FROM_TERMINAL = False
    RUN_FROM_TOOL = True # Use the Tool UI...
else:
    # We are running from terminal...
    # Use hard-coded parameters. Code + Data in DEV ENV. ((Overrides TOOL_DEV))
    arcpy.AddMessage(
        "\nWe are running from terminal. Tool UI ignored...\n"
        )
    RUN_FROM_TERMINAL = True 
    RUN_FROM_TOOL = False # Use the Tool UI...
'''

# *** SCRIPT PARAMETERS ***
DEC = '=+'*50

# *** PARAMETERS ***
'''
if RUN_FROM_TOOL:
'''    
TARGET_DIRECTORY = Path(arcpy.GetParameterAsText("target_directory"))
TIMEOUT = int(arcpy.GetParameterAsText("timeout"))
EXCLUDE__LIST = [x.strip().lower() for x in (arcpy.GetParameterAsText("exclude") or "").split(";")]

UNAME = arcpy.GetParameterAsText("uname")
PWORD = arcpy.GetParameterAsText("pword")
'''
else:
    TARGET_DIRECTORY = Path(r"")
    TIMEOUT = 
    EXCLUDE__LIST = [""]

    UNAME = ""
    PWORD = ""
'''    
# **** LOGGING ****
# Set up logging... (reconfigured to avoid duplicate messaging)
LOGFILE = TARGET_DIRECTORY / "mxd_to_aprx.log" # easier pathway config to log file
logger = logging.getLogger("CONTROLLER") # creates logger named "CONTROLLER"
logger.setLevel(logging.DEBUG) # set minimum severity level


# reporting varibles
map_timeout_list = []
map_exists_list = []



for h in list(logger.handlers): #remove all handlers currently attached to this logger (e.g. ArcPro handlers)
    logger.removeHandler(h)

# Create the handler, and set the format
file_handler = logging.FileHandler(LOGFILE, mode="a", encoding="utf-8")
file_handler.setFormatter(logging.Formatter(
    "%(asctime)s [%(name)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%b-%d %H:%M:%S"))

logger.addHandler(file_handler) # attach the file handler to "CONTROLLER" logger
logger.propagate = False # prevent log from flowing up to root logger


# *** FUNCTIONS / CLASSES ***

def log(level, in_message):
        '''Write to ArcPro and the log file with one call..'''

        if level == 'debug':
                logger.debug(in_message)
                arcpy.AddMessage(in_message)
        elif level == 'warning':
                logger.warning(in_message)
                arcpy.AddWarning(in_message) 
        elif level == 'error':
                logger.error(in_message)
                arcpy.AddError(in_message) 
        elif level == 'info':
                logger.info(in_message)
                arcpy.AddMessage(in_message) 


def main():
    '''
    find mxd's in target directory
    call mxd to aprx subprocess using python.exe to terminate maps that hang once they exceed the timeout
    '''

    # Log starting conversions
    log('info', f'{DEC}\nStarting conversions...\n{DEC}')
    
    # Walk through the TARGET_DIRECTORY in order (topdown parameter)
    for folder_path, subfolders, filenames in os.walk(TARGET_DIRECTORY, topdown=True):
        
        # If user specifies ignore directories, remove them.
        [subfolders.remove(sf) for sf in list(subfolders) if sf.lower() in EXCLUDE__LIST]

        # Skip files that are not MXDs
        for file in filenames:
            if not file.lower().endswith(".mxd"):
                continue

            # Get the mxd_file path so we can pass it into the worker subprocess
            mxd_file = Path(folder_path) / file

            # If APRX already exists, skip that MXD
            aprx = mxd_file.with_suffix(".aprx")
            if aprx.exists():
                map_exists_list.append(mxd_file)
                log("debug", f"Skipping existing APRX: {aprx.name}")
                 
                continue
            
            # Log start of first MXD conversion
            log("info", f"Launching worker for {mxd_file.name}")

           
            # 1. Launch the external process in the background
            # ------------------------------------------------
            # Convert each MXD in their own subprocess inside a separate Python environment
            # subprocess.Popen to execute external subprocess and open a pipe to their inputs/outputs
            
            # Command-line arguments that will be passed to subprocess
            cmd = [CENTRAL_PY, WORKER_SCRIPT, str(mxd_file), TEMPLATE_APRX, str(LOGFILE), UNAME, PWORD]
            proc = subprocess.Popen(
                    cmd,
                    stdin=subprocess.DEVNULL, # disconnect the child process from the terminal's keyboard input
                    stdout=subprocess.PIPE, # do not hold output messages in memory (avoid redundancy)
                    stderr=subprocess.PIPE, # hold error messages in memory
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW, # do not shoe command-line window pop-up
                )
            
            try:
                    # waits for the child python.exe process to finish, collects messages and adds to log file
                    #! this is also where we add the timeout
                    stdout, stderr = proc.communicate(timeout=TIMEOUT)
                    # add output messages to log
                    if stdout:
                        for line in stdout.splitlines():
                            arcpy.AddMessage(line)
                    if stderr:
                        for line in stderr.splitlines():
                            log("error", f"[{mxd_file.name}] {line}")
                    # if the MXD conversion produces an error (value > 0), log
                    if proc.returncode != 0:
                        log("error", f"Worker failed for {mxd_file.name} (exit code {proc.returncode})")
                   # otherwise, log completed
                    else:
                        log("debug", f"Completed {mxd_file.name}")
            # kill the subprocess if conversion time > TIMEOUT
            except subprocess.TimeoutExpired:
                    proc.kill()
                    log("warning",f"Timeout occurred while converting {mxd_file.name} (> {TIMEOUT}s). Skipping...")
                    map_timeout_list.append(mxd_file.name)

            finally: 
                  continue


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log('error', e)
    finally:
        log('debug', f'{DEC}\nFinished conversions!\n{DEC}')

        # Print the maps that were skipped for whatever reason...
        # Maps that timed out...
        if len(map_timeout_list) > 0:
            log('debug','The following maps timed-out...')
            for i in map_timeout_list:
                log('debug',i)
            log('debug',DEC)
        else:
            log('debug','No timeout warnings...')
        # Maps that already existed by name...
        if len(map_exists_list) > 0:
            log('debug','The following maps were skipped because they already exist...')
            for i in map_exists_list:
                log('debug',i)
            log('debug',DEC)
        else:
            log('debug', 'No skipped maps...')
