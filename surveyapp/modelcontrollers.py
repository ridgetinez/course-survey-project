from abc import abstractmethod, ABCMeta
from ast import literal_eval
import csv
from surveyapp import models, engine
from sqlalchemy.orm import sessionmaker

class CSVloader():
    def get_users_csv():
        with open("surveyapp/static/passwords.csv", newline='') as userfile:
            reader = csv.reader(userfile)
            for row in reader:
                UserController.write_user(row)

class UserController():
    def write_user(user_rep): # user_rep = [identifier, password, role]
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        new_user = models.User(uid=user_rep[0], password=user_rep[1], role=user_rep[2])
        session.add(new_user)
        try:
            session.commit()
        except:
            pass
        session.close()
    def check_password(user_name, password):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        user = session.query(models.User).filter(models.User.uid == user_name).first()
        if user.password == password:
            return True
        else:
            return False
