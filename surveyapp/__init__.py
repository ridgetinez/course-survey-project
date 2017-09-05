from flask import Flask
from surveyapp.models import Admin
from surveyapp.auth import UserAuthenticator

app = Flask(__name__)

admin_list = [Admin("admin@admin.com", "password")]

authenticator = UserAuthenticator(admin_list)

app.secret_key = 'Minjie'

import surveyapp.views
