
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, inspect
from surveyapp import Base

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

class Question(Base):
    __tablename__ = 'QUESTIONS'
    id = Column(Integer, primary_key=True)
    question = Column(String, unique=True, nullable=False)
    ans = Column(String, nullable=False)
    deleted = Column(String, nullable=False)

class Survey(Base):
    __tablename__ = 'SURVEYS'
    id = Column(Integer, ForeignKey('COURSES.id'), primary_key=True)   # 1to1 relationship allows fk to also be pk
    endtime = Column(DateTime, nullable=False)
    starttime = Column(DateTime, nullable=False)
    course = relationship('Course')
    state = Column(String, nullable=False)



# IN 2ND ITERATION OFDEVELOPMENT, REQUIRED FIELD ISNT NECESSARY,
# In iter3 we may have to decouple sid|qid|required into one table
# and then link answers to the sid|qid key
# class SurveyQStore(Base):
#     __tablename__ = 'SURVEYQSTORE'
#     sid = Column(Integer, ForeignKey('SURVEYS.id'), primary_key=True)
#     qid = Column(Integer, ForeignKey('QUESTIONS.id'), primary_key=True)
#     required = Column(String, nullable=False)

class SurveyQStore(Base):
    __tablename__ = 'SURVEYQSTORE'
    id = Column(Integer, primary_key=True)
    sid = Column(Integer, ForeignKey('SURVEYS.id'), primary_key=True)
    qid = Column(Integer, ForeignKey('QUESTIONS.id'), primary_key=True)
    #required = Column(String, nullable=False)

class Responses(Base):
    __tablename__ = 'RESPONSES'
    id = Column(Integer, primary_key=True)
    sid = Column(Integer, ForeignKey('SURVEYS.id'))
    qid = Column(Integer, ForeignKey('QUESTIONS.id'))
    response = Column(String, nullable=False)
