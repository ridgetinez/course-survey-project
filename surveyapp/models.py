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
        return len(self.__answer_list)

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


class User(object):
    """ User object acts as superclass for different types of users

    Args:
    password   -- User's password
    identifier -- User's identifier
    """

    def __init__(self, identifier, password):
        self.__identifier = identifier
        self.__password = password

    def __eq__(self, other):
        return self.__identifier == other.__identifier

    def __hash__(self):
        return hash(self.__identifier)

    def __str__(self):
        return self.__identifier

    def as_dict(self):
        return {"type" : self.type_name(), "identifier" : self.__identifier}

    #checks if password matches User's password
    def check_password(self, password):
        if password == self.__password:
            return True
        else:
            return False

class Admin(User):
    def type_name(self):
        return "admin"

class Staff(User):
    def __init__(self, identifier, password, classes):
        self._classes = classes
        super(Staff, self).__init__(identifier, password)

    def validate_identifier():
        if (self.__identifier.isdigit()):
            return True
        else:
            return False

    def type_name(self):
        return "staff"

    def get_classes(self):
        return self.__classes

class Student(User):
    def __init__(self, identifier, password, enrolement):
        self.__enrolement = enrolement
        super(Student, self).__init__(identifier, password)

    def validate_identifier():
        if (self.__identifier.isdigit()):
            return True
        else:
            return False

    def type_name(self):
        return "student"

    def get_enrolement(self):
        return self.__enrolement

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
