"""
modelcontrollers.py contains classes for controllers communicating with the database
"""

from abc import abstractmethod, ABCMeta
from ast import literal_eval
import csv
from surveyapp import models, engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

class CSVloader():
    def get_users_csv():
        with open("surveyapp/static/passwords.csv", newline='') as userfile:
            reader = csv.reader(userfile)
            for row in reader:
                UserController.write_user(row)
        UserController.write_user(['admin', 'password', 'admin'])

    def get_course_csv():
        with open("surveyapp/static/courses.csv", newline='') as coursefile:
            reader = csv.reader(coursefile)
            for row in reader:
                CourseController.write_course(row)

    def get_enrolement_csv():
        with open("surveyapp/static/enrolments.csv", newline='') as enrolmentsfile:
            reader = csv.reader(enrolmentsfile)
            for row in reader:
                EnrolmentController.write_enrolment([row[1], row[2], row[0]])

class CourseController():
    def write_course(course_rep): # course_rep = [name, session]
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        new_course = models.Course(name=course_rep[0], session=course_rep[1])
        session.add(new_course)
        try:
            session.commit()
        except:
            pass
        session.close()

    def get_courses():
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        session.close()
        return session.query(models.Course).all()

class EnrolmentController():
    def write_enrolment(enrolment_rep): # enrolment_rep = [course_name, course_session, user_id]
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        new_enrolment = models.Enrolment(course_name=enrolment_rep[0], course_session=enrolment_rep[1], uid=enrolment_rep[2], completed='False')
        session.add(new_enrolment)
        try:
            session.commit()
        except:
            pass
        session.close()

    def get_enrolment(user_id):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        courses = session.query(models.Enrolment).filter(models.Enrolment.uid == user_id).all()
        session.close()
        return courses


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

        session.close()
        if user.password == password:
            return True
        else:
            return False

    def get_user_survey(user_id):
        enrolments = EnrolmentController.get_enrolment(user_id)
        surveys = []
        for enrolment in enrolments:
            survey = SurveyController.get_survey(enrolment.course_name, enrolment.course_session)
            if enrolment.completed != 'True':
                surveys.append(survey)
            elif enrolment.completed == 'True' and survey.state == 'closed':
                surveys.append(survey)
        return surveys

    def set_survey_completed(course_name, course_session, user_id):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        enrolment = session.query(models.Enrolment).filter(models.Enrolment.uid == user_id).filter(models.Enrolment.course_name == course_name).filter(models.Enrolment.course_session == course_session).first()

        enrolment.completed = 'True'
        session.commit()
        session.close()

    def get_respondents(course_name, course_session):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        
        respondents = session.query(models.Enrolment).filter(models.Enrolment.course_name == course_name).filter(models.Enrolment.course_session == course_session).all()
        # remove rows which are staff checked from the user table
        session.close()
        return len(respondents);


class QuestionController():
    def write_question(question_rep): # question_rep = [question_text, [answers]]
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        new_question = models.Question(question=question_rep[0], ans="|".join(question_rep[1]), deleted='False')
        session.add(new_question)
        try:
            session.commit()
        except:
            print('error: Question alread exists!')
            return False
        session.close()
        return True

    def get_question(id): # [id, question, answers, deleted]
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        question = session.query(models.Question).filter(models.Question.id == id).first()

        session.close()
        return [question.id, question.question, QuestionController.reformat_ans(question.ans), question.deleted]

    def get_all_questions():
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        questions = session.query(models.Question).all()
        question_list = []
        for question in questions:
            question_list.append([question.id, question.question, QuestionController.reformat_ans(question.ans), question.deleted])

        session.close()
        return question_list

    def reformat_ans(answer):
        if answer == "":
            return []
        answers = answer.split('|')
        return answers

    def delete_question(question_id):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        question = session.query(models.Question).filter(models.Question.id == question_id).first()
        question.deleted = 'True'
        session.commit()
        session.close()

class SurveyController():
    def write_survey(course_name, course_session, starttime, endtime, questions):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        state='created'
        if starttime < datetime.now():
            state='review'
        if endtime < datetime.now():
            state='deactivate'
        new_survey = models.Survey(course_name=course_name, course_session=course_session, starttime=starttime, endtime=endtime, state=state)
        session.add(new_survey)
        for qid in questions:
            new_question = models.SurveyQStore(course_name=course_name, course_session=course_session, qid=qid)
            session.add(new_question)
        try:
            session.commit()
        except:
            return False
        session.close()
        return True

    def get_survey(course_name, course_session):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        survey = session.query(models.Survey).filter(models.Survey.course_name == course_name).filter(models.Survey.course_session == course_session).first()
        session.close()
        try:
            SurveyController.set_deactivate_after_end(survey)
            SurveyController.set_review_after_start(survey)
        except AttributeError:
            print("no survey for {} {}".format(course_name, course_session))

        return survey

    def get_all_surveys():
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        surveys = session.query(models.Survey).all()
        session.close()
        for survey in surveys:
            SurveyController.set_deactivate_after_end(survey)
            SurveyController.set_review_after_start(survey)
        return surveys

    def get_survey_questions(course_name, course_session):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        q_stores = session.query(models.SurveyQStore).filter(models.SurveyQStore.course_name == course_name).filter(models.SurveyQStore.course_session == course_session).all()

        questions = []
        for q in q_stores:
            questions.append(QuestionController.get_question(q.qid))

        session.close()
        return questions

    def set_survey_active(course_name, course_session):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        survey = session.query(models.Survey).filter(models.Survey.course_name == course_name).filter(models.Survey.course_session == course_session).first()

        survey.state = 'active'
        session.commit()
        session.close()

    def set_deactivate_after_end(survey):
        if survey.endtime < datetime.now():
            DBSession = sessionmaker(bind=engine)
            session = DBSession()

            sur = session.query(models.Survey).filter(models.Survey.course_name == survey.course_name).filter(models.Survey.course_session == survey.course_session).first()

            if sur.state == 'created' or sur.state == 'review':
                sur.state = 'deactivate'
            elif sur.state == 'active':
                sur.state = 'adeactivate'
            session.commit()
            session.close()

    def set_review_after_start(survey):
        if survey.starttime < datetime.now():
            DBSession = sessionmaker(bind=engine)
            session = DBSession()

            sur = session.query(models.Survey).filter(models.Survey.course_name == survey.course_name).filter(models.Survey.course_session == survey.course_session).first()

            if sur.state == 'created':
                sur.state = 'review'
            session.commit()
            session.close()
    def close_survey(course_name, course_session):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        survey = session.query(models.Survey).filter(models.Survey.course_name == course_name).filter(models.Survey.course_session == course_session).first()

        if survey.endtime < datetime.now():
            survey.state = 'closed'

        session.commit()
        session.close

class ResponsesController():
    def write_response(course_name, course_session, qid, response):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        response = models.Responses(course_name=course_name, course_session=course_session, qid=qid, response=response)

        session.add(response)
        session.commit()
        session.close()

    def get_responses(course_name, course_session):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        responses = session.query(models.Responses).filter(models.Responses.course_name == course_name).filter(models.Responses.course_session == course_session).all()

        session.close()
        return responses
