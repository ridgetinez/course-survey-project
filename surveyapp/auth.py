class UserAuthenticator(object):
    def __init__(self, user_list):
        tmp_users = {}
        for user in user_list:
            tmp_users[user.getEmail()] = user
        self._users_dict = tmp_users
    def authenticate(email, password):
        password_for_email = self._users_dict[email]
        if password == password_for_email:
            return True
        else:
            return False        
