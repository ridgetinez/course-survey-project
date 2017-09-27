from flask import Flask
from surveyapp.models import Admin
from surveyapp.auth import UserAuthenticator

app = Flask(__name__)

#contains all of the admin login credentials
#admin_list = [Admin("admin@admin.com", "password")]

#authenticator object used to authenticate users
authenticator = UserAuthenticator()

#used for session encryption
app.secret_key = 'Minjie'

import surveyapp.views
