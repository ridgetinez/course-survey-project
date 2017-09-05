from flask import session

class UserAuthenticator(object):
    
    """ contains methods for authenticating users

    Args:
    user_list -- list of admin users
    """
    
    def __init__(self, user_list):
        tmp_users = {}
        for user in user_list:
            tmp_users[user.getEmail()] = user
        self._users_dict = tmp_users

    def authenticate(self, email, password):
        try:
            user = self._users_dict[email]
        except KeyError:
            self.provideAdminSession(False)
            return False
        if user.checkPassword(password):
            self.provideAdminSession(True)
            return True
        else:
            self.provideAdminSession(False)
            return False        

    def provideAdminSession(self, boolean):
        session["admin_flag"] = boolean

    def checkAuthenticated(self):
        try:
            if session["admin_flag"] == True:
                return True
            else:
                return False
        except KeyError:
            return False
