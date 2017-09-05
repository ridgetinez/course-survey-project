class UserAuthenticator(object):
		
	def __init__(self, user_list):
		tmp_users = {}
		for user in user_list:
			tmp_users[user.getEmail()] = user
		self._users_dict = tmp_users

	def authenticate(email, password):
		user = self._users_dict[email]
		if user.checkPassword(password):
			return True
		else:
			return False


	def provideAdminSession():
		session["admin_flag"] = True
