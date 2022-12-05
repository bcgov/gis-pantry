7 Hacks to Level Up your AGO Game - ESRI Developers Hate This! 😲<!-- omit in toc -->
===
|Supporting Docs for Nov 2022 GIS CoP Presentation|Prepared by: South Coast GIS Team|
|---|---|

- [Emoji and Icons in AGO Apps](#emoji-and-icons-in-ago-apps)

# Emoji and Icons in AGO Apps
<!-- no toc -->
  - [Got text? Add an emoji](#got-text-add-an-emoji)
    - [Are emoji accessible?](#sidenote-are-emoji-accessible)
  - [Custom icons in Dashboard](#custom-icons-in-dashboard)
    - [Can I use custom point symbols on a map?](#can-i-use-custom-point-symbols-on-a-map)

Icons (including emoji) provide more options for communicating information to your audience. They can be a quick visual aid to reinforce an idea presented in text, or a concise way to add additional meaning without words. 

---

## Got text? Add an emoji
Apologies to those who cringe immediately at the sign of an emoji. Good news for the irreverent - it is incredibly easy to incorporate emoji almost anywhere you have text in AGO. 

Here I used the construction symbol 🚧 to show pages that hadn't yet been developed:

![construction symbol](img/construction-emoji.png "🚧 used to show pages not yet developed")   

In most cases, using an emoji is as easy as typing - on Windows 10+, **simply press the Windows logo key <img src="img/windows-logo.png" width="15em"> + period (.)** to open the emoji panel, start typing a search term, and hit enter or click on the emoji you want. Or Google and copy and paste.

To add the emoji in the menu shown above, I just typed them in as the page title in Experience Builder, using the windows emoji panel:

![](img/emoji-EB.png)

Other fun (and potentially useful) spots to include emoji are in titles, chart legends, or indicators. Really the only limit is your creativity. Sometimes, emoji let us mimic symbols that might normally be added with JavaScript, like the ➕ on this tab label to show it can be expanded:

![plus menu](img/plus-tab.png "➕ next to the tab label to show it can be expanded")  

⚠ One important caution - emoji appearances [vary across platforms](https://thedavidbarton.github.io/blog/os-dependent-emoji-display/). Chances are it will still get the same message across, but the colour or general aesthetic could vary greatly.

---

### Are emoji accessible?
Yes, but only when used properly. Screen readers will read out the name of the emoji (e.g. "Fire", "Face with Tears of Joy", or "Thumbs Up Sign"). 

So what's the problem? Imagine how this would sound: 🍕🍕🍕😋🎉🎉🎉

This post on the [Easterseals blog](https://blog.easterseals.com/emojis-and-accessibility-the-dos-and-donts-of-including-emojis-in-texts-and-emails/) gives a few tips:
 - don't repeat emoji over and over
 - keep the total number of emoji limited
 - put the important information before the emoji so it's more likely to be heard (tough one for me)
---
## Custom icons in Dashboard
Esri gives the option to [add SVG icons](https://doc.arcgis.com/en/dashboards/latest/create-and-share/use-custom-icons.htm) in indicators, headers, selectors, and tables in Dashboards. For example, in this Dashboard header bar, I used custom icons to help the user to recognize the two groups of filters ('selectors' officially) - Area and Project:

![icon filters](img/icon-filters.png "Using icons in an AGO Dashboard selector to support text") 

Here, icons add style and clarity to the indicators:

![fish indicators](img/icon-indicator.png "Icons showing the subject of each indicator")  

Icon settings will be found somewhere in the element configuration. In the case of a Category selector go to Configure > Selector > Icon > Change > Custom

![custom icon](img/custom-icon.png "Custom icon settings")

Let's say I want to change the icon here to something else. Esri tells us "SVG icons are an XML-based vector image format and can be created in any text editor or using drawing software." And while you could technically type out an SVG in notepad - I'd suggest finding an existing SVG online.

Try a Google image search for '*your interest here* icon' or check out Google's [Material Symbols](https://fonts.google.com/icons) library. Take note of any image licensing. Once you've found an icon you like - I'll use this [crop icon](https://fonts.google.com/icons?selected=Material+Symbols+Outlined:crop:FILL@0;wght@400;GRAD@0;opsz@48) ![crop](img/crop.svg) - look around for a 'SVG download' button and save that file.

Then, open the file in your web browser, and right click > View page source to see the SVG code. It will look something like:

```
<svg xmlns="http://www.w3.org/2000/svg" height="48" width="48"><path d="M34.75 46v-8.25h-21.5q-1.2 0-2.1-.9-.9-.9-.9-2.1v-21.5H2v-3h8.25V2h3v32.75H46v3h-8.25V46Zm0-14.25v-18.5h-18.5v-3h18.5q1.2 0 2.1.9.9.9.9 2.1v18.5Z"/></svg>
```

Then simply copy all that and paste it into the SVG Code box in the element settings in Dashboard and tada - a new custom icon:

![](img/new-icon-indicator.png)  


---

### Can I use custom point symbols on a map?
Often the map is the star of the show, so naturally you'd want custom icons there. Sadly, the feature to do this online still hasn't made it from [Map Viewer Classic](https://www.esri.com/arcgis-blog/products/arcgis-online/mapping/using-images-as-custom-point-symbols/) into Map Viewer.

Esri has added [vector symbols](https://www.esri.com/arcgis-blog/products/arcgis-online/mapping/do-more-with-symbols-in-map-viewer-beta/) to Map Viewer and custom icons can be [exported as a Web Style](https://www.esri.com/arcgis-blog/products/arcgis-online/mapping/use-published-2d-symbols-in-arcgis-online/) from ArcGIS Pro. 

However, vector symbols come with this spooky warning:

![](img/symbol-warning.png)  

The [blog post](https://www.esri.com/arcgis-blog/products/arcgis-online/mapping/do-more-with-symbols-in-map-viewer-beta/) doesn't go into much depth, but these symbols work with the ArcGIS API for Javascript version 4.x, which includes Dashboards and Experience Builder. Notably, these symbols wont work with Web AppBuilder. 

In the new Map Viewer, there is a limited number of symbology folders to use, compared to the Classic Map Viewer:

![image](https://user-images.githubusercontent.com/10811420/205417560-b55468a3-05e6-425f-98dd-a2b5f1284955.png)

If you don’t want to start over building your map from scratch in classic and then resave it with the new map viewer (which seems to also save the old symbology), it is possible to access the symbols from the classic map viewer while retaining the functionality of the new map viewer. 

1.	In the GUI of a Classic Map Viewer-saved map, identify and save the symbology of the feature layer you’d like to use:
![image](https://user-images.githubusercontent.com/10811420/205417568-faeff5b8-32bc-492e-8329-a0ffff37a81d.png)
2.	In the new map viewer GUI, load in the feature layer of interest and use some random symbol from the new map viewer “Government” symbol selection folder on the symbology class of interest, save the map file.
3.	Open both the new map and the classic map JSON files.
4.	CTRL+F the symbology class for the value in question in the classic map JSON file, e.g., “Mule Deer”.
5.	Continue to search until you see some associated URL and ImageData tag for the value:
 ![image](https://user-images.githubusercontent.com/10811420/205417579-29051eda-d49f-404e-bb04-8352f684dbba.png)
6.	Copy only the “URL” and “ImageData” tags. 
7.	Search for the same symbology class, e.g., e.g., “Mule Deer”, in the new map viewer file and skip to the result which has classes for the symbol:
![image](https://user-images.githubusercontent.com/10811420/205417583-e660f91d-a446-4916-aea9-126791c372a6.png)
8.	Replace the identical tags in the new map viewer file with the URL and imageData tags and save the JSON file.
9.	Refresh the new map viewer GUI. Your symbol should be updated:
![image](https://user-images.githubusercontent.com/10811420/205417589-5af6c29f-6454-47fe-b7d3-352b4bb5b341.png)
11.	That’s it! Your new map will have the symbol replaced with one from the old catalog. You can also use this to replace it with custom public-hosted images.
12.	Tip: to replace with non-standard AGO web map images, upload your custom image to a public-facing image URL such as in GitHub, or as a public icon in AGO if you have administrative privileges. Then just copy and paste the URL, without regard to the imageData tag:
![image](https://user-images.githubusercontent.com/10811420/205417606-10a1789c-c0a8-4212-97bc-5b6f9a6f4008.png)

### Adding more than 5 widgets to an AGO web app

You can see there are six widgets in the app below:
 ![image](https://user-images.githubusercontent.com/10811420/205417508-f463cd01-b5e5-492f-834d-f41b291179dc.png)

How to add a sixth widget to a web app:

1.	Open the app in https://assistant.esri-ps.com/ and select JSON editor, then click on the ‘data’ tab. Make sure you’re signed into the account with appropriate permissions. 
2.	Click on the ‘Edit JSON’ button on the top-right.
3.	Ctrl+ F the term “Widgets/LayerList”. You need to make sure you are searching using the in-JSON search bar, not the generic browser search bar, else no results will be returned.
4.	Note the lines above the widget which state the position of the widget: 
a.	 ![image](https://user-images.githubusercontent.com/10811420/205417513-fd54c8a2-2a45-452d-aef3-1cc7159fa02e.png)
5.	Do this for all five widgets and copy the positions into a text document just in case.
6.	Copy the entire JSON snippet for one of your widgets. This should span from the curly bracket above the position argument, all the way down to the last curly bracket comma of that widget (i.e., “},”). You have to scroll very far. For this example, I scrolled through about 800 lines. If you are not sure where the curly bracket ends, you can also click the bracket, and it will highlight its match, which you can see once you scroll to it. 
a.	First bracket:  ![image](https://user-images.githubusercontent.com/10811420/205417518-1f24a649-9402-45c8-aae7-2b52171fa7c3.png)

b.	Last bracket:  ![image](https://user-images.githubusercontent.com/10811420/205417523-379cb4f3-528c-45f6-970f-05ca7bf8acd4.png)
 
7.	Paste below the widget you just copied right under the last curly bracket (i.e., right after you see the last “},” right after where the red circle is on the screenshot above).  Now you have an exact copy of an existing widget with all of its layers and configurations as a sixth widget.
8.	Calculate the new position for your sixth widget. 
a.	If you want the sixth layer widget at the top, I find the following “top” positions for each widget to place it work well:
i.	12 for new layer, and  162, 112, 212, 265 for each existing grouped widget, respectively.
ii.	Else, use custom position numbers based on the positions you noted earlier. This may require fiddling with, saving, visualizing on the app, and refining the position number.
9.	Upload a new icon for your widget by uploading it to your content tab (New Item -> Your Device) and setting its sharing to public.
10.	Copy the URL at the bottom right of the item details page, and paste into the “icon” parameter in the JSON. 
a.	Ex: https://bcgov03.maps.arcgis.com/sharing/rest/content/items/7eab8ccb9a50490c9d776bd4646b63aa/data
b.	 ![image](https://user-images.githubusercontent.com/10811420/205417533-0e3bba91-5474-48c6-a65a-5ce68067cf6d.png)


11.	Save the JSON and voila! You can now resume editing this widget on your regular app editor and remove and add the necessary layers.
