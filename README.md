# Contributing

We're going to adopt best practices for git. This pretty much means we'll be working on branches and merging them when we're done with our feature. 

We're going to the main MASTER branch. When we work on a different section we'll branch out, and then merge back in when completed it.

WORKFLOW
========

1. Dev checks out to their own feature branch.
2. Commits changes to their feature branch.
3. Pushes to the remote branch.
4. Submits a pull request to merge back into master.
5. Team reviews and either suggests fixes or merges to master branch.
6. Coders note any changes/tasks completed in tasks logs
7. Documenter notes these changes in all documentation (UML Diagrams, Task Logs, Charts, etc.)
8. Dev is happy.


## Project Structure

 - run.py  
 - surveyapp/ 
    - \_\_init\_\_.py
    - auth.py
    - controller.py
    - models.py
    - readers.py
    - tests.py
    - views.py
    - writers.py
    - static/
    - templates/

### What do these files/directories do?

__run.py__ - Starts the server



__\_\_init\_\_.py__ - Tells server that the directory is a python module

__auth.py__ - Contains classes to handle the login/authentication/security for the survey app

__controller.py__ - holds surveyController which contains methods to display the survey to respondents

__models.py__ - Uses sqlalchemy to implement database for survey objects

__readers.py__ - Reads data from .csv files 

__tests.py__ - Contains test data for iteration 3

__views.py__ - Contains the general workflow of the survey system including routing to different webpages

__writers.py__ - Uses sqlalchemy to write into .csv files and databases


__static/__ - Contains static files (most IMPORTANTLY our .csv files!)

__templates/__ - Contains Jinja2 templates (front-end application user interface)
