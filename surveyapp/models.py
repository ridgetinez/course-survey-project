
class Question(object):
    """ Question object to populate question pools and surveys
    
    Args:
    question_text -- String of the question displayed to user
    answer_list   -- Tuple of strings representing multiple choice answers
    """
        
    def __init__(self, question_text, answer_list):
        self.question_text = question_text
        self.answer_list = answer_list
        self.uqid = id(self)
    
    def __str__(self):
        return '{0}\n{1}'.format(self.question_text, self.answer_list)        
    
    def addAnswerOption(self, answer):
        self.answer_list.append(answer)
        
        
firstQ = Question("How fucked are you for 1531?", ["Yes", "Yes in green", "si est verte"])
print(firstQ)
firstQ.addAnswerOption("<3")
print(firstQ)
print(getattr(firstQ, 'uqid'))