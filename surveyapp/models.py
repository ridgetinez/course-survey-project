"""
models.py uses sqlalchemy to implement database for survey objects
"""

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from surveyapp import Base

class User(Base):
    __tablename__ = 'USERS'
    uid = Column(String(50), primary_key=True)
    password = Column(String(50), nullable=False)
    role = Column(String(50), nullable=False)

    __mapper_args__ = {
        'polymorphic_on': role,
        'polymorphic_identity': 'user'
    }

class Admin(User):
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

class Staff(User):
    __mapper_args__ = {
        'polymorphic_identity': 'staff'
    }

class Student(User):
    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

class Guest(User):
    enrolled = Column(String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'guest'
    }

class Course(Base):
    __tablename__ = 'COURSES'
    name = Column(String(50), primary_key=True)
    session = Column(String(50), primary_key=True)

class Enrolment(Base):
    __tablename__ = 'ENROLMENTS'
    uid = Column(Integer, ForeignKey('USERS.uid'), primary_key=True)
    completed = Column(String(50), nullable=False)
    course_name = Column(String(50), nullable=False, primary_key=True)
    course_session = Column(String(50), nullable=False, primary_key=True)
    user = relationship('User')
    course = relationship('Course')
    __table_args__ = (ForeignKeyConstraint([course_name, course_session],
                                           [Course.name, Course.session]),
                                           {})

class Question(Base):
    __tablename__ = 'QUESTIONS'
    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    ans = Column(String, nullable=False)
    deleted = Column(String(50), nullable=False)
    is_optional = Column(String(50), nullable=False)

class Survey(Base):
    __tablename__ = 'SURVEYS'
    course_name = Column(String(50), nullable=False, primary_key=True)
    course_session = Column(String(50), nullable=False, primary_key=True)
    endtime = Column(DateTime, nullable=False)
    starttime = Column(DateTime, nullable=False)
    course = relationship('Course')
    state = Column(String(50), nullable=False)
    __table_args__ = (ForeignKeyConstraint([course_name, course_session],
                                           [Course.name, Course.session]),
                                           {})



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
    course_name = Column(String(50), nullable=False, primary_key=True)
    course_session = Column(String(50), nullable=False, primary_key=True)
    qid = Column(Integer, ForeignKey('QUESTIONS.id'), primary_key=True)
    __table_args__ = (ForeignKeyConstraint([course_name, course_session],
                                           [Survey.course_name, Survey.course_session]),
                                           {})

class Responses(Base):
    __tablename__ = 'RESPONSES'
    id = Column(Integer, primary_key=True)
    course_name = Column(String(50), nullable=False)
    course_session = Column(String(50), nullable=False)
    qid = Column(Integer, ForeignKey('QUESTIONS.id'))
    response = Column(String, nullable=False)
    __table_args__ = (ForeignKeyConstraint([course_name, course_session],
                                           [Survey.course_name, Survey.course_session]),
                                           {})
