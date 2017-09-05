from flask import Flask
app = Flask(__name__)

session["admin_flag"] = false

import surveyapp.views
