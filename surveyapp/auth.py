from flask import session

class UserAuthenticator(object):

    """ contains methods for authenticating users

    Args:
    user_list -- list of admin users
    """

    def __init__(self):
        """
        tmp_users = {}
        #initialises dict of admins with emails as key
        for user in user_list:
            tmp_users[user.getEmail()] = user
        self._users_dict = tmp_users
        """

    #attempts to authenticate a user when provided with email and password
    def authenticate(self, email, password):
        try:
            user = self._users_dict[email]
        except KeyError:
            #flag the user as a non-admin
            self.provideAdminSession(False)
            return False
        if user.checkPassword(password):
            #flag the user as an admin
            self.provideAdminSession(True)
            return True
        else:
            #flag the user as a non-admin
            self.provideAdminSession(False)
            return False

    #flags the user as either an admin or a non-admin dependent on boolean
    def provideAdminSession(self, boolean):
        session["admin_flag"] = boolean

    #checks if a user has been authenticated
    def checkAuthenticated(self):
        try:
            if session["admin_flag"] == True:
                return True
            else:
                return False
        except KeyError:
            return False
