

[home](../readme.md)

[QGIS Plugin repository](https://plugins.qgis.org/)

# Introduction
To enhance a software’s capabilities, the add-on functions need to be activated or downloaded. We call it plugins. As other GIS software, QGIS also have many plugins at your disposal. There are a list of plugins ready to be installed. 

# Installation 
TO install some of plugins, all you need to do are going into plugin menu option and select “Manage and Install Plugins…” and then search for the plugin that you need for your tasks. The installation is just a button away.
![](https://github.com/bcgovjz/gis-pantry/blob/master/docs/getting-started-with-QGIS/images/pluginInstall.gif)

# Uninstallation
Uninstallation is also easy, beside “install” button, there is a button called “Uninstall Plugin”.
![](https://github.com/bcgovjz/gis-pantry/blob/master/docs/getting-started-with-QGIS/images/pluginunInstall.gif)

# Other Options
On the left of the plugin window, you can see different options to filter the plugin list, such as “Installed” or “Not installed”. In another case if you have a plugin that is not published and not listed in the all plugin list, you are also able to install plugin from a .zip files. Last but not least, you can update the plugin settings under the "Settings" section. For example to to allow more functionality, such as allow experimental plugins to show on the plugin list. 
![](https://github.com/bcgovjz/gis-pantry/blob/master/docs/getting-started-with-QGIS/images/pluginIntro.gif)

# Build Your Own Plugins 
If you are more advanced in QGIS and would like to build your own plugins. There is one way you can achieve that. Under Plugins>>Settings, check the box of “Show also experimental plugins”. And then go back to “All”, search for Plugin Builder 3, install this plugin. 
![](https://github.com/bcgovjz/gis-pantry/blob/master/docs/getting-started-with-QGIS/images/pluginbuilder.gif)

After we have Plugin Builder 3 activated, you can see it under “Plugins” from the main menu. From here you can follow the steps and create your own plugins.
![](https://github.com/bcgovjz/gis-pantry/blob/master/docs/getting-started-with-QGIS/images/pluginbuilderopen.gif)

For the first and sceond page inside Plugin Builder dialog, some information need to be entered. Here is an example.
![](https://github.com/bcgovjz/gis-pantry/blob/master/docs/getting-started-with-QGIS/images/pluginbuilder1.png)
![](https://github.com/bcgovjz/gis-pantry/blob/master/docs/getting-started-with-QGIS/images/pluginbuilder2.png)

On the thrid page, you have the options to choose the style of your widgets. You can choose accroding to your needs.
![](https://github.com/bcgovjz/gis-pantry/blob/master/docs/getting-started-with-QGIS/images/pluginbuilderopendialogoption.gif)

Then keep the fourth and fifth page as it is or update the information as you need. The next part we need to point the tool to the correct plugin folder on your computer. Sometime you are not able to AppData folder, it is hidden as defult. You can turn it on in file explorer
![](https://github.com/bcgovjz/gis-pantry/blob/master/docs/getting-started-with-QGIS/images/pluginbuilder5.png)

After clicking on the "Generate" button, a new folder will appearing inside your plugin folder you pointed to earilier.  
![](https://github.com/bcgovjz/gis-pantry/blob/master/docs/getting-started-with-QGIS/images/pluginbuilderopendialogcreation.gif)

Inside the new plugin folder, there will be already established file structures.
![](https://github.com/bcgovjz/gis-pantry/blob/master/docs/getting-started-with-QGIS/images/pluginfolder.PNG)

Now there a new folder created in the plugins folder and it contains all the main elements of a plugin need. Next steps its to add functionality to the new plugin. Here are the steps to add functionalities to your plugins.
1. Open the .ui file inside Qt Designer. Create a interface layout that will work for your plugin. 
2. Add python codes with functionality inside xxxx_dialog.py
3. Activate and reload plugin inside QGIS.

And you are ready to start using your custom made plugin.

