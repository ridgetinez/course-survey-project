from flask import session, redirect, url_for
from surveyapp import models
import sqlite3

class UserAuthoriser(object):

    """ contains methods for authorising users
    """
    #flags the user as either an admin or a non-admin dependent on boolean
    def provideUserSession(user):
        session["user"] = user.as_dict()

    def check_permission(user_type_allowed, user_id):
        try:
            user_type = session["user"]["type"]
            print('type: ' +user_type)
        except KeyError:
            print("Key Error when parsing user data from session")
            return False
        if user_type == user_type_allowed:
            print("{} {}".format(session["user"]["identifier"], user_id))
            if user_type == "student" or user_type == "staff":
                if session["user"]["identifier"] != user_id:
                    return False
            return True
        else:
            return False

class AuthController(object):

    """ controller for authentication
    """
    def _user_type_to_query(user_type):
        if user_type == "staff":
            return "STAFF"
        elif user_type == "student":
            return "STUDENTS"
        elif user_type == "admin":
            return "ADMINS"
        print("ERROR: INVALID USER TYPE")

    def login(user_type, identifier, password):
        userdata = AuthController.get_userdata_from_db(user_type, identifier)
        print(userdata)
        if not userdata:
            return False
        if password != userdata[1]:
            return False
        #auth for different users
        if user_type == "student":
            user = models.Student(identifier, password, [])
            UserAuthoriser.provideUserSession(user)
        elif user_type == "staff":
            user = models.Staff(identifier, password, [])
            UserAuthoriser.provideUserSession(user)
        elif user_type == "admin":
            user = models.Admin(identifier, password)
            UserAuthoriser.provideUserSession(user)
        return True

    def get_userdata_from_db(user_type, identifier):
        connection = sqlite3.connect('surveyapp/users.db')
        cursor = connection.cursor()
        query = "SELECT * FROM {} where id=\"{}\"".format(AuthController._user_type_to_query(user_type), identifier)
        print(query)
        cursor.execute(query)
        result = cursor.fetchone()
        connection.commit()
        cursor.close()
        return result

    def logout():
        session["user"].pop
