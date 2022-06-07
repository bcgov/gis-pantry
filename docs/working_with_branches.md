# Working with branches

Branches are an integral feature of version control using Git and fundamental to everyday development processes, whether in a collaborative context or otherwise. You can read more about [how branches work](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell) but this requires some understand of how Git actually works... 

Here's what you need to know (from [here](https://www.toolsqa.com/git/branch-in-git/)):
> a branch in Git is a way to keep developing and coding a new feature or modification to the software and still not affecting the main part of the project. 

Neat, huh? Read on to learn how to set one up.

# Making new branches

These steps pertain to VS Code and assume you already have a repo initialized. For help with that, check out [this intro to GitHub](Using-GitHub.md).

## Making a new branch:
  -   in VS Code, CTRL+SHIFT+P to open Command Palette
  -   Type / select: `Git: Checkout to...`
  -   Select: `Create new branch from... `
  -   Provide a new branch name, including origin branch (in my case, `alg`, but could be `main` or `master`) and adding reference to the new feature (my new branch: `alg-addoutputs`)
  -   Select a reference to create the branch from (in my case, I want this branch to come off the previous `alg` branch and to compare against the remote `alg` branch which I had committed and pushed earlier that day)
  -   The new branch name is now shown in the bottom left as your active branch
  -   For now this branch is local only, but once you publish (CTRL+SHIFT+P type/select `Git: Publish` OR click little cloud upload button next to your branch name) it will also be visible on the GitHub page for the repo
 ## Working on the branch
  -   Go ahead saving and adding commits to the new branch. Sync/push when appropriate.
  -   You can switch over to another branch at any time by clicking the active branch name (bottom left) or using `Git: Checkout`
  -   What is cool about switching branches is the local files will actually change. In my case (developing a QGIS processing script), if I change branches and then refresh available scripts in QGIS, the active branch version will show up in QGIS, since this is actually what is stored in the local file.
 ## Merging with the origin branch
  -   New branches are displayed loud and clear on the GH repo page.
  -   To merge a branch, click 'Compare & pull request' to start preparing a pull request
  -   --> Right up top, you will probably want to change the branch that your new branch is being compared against to the branch you made your new one off of (`alg` in my case)
      -   GH seems to default to comparing against `main`
  -   Scroll down for a neat comparison of all the changes to your code
