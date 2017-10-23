from flask import session
from surveyapp import modelcontrollers, auth
from datetime import datetime
"""
class SurveyController(object):
     Handles the respondent answering a survey

    Args:
    survey -- the designated survey to serve to respondent


    def __init__(self, survey):
        self.__survey = survey
        self.__response = dict()

    def get_question(self, qid):
        return self.__survey.get_question(qid)

    # pressing NEXTQ, we attain
    def set_response(self, qid, ans_index):
        # GET QUESTION AND THEN
        self.__response[qid] = ans_index

"""
class FormController(object):
    def parse_login(request):
        try:
            success = modelcontrollers.UserController.check_password(request['id'], request['password'])
        except KeyError:
            print("error: something went wrong when parsing login form")
        if success:
            user = modelcontrollers.UserController.get_user(request['id'])
            auth.UserAuthoriser.provideUserSession({'identifier' : user.uid, 'role' : user.role})
            return True
        return False
    
    def parse_create_q(request):
        answers = []
        for i in range(session['n_answers']):
            answers.append(request['answer' + str(i)])

        #check for parsing errors
        if request['question_text'] == "":
            return [False, 'qerror']
        if len(set(answers)) < session['n_answers']:
            return [False, 'aerror']
        if "" in answers:
            return [False, 'aerror']

        if modelcontrollers.QuestionController.write_question([request['question_text'], answers]) == False:
            return [False, 'derror']
        return [True]

    def parse_create_survey(request):
        try:
            start_time = datetime.strptime(request['start-time'], "%Y-%m-%dT%H:%M")
            end_time = datetime.strptime(request['end-time'], "%Y-%m-%dT%H:%M")
        except ValueError:
            return [False, 'verror']

        if start_time > end_time:
            return [False, 'terror']
        course = request['course_name'].split(" ")
        questions = []
        for item in request:
            if (item != 'course_name') and (item != 'start-time') and (item != 'end-time'):
                questions.append(item)
        if len(questions) == 0:
            return [False, 'qerror']
        if modelcontrollers.SurveyController.write_survey(course[0], course[1], start_time, end_time, questions) == False:
            return [False, 'rerror']
        return [True]

    def parse_response(request, user_id):
        survey_list = request['course'].split(" ")
        for item in request:
            if item != 'course':
                modelcontrollers.ResponsesController.write_response(survey_list[0], survey_list[1], item, request[item])
        modelcontrollers.UserController.set_survey_completed(survey_list[0], survey_list[1], user_id)

    def parse_register(request):
        if request['password1'] != request['password2']:
            return [False, 'merror']
        success = modelcontrollers.UserController.write_user([request['id'], request['password1'], 'guest', request['course_name']])
        return [success, 'derror']
