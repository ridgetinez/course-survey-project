
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
        self.__answer_list = answer_list
        self.__qid = Question.uqid
        Question.uqid += 1
    
    def __eq__(self, other):
        return self.__question_text == other.__question_text
        
    def __hash__(self):
        return hash(self.__question_text)
    
    def __str__(self):
        return '{0} : {1}'.format(self.__question_text, self.__answer_list) 

    @property
    def qid(self):
        return self.__qid
           
    
    def add_answer_option(self, answer):
        self.__answer_list.append(answer)


class QuestionStore(object):
    """ Super-class for question container classes
    
    Args:
    question_list -- list of questions to be stored in container
    """
    def __init__(self, question_list):
        self.__question_dict = {}
        for q in question_list:
            if q not in self.__question_dict.values():
                self.__question_dict[q.qid] = q
        self.__size = len(self.__question_dict)     
    
    def add_question(self, q):
        if q in self.__question_dict.values():
            return False
        self.__question_dict[q.qid] = q
        self.__size += 1
        return True
    
    def get_question(self, qid):
        try:
            return self.__question_dict[qid]
        except:
            return None


# class QuestionPool(QuestionStore):
#     """ Retrieves the collection of created question
#     
#     Args:
#     question_list -- list of questions created
#     """
#     
#     def __init__(self, question_list):
#         q_dict = {}
#         for q in question_list:
#             q_dict[q.qid] = q
#         self.__question_dict = q_dict   
#         
#     def add_question(self, q):
#         self.__question_dict[q.qid] = q
#         
#     def get_question(self, qid):
#         return self.__question_dict[qid]
# 
# 
# # USE NGROK FOR FLASK
# class Survey(QuestionStore):
#     """ Surveys holds a curated set of questions with response data
#     
#     Args:
#     question_list -- list of questions appearing in the survey
#     """
#     
#     usid = 0
#     
#     def __init__(self, question_list):
#         self.question_list = set(question_list)
#         self.sid = Survey.usid
#         # create another dictionary which maps qid to survey responses list
#         self.responses = pass
#         Survey.usid += 1
#     
#     def retrieve_responses(self):
#         pass
#     
#     def get_public_url(self):
#         return "placeholderString"
#         
#         
# class Course(object):
#     pass
#     

        
        
        
        
        
        
        