import surveyapp.models
from flask import session
class SurveyController(object):
    """ Handles the respondent answering a survey

    Args:
    survey -- the designated survey to serve to respondent
    """

    def __init__(self, survey):
        self.__survey = survey
        self.__response = dict()

    def get_question(self, qid):
        return self.__survey.get_question(qid)

    # pressing NEXTQ, we attain
    def set_response(self, qid, ans_index):
        # GET QUESTION AND THEN
        self.__response[qid] = ans_index


class FormController(object):
    def parse_create_q(request):
        answers = []
        print(request)
        for i in range(session['n_answers']):
            answers.append(request['answer' + str(i)])

        #check for parsing errors
        if request['question_text'] == "":
            return [False, 'qerror']
        if len(set(answers)) < session['n_answers']:
            return [False, 'aerror']
        if "" in answers:
            return [False, 'aerror']

        print({request['question_text'] : answers})
        #this is where you should call create question
        return [True]
