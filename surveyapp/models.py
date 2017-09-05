
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
    
    def __str__(self):
        return '{0}\n{1}'.format(self.__question_text, self.__answer_list) 

    @property
    def qid(self):
        return self.__qid
           
    
    def add_answer_option(self, answer):
        self.__answer_list.append(answer)
        
        
firstQ = Question("How fucked are you for 1531?", ["Yes", "Yes in green", "si est verte"])
print(firstQ)
firstQ.add_answer_option("<3")
print(firstQ)
print(firstQ.qid)
secondQ = Question("Did you really sleep when you have 1531?", ["Yes", "No", "No in yes."])
print(secondQ.qid)




class QuestionPool(object):
    """ Retrieves the collection of created question
    
    Args:
    question_list -- list of questions created
    """
    
    def __init__(self, question_list):
        q_dict = {}
        for q in question_list:
            q_dict[q.qid] = q
        self.__question_dict = q_dict
        
    # LEGACY ITER from when QPOOL was a list. TODO: Change for dicts
    def __iter__(self):
        return self.__question_dict
    
    def __next__(self):
        if self.i >= len(self.question_list):
            raise StopIteration
        next_question = self.question_list[self.i]
        self.i += 1
        return next_question
        
        
    def add_question(self, q):
        self.__question_dict[q.qid] = q
        
    def get_question(self, qid):
        return self.__question_dict[qid]
        
        
    
qp = QuestionPool([firstQ, secondQ])
for q in qp:
    print(q) 
        
        
        
        
        
        
        
        