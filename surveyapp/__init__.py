"""
__init__.py initialises the server and database (sqlite3)
"""

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///library.db')

from surveyapp import models

try:
    Base.metadata.create_all(engine) # Creates database if not there already
except:
    print('Table already there.')

from surveyapp import modelcontrollers

modelcontrollers.CSVloader.get_users_csv()  # loads .csv files
modelcontrollers.CSVloader.get_course_csv()
modelcontrollers.CSVloader.get_enrolement_csv()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#used for session encryption
app.secret_key = 'Minjie'

import surveyapp.views

# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response