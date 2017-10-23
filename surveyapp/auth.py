"""
auth.py contains a UserAuthoriser and an AuthController to handle the login for into the survey app
"""

from flask import session, redirect, url_for
from surveyapp import modelcontrollers
import sqlite3

class UserAuthoriser(object):

    """ contains methods for authorising users
    """
    #flags the user as either an admin or a non-admin dependent on boolean
    def provideUserSession(user_dict):
        session["user"] = user_dict

    def check_permission(user_type_allowed, user_id):
        try:
            user_type = session["user"]["role"]
        except KeyError:
            print("Key Error when parsing user data from session")
            return False
        if user_type == user_type_allowed:
            if user_type == "student" or user_type == "staff" or user_type == 'guest':
                if session["user"]["identifier"] != user_id:
                    return False
            return True
        else:
            return False


class AuthController(object):

    """ controller for authentication
    """
    def login(user_type, identifier, password):
        password_correct = modelcontrollers.UserController.check_password(identifier, password)

        if password_correct == False:
            return False

        UserAuthoriser.provideUserSession({'identifier' : identifier, 'role' : user_type})
        return True

    def logout():
        session["user"].pop
