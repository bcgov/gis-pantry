# MXD to APRX Tool
## Description
Scripts and tool that will batch convert mxds to aprxs.
This is an easy way to convert a lot of mxds to aprxs. It handles BCGW layers as well as standard layers.


The tool will recursively search the subdirectories in the target directory. You can also exclude specific subfolders.

Batch_MXD_to_APRX_terminal_only.py is a standalone script that will run from terminal. It uses multithreading instead of subprocess. MXD_To_APRX_Tool.py and MXD_to_APRX_Subprocess.py work with the tool found in MXD_TO_APRX.atbx.

### Inputs
Target folder path: Location where mxd files are.  
Timeout: Time limit for converting an individual map before skipping.  
Exclude Folder List: Semicolon separated list of folder names (case insensitive).  
BCGW User  
BCGW Password

### Outputs
One or more aprx files named the same as the mxds.

### Requirements 
Arcpro 3.4 or above is required to run the script tool.  
BCGW access.

### Production Folder Location
Q:\dsswhse\Resources\Scripts\Tools_ArcPro\General\MXD_to_APRX
