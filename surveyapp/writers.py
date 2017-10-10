"""
writers.py uses sqlalchemy to write into .csv files and databases
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from abc import ABCMeta, abstractmethod
from models import User, Course, Enrolment, Base
import csv

DATABASE_URL = 'sqlite:///survey.db'

class TableConnector(metaclass=ABCMeta):

    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        try:
            Base.metadata.create_all(bind=self.engine)
        except:
            print("Tables already created! SHITS LIT.")
        self.DBSession = sessionmaker(bind=self.engine)

class TableLoader(TableConnector):

    def __init__(self, *args):
        super(TableLoader, self).__init__()

    def add_row(self, obj):
        session = self.DBSession()
        session.add(obj)
        session.commit()

    @abstractmethod
    def csv_to_db(self, csv_name):
        pass

class UserLoader(TableLoader):

    def __init__(self):
        super(UserLoader, self).__init__()

    def csv_to_db(self, csv_name):
        session = self.DBSession()
        with open(csv_name, newline='') as f:
            user_reader = csv.reader(f, delimiter=',', quotechar='|')
            for uid, password, role in user_reader:
                if (session.query(User.id).filter(User.id == uid).first() is None):
                    new_user = User(id=uid, password=password, role=role)
                    self.add_row(new_user)
        session.close()

    def get_all(self):
        session = self.DBSession()
        q = session.query(User)
        for user in q.all():
            print(user.id, user.password, user.role)
        session.close()


class CourseLoader(TableLoader):

    def __init__(self):
        super(CourseLoader, self).__init__()

    def csv_to_db(self, csv_name):
        session = self.DBSession()
        with open(csv_name, newline='') as f:
            course_reader = csv.reader(f, delimiter=',', quotechar='|')
            for course, sem in course_reader:
                if (session.query(Course.id).filter(Course.name == course and Course.session == sem).first() is None):
                    new_course = Course(name=course, session=sem)
                    self.add_row(new_course)
        session.close()




class EnrolmentLoader(TableLoader):

    def __init__(self):
        super(EnrolmentLoader, self).__init__()

    def csv_to_db(self, csv_name):
        session = self.DBSession()
        with open(csv_name, newline='') as f:
            enrolment_reader = csv.reader(f, delimiter=',', quotechar='|')
            for uid, course, sem in enrolment_reader:
                c = session.query(Course.id).filter(Course.name == course and Course.session == sem).one()
                if (session.query(Enrolment).filter(Enrolment.cid != c[0] and Enrolment.uid == uid).first() is None):
                    # cid = session.query(Course.id).filter(Course.name == course and Course.session == sem).first()
                    new_enrolment = Enrolment(uid=uid, cid=c[0], completed="no")
                    self.add_row(new_enrolment)
        session.close()

    def get_all(self):
        session = self.DBSession()
        q = session.query(Enrolment)
        for enrolment in q.all():
            print(enrolment.course.name, enrolment.cid, enrolment.uid, enrolment.completed)
        session.close()
