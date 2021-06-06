# GitHub Pages auto generation

Automatically searches through the `cool-stuff` directory and build a list of all the cool stuff that has been submitted. This script will be auto triggered by a github action when a new push is made to the `gh-pages` branch.

Note that the `gh-pages` branch is also managed by a github action and should be not be pushed to manually. Doing so will likely break the directory structure.