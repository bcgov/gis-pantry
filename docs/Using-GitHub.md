# Using Git Hub to Contribute to GIS Pantry

## Create a Git Hub Account

Sign up for a GitHub account at <https://github.com/>

- In your seetings it is a good idea to set up 2 factor authentication. This provides an extra level of security for your account. Once logged into your account this can be found under settings and account security.

-It is also useful to have GitHub desktop on your computer to transition Push and Pull requests from code edited on your computer to updating the fork on GitHub.

## Setting up and working with the Repository

1. Log into your GitHub Account

2. Navigate to the repository you want to contribute to <https://github.com/bcgov/gis-pantry>

3. In the upper right click on Fork. This will create a copy of the Repo under your name.

4. You should have a copy under your name called. (Your username/GIS-Pantry)

5. When you are in the forked copy this is called "Master" the main Repository it was created from would be called the "Upstream/Master"

Forking GitHub Repository
![Fork GitHub Repository](./getting-started-with-QGIS/images/Fork_GitHub_Repository.gif)

## Making edits to the repository

NOTE BEFORE EDITING: Always do a fetch on bcgov/gis-pantry before pushing your own changes. Git fetch checks for any changes. If there are changes then git pull is needed to get those changes synced. See git fetch vs git pull. This can be done by adding a remote to point to bcgov/gis-pantry. The reason for this is if another user has made a pull request since the you forked and cloned copy was made it will create a merge conflict because your copy will be out of sync with bcgov/gis-pantry. 

Using MS Visual Studio Code or GitHub for desktop should have this functionality built in. The main thing to remember is that the update on the remote bcgov/gis-pantry will integrate into your local copy before making push and pull requests to your forked version.

### Option 1: Make edits directly on GitHub

1. Navigate to the page you want to edit

2. Click on the pencil in the top right corner  

3. Edit the document (note the edit file and Preview tab are handy for checking your markdown syntax)

4. Scroll to the bottom Add a short description as to what your updating and click commit changes. This will commit changes to your Master Fork.

5. Repeat editing files until you are done a milestone that you feel needs to go back to the source "Upstream/Master" repository

6. See below regarding creating a pull request to the "Upstream/Master"  

Edit Fork on GitHub
![Edit GitHub Repository](./getting-started-with-QGIS/images/Edit_On_GitHub_Repository.gif)

### Option 2: Download the Repo to your computer and edit

1. Clone to your local directory - This can be done many ways either using something like Microsoft Visual Studio code, GitHub for Desktop, or even git command line.

2. Make edits to files, folder structure, add/delete files 

3. Push your changes back to github (your repository) when you feel you have accomplished something. This could be a few times a day. 

4. Repeat until you are done a milestone you feel needs to go back to the source repository 


## Creating Pull request to update Upstream Master with Forked copy.

1.



