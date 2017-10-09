
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, inspect

Base = declarative_base()
engine = create_engine('sqlite:///library.db')

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

class SurveyQStore2(Base):
    __tablename__ = 'SURVEYQSTORE'
    sid = Column(Integer, ForeignKey('SURVEYS.id'), primary_key=True)
    qid = Column(Integer, ForeignKey('QUESTIONS.id'), primary_key=True)
    aid = Column(Integer, ForeignKey('ANSWERS.id'), primary_key=True)
    # required = Column(String, nullable=False)   # optional vs. mandatory questions
    survey = relationship('Survey')
    questions = relationship('Question')

class Responses(Base):
    __tablename__ = 'RESPONSES'
    id = Column(Integer, primary_key=True)
    sid = Column(Integer, ForeignKey('SURVEYS.id'))
    qid = Column(Integer, ForeignKey('QUESTIONS.id'))
    response = Column(String, nullable=False)


Base.metadata.create_all(bind=engine)
ins = inspect(engine)
for t in ins.get_table_names(): print(t)