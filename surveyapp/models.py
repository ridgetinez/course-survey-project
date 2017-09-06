# Agile Development Memes for Minjie Shen's teens
import csv


class Question(object):
    """ Question object to populate question pools and surveys

    Args:
    question_text -- String of the question displayed to user
    answer_list   -- Tuple of strings representing multiple choice answers
    """

    uqid = 0

    def __init__(self, question_text, answer_list):
        self.__question_text = question_text
        self.__answer_list = list(set(answer_list))
        self.__qid = Question.uqid
        Question.uqid += 1

    def __eq__(self, other):
        return self.__question_text == other.__question_text

    def __hash__(self):
        return hash(self.__question_text)

    def __str__(self):
        return '{0} : {1}'.format(self.__question_text, self.__answer_list)

    @property
    def id(self):
        return self.__qid

    @property
    def num_answers(self):
        return self.__num_answers

    @property
    def text(self):
        return self.__question_text

    @property
    def answer_list(self):
        return self.__answer_list

class QuestionStore(object):
    """ Super-class for question container classes

    Args:
    question_list -- list of questions to be stored in container
    """
    def __init__(self, question_list):
        self.__question_dict = {}
        for q in question_list:
            if q not in self.__question_dict.values():
                self.__question_dict[q.id] = q
        self.__size = len(self.__question_dict)

    def add_question(self, q):
        if q in self.__question_dict.values():
            return False
        self.__question_dict[q.id] = q
        self.__size += 1
        return True

    def get_question(self, qid):
        try:
            return self.__question_dict[qid]
        except:
            return None

    def get_all_questions(self):
        return list(self.__question_dict.values())


# USE NGROK FOR FLASK
class Survey(QuestionStore):
    """ Surveys holds a curated set of questions with response data

    Args:
    question_list -- list of questions appearing in the survey
    """

    usid = 0

    def __init__(self, question_list, course_name):
        super(Survey, self).__init__(question_list)
        #self.__responses = list()
        self.__course_name = course_name
        self.__sid = Survey.usid
        self.__public_url = '/survey/respond/{0}/{1}'.format(self.__course_name, self.__sid)
        Survey.usid += 1

    @property
    def id(self):
        return self.__sid

    @property
    def url(self):
        return self.__public_url

    @property
    def course(self):
        return self.__course_name


class Admin(object):
    """ Question object to populate question pools and surveys

    Args:
    email -- Admin's email
    password   -- Admin's password
    """

    uaID = 0

    def __init__(self, email, password):
        self.__email = email
        self.__password = password
        self.__aID = Admin.uaID
        Admin.uaID += 1

    def __eq__(self, other):
        return self.__email == other.__email

    def __hash__(self):
        return hash(self.__aID)

    def __str__(self):
        return '{0} : {1}'.format(self.__aID, self.__email)

    #getter function for admin id
    def getAdminID(self):
        return self.__aID

    #getter function for admin email
    def getEmail(self):
        return self.__email

    #checks if password matches admin's password
    def checkPassword(self, password):
        if password == self.__password:
            return True
        else:
            return False


class Course(object):
    """ Container of Survey Instances

    Args:
    course_id -- unique label for the course in form COMPXXXX
    session   -- which year and semester the course is running
    """

    def __init__(self, course_id, session):
        self.__course_id = course_id
        self.__session = session
        self.__surveys = []

    def __str__(self):
        return "{0}:{1}".format(self.__course_id, self.__session)

    def add_survey(self, survey):
        """ Appends a survey to the courses list of surveys

        Args:
        survey -- survey to be labelled under Course instance
        """
        return self.__surveys.append(survey) # does not check for duplicates

    def get_survey(self, sid):
        """ Return specific survey by survey id

        Args:
        sid -- unique survey integer identifier
        """
        for s in self.__surveys:
            if s.id == sid:
                return s

    @property
    def id(self):
        return self.__course_id

    @property
    def surveys(self):
        return self.__surveys
