class Admin(object):
    """ Question object to populate question pools and surveys
    
    Args:
    email -- Admin's email
    password   -- Admin's password
    """
        
    uaID = 0
        
    def __init__(self, email, password):
        self.__email = email
        self.__password = password
        self.__aID = Admin.uaID
        Admin.uaID += 1
    
    def __eq__(self, other):
        return self.__email == other.__email
        
    def __hash__(self):
        return hash(self.__aID)
    
    def __str__(self):
        return '{0} : {1}'.format(self.__aID, self.__email)

    #getter function for admin id
    def getAdminID(self):
        return self.__aID

    #getter function for admin email
    def getEmail(self):
        return self.__email

    #checks if password matches admin's password
    def checkPassword(self, password):
        if password == self.__password:
            return True
        else:
            return False

