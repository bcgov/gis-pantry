


# GeoBC PYTHON ENVIRONMENTS

If you are curious about Python environments at GeoBC, or have reached a point where want to change or modify the environment that your scripts run within, then this document should help you get started.

## Index
* [Python Environments](#python-environments)
* [General Info](#general-info)
* [GeoBC Development Context](#geobc-development-context)
* [Your Environment Options](#your-environment-options)
* [Deciding Where to Develop -- The Environment "Decision Tree"](#deciding-where-to-develop----the-environment-decision-tree)

## Python Environments
### General Info
Python development environments are complex. In a nutshell all languages run within environments, and lines of code wouldn't mean much to a computer without them. Environments are the reason a computer knows where to find a block by name. Environments have a lot to do with OS and system Path variables and where underlying blocks of code are stored. An environment contains the path variables, executables, scripts, and code libraries that make a language work within a particular environment context.

 ### GeoBC Development Context
 In general, if you are developing scripts for your work with GeoBC you will do this in one of two places:
1. The GTS Citrix environment (recommended)
2. On your local machine (when necessary)

Most of the time you will likely be developing for one of the following applications: QGIS, ESRI desktop GIS (ArcPro, ArcGIS Desktop), or ArcGIS Online. 

 ### Your Environment Options
 The main questions to ask are <ins>what</ins> do you want to do and <ins>where</ins> should you do it (meaning platform and environment). The <ins>what</ins> will guide the <ins>where</ins>.
 
 Below is a "decision tree" of sorts to help you...

## Deciding Where to Develop -- The Environment "Decision Tree"
Scan the bulleted "Decision Tree" list below for an entry that sounds like what you want to do. Each entry provides you with your environment options along with some helpful information to get started.  

***Last Update: Mid 2023. Keep in mind that things change as the platform changes. Please update this section with new information. Much appreciated!***

### You want to...

* **Develop a script on GTS that calls ArcPy**
	* For this, use the GeoBC central clone environment (this is the environment we should use most of the time, for most things)
		* *Notes:*
			* You need to point ArcPro to this environment using drive letter mapping. Like this:
				* P:\corp\<current clone directory>
			* You need to point VS Code using UNC. Like this:
				* \\GISWHSE.ENV.GOV.BC.CA\whse_np\corp\<current clone directory>

	* IF you need to **<a name="AddPackageLink">install additional packages:</a>**

		* **OPTION 1 -** Add them directly to GeoBC central clone
			* You can do this yourself within the ArcPro package manager as long as the packages you want are available.
				* See [Package Manager](https://pro.arcgis.com/en/pro-app/latest/arcpy/get-started/what-is-conda.htm) help docs.
			* If you need to use Pip then - ***Work with Zach/Scott***
			* Afterwards, continue your development using the central clone

		* **OPTION 2 -** Create your own clone environment and add to it as needed (Advanced)<a name = "make-your-own-clone"></a>
			
			*For instance, you may want to test packages or otherwise develop within an environment that you are allowed to change at will (as well as to break without affecting other users). Maybe the additional packages are not easy to install to the clone, or you don't want to bother IT staff at this time to modify the environment as needed, etc...*

			*FYI: You may encounter some issues (mentioned below), also clones eat disk space - 1.6GB minimum...*

			* The easiest way to make a clone is to use the ArcPro [Package Manager](https://pro.arcgis.com/en/pro-app/latest/arcpy/get-started/clone-an-environment.htm)
			* OR create the clone using the "Python Command Line" terminal 
				* You can launch this from the windows start menu. It is standard with ArcPro installations 
				* See: [Cloning an Environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#cloning-an-environment) in the Conda help docs.
				* If you want to specify the location use ```--prefix``` in the call like this
				 ```$ conda create --prefix=myclone --clone myenv```
			  
			* *Notes:*
				* **You can either:**
					1. Save the clone to your user profile
						* You will be able to use such clones within ArcPro by activating it in the ArcPro Package Manager. See [Package Manager](https://pro.arcgis.com/en/pro-app/latest/arcpy/get-started/what-is-conda.htm) help docs.
						* VS Code will not work (because at time of writing VS requires UNC, but your user profile is at C:).
						* 15-20 minutes to create (in our tests)
					1. Save the clone at a LAN location
						* ArcPro may not work with clones located on the LAN. Some of our tests failed.
						* VS Code used LAN based clones just fine as long as you point to them with UNC
						* 15-20 minutes to create (in our tests)

* **Develop a script on GTS that <ins>does not call ArcPy</ins> (Python Executable also possible)**	
	* **OPTION 1:** You can still use the GeoBC central clone environment - just don't call ArcPy. 
		* However, if you need to add additional libraries then the steps listed [above](#AddPackageLink) apply here as well.
		* If you want to create a python executable...
			* Use pyinstaller or auto-py-to-exe (already installed in the central clone).
			* *Notes:*
				* If pyinstaller and auto-py-to-exe are not installed then contact I.T.
				* You cannot have IE set as the default browser - *Set your default to Edge*
				* For more information see [Python Executables HOW TO](./GeoBC_Python_Executables_HOW-TO.md)

	* **OPTION 2:** Alternatively, use the "GTS Python environment" (coming soon!) to create a virtual environment.
		* *Notes:*
			* You can develop in your IDE of choice
			* You can modify your virtual environment without affecting anyone else.
			* The environment is lightweight, compact, and quick to create
		* If you want to create a python executable...
			* Install exe creation tools into the environment to make the exe
			* Create your EXE
			* For more information see [Python Executable HOW-TO](./Python_Executables_HOW-TO)

* **Make an Executable that Calls Arcpy?**
	* Sorry, not Possible - ArcPy cannot run from within an exe. Arcpy expects to run in the ESRI conda environment and throws an error when run from within an exe.

* **You want to develop on your local machine (various reasons)**
	* Sometimes it is necessary to develop using one's local machine. In this case you will:
		* Install the Python version (or versions) of your choice to your local machine
		* Optionally, create a virtual environment to work within.
			* Use the built-in module venv (alternatives to venv also exist)
		* Add packages and modify your environment as desired
		* Develop your code within this environment
		* If you want to create an exe:
			* Add exe creation tools to your environment (e.g. auto-py-to-exe)
			* Create your exe
		* *Notes:* 
			* If you develop on your local machine, then it's a good idea to store your code on network a location.
				* You can do this by developing with a working copy on your local machine, but maintain an official copy at a network location that others can access.
---
### FYI: Using venv to make a lightweight environment from the ESRI conda environment in GTS that can call arcpy... 
I'm including this hack in case it is useful to someone...  
Thanks to Kevin Netherton for this approach, though he admits it is “hacky”, and has limitations. 

There is a way to create a lightweight virtual environment from the ESRI environments using venv, and then force the correct paths into place when a script runs using the archook module. Your script must import archook to do this. The archook module is essentially going out to find the paths ArcPy needs to run, and then appending them into the sys.path variable. You have to call archook before arcpy, so that needed paths are then available to arcpy. 

This approach allows your script to import libraries from the larger ESRI python environment, while also being able to import libraries you’ve installed in a virtual environment. You will not be able to make an executable if the code calls arcpy.

***For more information see:***
<https://gist.github.com/franTarkenton/b8a9a3809de9e180735f3bae08f03e1d>
<https://github.com/franTarkenton/archook>