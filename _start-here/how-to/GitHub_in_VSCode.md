# Using GitHub in VS Code (GTS)
> How to interact with your GitHub repositories directly in VSCode in GTS

**Further Reading:**  
If you want more information about using Git and GitHub in VS Code, please see [Introduction to Git in VS Code](https://code.visualstudio.com/docs/sourcecontrol/intro-to-git) and [Working with GitHub in VS Code](https://code.visualstudio.com/docs/sourcecontrol/github#_setting-up-a-repository)  

**Prerequisites:** 
* GIT (already available in GTS) 
* Visual Studio Code (already available in GTS)
* GitHub account ready for use. If not please see [GitHub Account Set UP](./GitHub_Account_Set_Up).

## Introduction
> Since Git and Visual Studio Code are available in our Geospatial Terminal Servers (GTS) we can peform common Git actions like pushing and pulling code, creating and merging branches, and committing code changes right within the VS Code editor. 

## Workflow Outline
### Getting Started with GitHub in VSCode:
* [Open a GitHub repository remotely](#open-a-github-repository-remotely)
    1. Install the GitHub Repositories extension
    1. Use the 'Open Remote Repository' command
    1. Select the GitHub repository that you want to open

* [Clone an existing repository to a local folder](#clone-an-existing-repository-to-a-local-folder)
    1. Use the 'Clone Repository' command
    1. Select repository from GitHub that you want to clone
    1. Select a local folder to clone the repository to

* [Create a new repository from a local folder](#create-a-new-repository-from-a-local-folder)
    1. Open folder in VS Code
    1. Use the 'Publish to GitHub' command
    1. Publish to GitHub

### Using Source Control in VS Code:
* [Staging and committing code changes](#staging-and-committing-code-changes)
* [Pushing and pulling remote changes](#pushing-and-pulling-remote-changes)
* [Using branches](#using-branches)

## Getting Started with GitHub in VSCode
### Open a GitHub repository remotely
<ol>
  <li><p>Install the GitHub Repositories extension</p>
  <img src=../_media/GitHub_VSCode_Repositories_Extension.PNG>
  <p>Use the Extensions window and search for "GitHub Repositories" to locate the extension to install (notice the blue check mark verifying github.com as the publisher of this extension).</p>
  </li>
  <br>
  <li><p>Use the 'Open Remote Repository' command</p>
  <img src=../_media/GitHub_VSCode_OpenRemoteRepository.PNG><img src=_media/GitHub_VSCode_OpenRemoteRepository2.PNG>
  <p>You should now have an Open Remote Repository option in your Explorer window. Click this button to be prompted to open a GitHub repository.</p>
  <p>You will now be prompted to sign in using GitHub, opening a web browser which will prompt you to enter your GitHub username and password.</p>
  </li>
  <br>
  <li><p>Select the GitHub repository that you want to open</p>
  <img src=../_media/GitHub_VSCode_OpenRemoteRepository_Select.PNG>
  <p>You will be given a list of repositories to open remotely, select the one you want to open.</p>
  <img src=../_media/GitHub_VSCode_OpenRemoteRepository_Opened.PNG>
  <p>You will now be able to make changes to your repository in GitHub remotely using VS Code.</p>
  </li>
</ol>

---
### Clone an existing repository to a local folder
<ol>
  <li><p>Use the 'Clone Repository' command</p>
  <img src=../_media/GitHub_VSCode_CloneRepo.PNG><img src=_media/GitHub_VSCode_CloneRepo2.PNG>
  <p>From the Explorer window click the Clone Repository button.</p>
  </li>
  <br>
  <li><p>Select repository from GitHub that you want to clone</p>
  <p>You will now be prompted to sign in using GitHub, opening a web browser which will prompt you to enter your GitHub username and password.</p>
  <img src=../_media/GitHub_VSCode_CloneRepo3.PNG>
  <p>Select the repository you want to clone from the list of available GitHub repositories.</p>
  </li>
  <br>
  <li><p>Select a local folder to clone the repository to</p>
  <p>You will now be prompted to to select a folder to save the clone to locally.</p>
  <img src=../_media/GitHub_VSCode_Cloning.PNG>
  <p>Once the folder is selected VS Code will start cloning the repository to your local folder</p>
  <img src=../_media/GitHub_VSCode_OpenClone.PNG>
  <img src=../_media/GitHub_VSCode_OpenRemoteRepository_Opened.PNG>
  <p>Once completed you will be given the option to open the local clone, and can then start working off of the clone in VS Code.</p>
  </li>
</ol>

---
### Create a new repository from a local folder
<ol>
  <li><p>Open folder in VS Code</p>
  <img src=../_media/GitHub_VSCode_LocalFolder.PNG>
  <p>Open the folder that you want to make a new GitHub repository out of in VS Code.</p>
  </li>
  <br>
  <li><p>Use the 'Publish to GitHub' command</p>
  <img src=../_media/GitHub_VSCode_Publish.PNG>
  <p>Open the Source Control window and you should now have a Publish to GitHub option. Click this button to be prompted to publish a new GitHub repository.</p>
  <p>You will now be prompted to sign in using GitHub, opening a web browser which will prompt you to enter your GitHub username and password.</p>
  <img src=../_media/GitHub_VSCode_Publish2.PNG>
  <p>You'll be given the option to publish to a private or public repository on GitHub.</p>
  <img src=../_media/GitHub_VSCode_Publish3.PNG>
  <p>You'll also be given the option of what files from your folder to include in the repository.</p>
  </li>
  <br>
  <li><p>Publish to GitHub</p>
  <img src=../_media/GitHub_VSCode_Publish_Message.PNG><img src=../_media/GitHub_VSCode_Publish_Message2.PNG>
  <p>VS Code will now start to publish your new repository to GitHub and will give you a prompt when it's done.</p>
  <img src=../_media/GitHub_VSCode_Publish_SourceControl.PNG>
  <p>Once complete you will now see new options in the Source Control window to interact with your repository in GitHub.</p>
  <img src=../_media/GitHub_VSCode_Publish_GitHub.PNG>
  <p>If you enter GitHub via your browser you will also now be able to see and interact with your new repository.</p>
  </li>
</ol>

---
## Using Source Control in VS Code
> Once you've connected VS Code to a GitHub repository using one of the methods above, you will now have access to Source Control capabilities in the Source Control window.  

### Staging and committing code changes
<p>As soon as you've made a change to a repository file in VS Code you'll notice that the Source Control icon will have numbers/notifications on it, indicating changes.</p>
<img src=../_media/GitHub_VSCode_Source_Changes.PNG>
<p>Once you open the Source Control window you'll also see a list of files with changes.</p>
<img src=../_media/GitHub_VSCode_Source_Changes2.PNG>
<p>You can click on the file to open a comparison window to see where the changes are line-by-line.</p>
<p>You now have the option to either discard the changes made locally, or to stage the changes, ready to be committed to the repository.</p>
<img src=../_media/GitHub_VSCode_Source_StagedChanges.PNG>
<p>Once staged, you'll see the changes move up into the Staged Changes list, indicating that it will be included in the next commit.</p>
---

### Pushing and pulling remote changes
<img src=../_media/GitHub_VSCode_Source_StagedChanges.PNG>
<p>Once staged, you'll see the changes move up into the Staged Changes list. You'll now need to enter a commit message in the box above and are ready to commit and push the changes.</p>
<img src=../_media/GitHub_VSCode_Source_PushPull.PNG>
<p>The More Actions button (denoted by the three dots) also allows you to select from various git actions. You can also sync remote changes to your local copy of the repository using these actions.</p>
---

### Using branches
<img src=../_media/GitHub_VSCode_Source_Changes.PNG>
<p>You also have the option to use branches other than the main/master branch.</p>
<p>Clicking on the branch name (defaults to master*) next to your repository under Source Control Repositories in the Source Control window will allow you to change branches or create a new branch.</p>
<img src=../_media/GitHub_VSCode_Source_Branches.PNG>
<p>Select an existing branch from the list or click Create a new branch to make a new branch.</p>
<img src=../_media/GitHub_VSCode_Source_Branches2.PNG>
<p>Once you've selected a branch to use VS Code will load that branch and you'll see in the Source Control window that the branch name next to your repository under Source Control Repositories has changed .</p>
<img src=../_media/GitHub_VSCode_Source_Branches3.PNG>
<p>If you are using a branch, the branch name will also be indicated in the bottom left of your VS Code window.</p>
---
