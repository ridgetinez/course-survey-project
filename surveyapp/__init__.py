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

#used for session encryption
app.secret_key = 'Minjie'

import surveyapp.views
