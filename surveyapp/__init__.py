"""
__init__.py tells server that the directory is a python module
"""

from flask import Flask
from surveyapp.models import Admin

app = Flask(__name__)

#used for session encryption
app.secret_key = 'Minjie'

import surveyapp.views
