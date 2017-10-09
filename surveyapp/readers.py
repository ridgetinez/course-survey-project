from abc import ABCMeta, abstractmethod
import csv
from sqlalchemy import *
from models import Question, SurveyQStore, Survey, Course, User, Enrolment, Answer, Responses, TableConnector, TableLoader

class QuestionReader(TableConnector):
 #
    def __init__(self):
      super().__init__()

    def check_question(self, Q_TEXT):
      """ 
      Appends a row, saving question fields to flat file CSV
      Question in CSV is formatted: qid | question_text | answers_list
    
      Args:
      q -- question instance to be saved into csv
      """
      session = self.DBSession()
      if session.query(exists().where(Question.q_text==Q_TEXT)).scalar() is True:
        session.close()
        return True
      else:
        print("Doesn't Exists")
        session.close()
        return False

class UserReader(TableConnector):
    def __init__(self):
      super().__init__()

    def authorise_user(self, user, password):
      """ 
      Appends a row, saving question fields to flat file CSV
      Question in CSV is formatted: qid | question_text | answers_list
    
      Args:
      q -- question instance to be saved into csv
      """
      session = self.DBSession()
      if session.query(exists().where(User.uid==user and User.password==password)).scalar() is True:
        session.close()
        return True
      else:
        print("Doesn't Exists")
        session.close()
        return False

class SurveyReader(TableConnector):
    def __init__(self):
      super().__init__()

    def check_survey(self, course_name, course_session):
      """ 
      Appends a row, saving question fields to flat file CSV
      Question in CSV is formatted: qid | question_text | answers_list
    
      Args:
      q -- question instance to be saved into csv
      """
      session = self.DBSession()
      name = Course.name
      print(course_name)
      if session.query(Survey).filter(Course.name == course_name).count() and session.query(Survey).filter(Course.session == course_session).count() is not 0:
        session.close()
        return True
      else:
        print("Doesn't Exists")
        session.close()
        return False
