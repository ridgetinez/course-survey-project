
# Agile Development Memes for Minjie Shen's teens



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
        self.__num_answers = len(self.__answer_list)
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
           
    def add_answer_option(self, answer):
        if answer in self.__answer_list:
            return False 
        self.__answer_list.append(answer)
        return True


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
         
         

    

        
        
        
        
        
        
        