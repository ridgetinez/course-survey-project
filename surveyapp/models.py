
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, inspect
from abc import ABCMeta, abstractmethod

Base = declarative_base()
DATABASE_URL = 'sqlite:///survey.db'
engine = create_engine('sqlite:///survey.db')

class TableConnector(metaclass=ABCMeta):

    def __init__(self): 
        self.__base = declarative_base()
        self.__engine = create_engine(DATABASE_URL)
        try:
            Base.metadata.create_all(bind=self.__engine)
        except:
            print("Tables already created! SHITS LIT.")
        self.DBSession = sessionmaker(bind=self.__engine)

class TableLoader(TableConnector):

    def __init__(self):
        print("hhihihi")
        super().__init__()

   # @abstractmethod
    def csv_to_db(self, csv_name):
       pass

class User(Base):
    __tablename__ = 'USERS'
    uid = Column(String, primary_key=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

class Course(Base):
    __tablename__ = 'COURSES'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    session = Column(String, nullable=False)

class Enrolment(Base):
    __tablename__ = 'ENROLMENTS'
    uid = Column(Integer, ForeignKey('USERS.uid'), primary_key=True)
    cid = Column(String, ForeignKey('COURSES.id'), primary_key=True)
    completed = Column(String, nullable=False)
    user = relationship('User')
    course = relationship('Course')

class Answer(Base):
    __tablename__ = 'ANSWERS'
    id = Column(Integer, primary_key=True)
    ans_text = Column(String, unique=True)

class Question(Base):
    __tablename__ = 'QUESTIONS'
    id = Column(Integer, primary_key=True)
    q_text = Column(String, unique=True, nullable=False)

class Survey(Base):
    __tablename__ = 'SURVEYS'
    id = Column(Integer, ForeignKey('COURSES.id'), primary_key=True)   # 1to1 relationship allows fk to also be pk
    #endtime = Column(DateTime, nullable=False)
    #   starttime = Column(DateTime, nullable=False)
    course = relationship('Course')
    state = Column(String, nullable=False)

# BENEFITS OF THIS DESIGN
# The required field is a question+survey property not affected by answers
# abstracting this out and creating an idea to this SURVEYQStore1 will allow us to
# simply index this table when wanting to add answers to questions (with this imp. they will already be linked to surveys)  
class SurveyQStore(Base):
    __tablename__ = 'SURVEYQSTORE'
    sid = Column(Integer, ForeignKey('SURVEYS.id'), primary_key=True)
    qid = Column(Integer, ForeignKey('QUESTIONS.id'), primary_key=True)
    q_type = Column(String, nullable=False)     # could remove this and have aid be the NULL id when it's text based.
    required = Column(String, nullable=False)   # optional vs. mandatory questions
    survey = relationship('Survey')

class Responses(Base):
    __tablename__ = 'RESPONSES'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sid = Column(Integer, ForeignKey('SURVEYS.id'), primary_key=True)
    qid = Column(Integer, ForeignKey('QUESTIONS.id'), primary_key=True)
    response = Column(String)
    # sqid = Column(Integer, ForeignKey('SURVEYQSTORE1.id'), primary_key=True)
    # response = Column(String, nullable=False)
    # new design motivated by linking response to the specific question type
    # IF QTYPE == TEXT: LEAVE RESPONSE AS STRING
    # ELIF QTYPE == MC: TYPECAST TO INT
    # Also possible to just make the answertext (for MC and text) as what populates response.

class AnswerQStore(Base):
   __tablename__ = 'ANSWERQSTORE'
   qid = Column(Integer, ForeignKey('QUESTIONS.id'), primary_key=True)
   aid = Column(Integer, ForeignKey('ANSWERS.id'), primary_key=True)
   answer = relationship('Answer')
   question = relationship('Question')