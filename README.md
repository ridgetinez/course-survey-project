# Contributing

We're going to adopt best practices for git. This pretty much means we'll be working on branches and merging them when we're done with our feature. For more information (and how to be a beast with git), read chapters 3 & 4 of [this git tutorial](https://www.learnenough.com/git-tutorial#sec-branching_and_merging).

We're going to the main MASTER branch, and then when you're working on - say, the SurveyController module and views - you'll branch out, and then merge back in when you've completed it.

WORKFLOW
========

1. Dev checks out to their own feature branch.
2. Commits changes to their feature branch.
3. Pushes to the remote branch.
4. Submits a pull request to merge back into master.
5. Team reviews and either suggests fixes or merges to master branch.
6. Dev is happy.


## Project Structure

 - run.py  
 - surveyapp/ 
    - \_\_init\_\_.py
    - models.py
    - views.py
    - static/
    - templates/

### What do these files/directories do?

__run.py__ - Starts the server

__\_\_init\_\_.py__ - Tells python that this directory is actually a python module

__views.py__ - Holds all of the url/route information

__models.py__ - Contain classes that act as data models

__static/__ - Contains static files eg. images, css

__templates/__ - Contains Jinja2 templates
