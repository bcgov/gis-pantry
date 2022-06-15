# Working with branches

You're working on a fix to bug #104, while Suzette is trying to build a shiny new user interface. If you were both pushing commits to the same place, the commit history would get awfully confusing with high potential for conflicts.

Enter branches. Branches are an integral feature of version control using Git and fundamental to everyday development processes, whether in a collaborative context or otherwise. You can read more about [how branches work](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell) but this requires some understand of how Git actually works... 

Here's what you need to know (from [here](https://www.toolsqa.com/git/branch-in-git/)):
> a branch in Git is a way to keep developing and coding a new feature or modification to the software and still not affecting the main part of the project. 

Neat, huh? Read on to learn how to set one up and then merge it back in with the rest of your project.

These steps pertain to VS Code and GitHub and assume you already have a repo initialized. For help with that, check out [this intro to GitHub](Using-GitHub.md). Chances are good there are much faster and slicker ways to complete this process with Git Bash, but this process is user-friendly for the novice.

## Making a new branch:
The first step to using branches is to make one!
  -   in VS Code, `CTRL+SHIFT+P` to open the Command Palette
  -   Type / select: `Git: Checkout to...`
  -   Select: `Create new branch from... `
  -   Provide a new branch name, including origin branch (in my case, `alg`, but could be `main` or `master`) and adding reference to the new feature (my new branch: `alg-addoutputs`)
  -   Select a reference to create the branch from (in my case, I want this branch to come off the previous `alg` branch and to compare against the remote `alg` branch which I had committed and pushed earlier that day)
  -   The new branch name is now shown in the bottom left as your active branch
  -   For now this branch is local only, but once you publish (CTRL+SHIFT+P type/select `Git: Publish` OR click little cloud upload button next to your branch name) it will also be visible on the GitHub page for the repo

## Working on the branch
  -   Go ahead saving and adding commits to the new branch. Sync/push when appropriate (ie frequently if collaborating on the same branch).
  -   You can switch over to (`checkout`) another branch at any time by clicking the active branch name (bottom left) or using `Git: Checkout`
  -   What is cool about switching branches is the local files will actually change. In my case (developing a QGIS processing script), if I change branches and then refresh available scripts in QGIS, the active branch version will show up in QGIS, since this is actually what is stored in the local file.

## Pull requests: sending your work back to the origin branch
The following steps pertain to create pull requests on GitHub, but no doubt you could do this in VS Code or with terminal commands.
  -   Head to the Branches page for your repo on GitHub: ![image](https://user-images.githubusercontent.com/38586679/173863596-cb38eb6e-fd6d-449e-881c-9c43a81fbb0e.png)
  -   To merge a branch, click `New pull request`
  -   Use the drop down up top to set the base branch that your new branch is being compared against and merged into (`alg` in my case)
> **_NOTE:_** GH defaults to comparing against `main` - be sure to select your origin branch
  -   Scroll down for a neat comparison of all the changes to your code - if you set the wrong base branch, that should now be obvious.
  -   Add title and description as needed, and hit `Create pull request` to send off your submission

## Merging
  - Following the instructions above, you will now be on the page of your new Pull Request. If you're not a project collabortor, kick back ⛱ - your work is done.
  - Project collaborators (which might include you) can now review your pull request and merge it with the origin branch. You can also request a review to get feedback on your code.
  - Git will provide an indication if there are any merge conflicts. If you're lucky, you'll see this:
![image](https://user-images.githubusercontent.com/38586679/173869358-034e36a8-b4a7-4e3b-a66f-08468a9c29ba.png)
      - In the case of any conflicts, GH offers a simple code editor which will display both sets of code for any conflicting areas.
  - Once conflicts are resolved hit `Merge pull request`
  - Back in VS Code, you can checkout the newly updated origin branch, sync, and see your merged changed in place.

## Cleanup
  - Finally, you can delete the branch you were working on, since it is likely no longer needed. GH makes this convenient:
![image](https://user-images.githubusercontent.com/38586679/173870964-475a0753-2d40-48ce-a1cc-8ec7c4f98cd4.png)
  - You will still have a local copy of this branch! Keep your local environment tidy by deleting it, unfortunately not currently possible in VS Code (as of 2022-06-15). A quick git command will take care of it:
      - Open your repo location in Windows File Explorer, right click and `Git Bash Here` (or you may be able to use powershell terminal in VS Code but I get a `'git' is not recognized` error)
      - Enter `git branch -d <branch-name>` to delete the local branch. You may need to use `-D` to force if you receive an error.
      - Give VS Code a second and your deleted branch will no longer be listed
  - Time to make a new branch, rinse and repeat!
