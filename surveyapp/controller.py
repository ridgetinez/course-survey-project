import models

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
                
    def 
    # IDEAS
    
    # GET question, store in 
    
    # 
    
     
