
class Question(object):
    """ Question object to populate question pools and surveys
    
    Keywords:
    questionText | String holds the question displayed to user
    answerList   | List of strings representing multiple choice answers
    qid          | Unique identifier for instance
    """
    
    def __init__(self, questionText, answerList, qid):
        self.questionText = questionText
        self.answerList = answerList
        self.qid = qid        
    
    def __str__(self):
        pass
    
    def add
        