import models
import csv

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
 
   # def get_next_question(self, qid):
    #	if SurveyController.has_next_question is True:
    #		return self.__survey.get_question(qid + 1) 
    #	else:
    #		return self.__survey.get_question(qid)
    #def get_previous_question(self, qid):
    #	if SurveyController.has_previous_question is True:
    #		return self.__survey.get_question(qid - 1) 
    #	else:
    #		return self.__survey.get_question(qid)
    #def has_previous_question(self, qid):
    #	try:
    #		self.__survey.get_question(qid - 1)
    #		return True
    #	except:
    #		return False
    #def has_next_question(self, qid):
    #	try:
    #		print (self.__survey.get_question(qid + 1))
    #		self.__survey.get_question(qid + 1)
    #		return True
    #	except:
    #		return False
    def write_csv (self, qid):
    	with open ('response.csv', 'w')  as csvfile:
    		fieldnames = ['ID', 'response']
    		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    		for line in self.__response.values():
    			writer.writerow({'ID' : qid, 'response': self.__response[qid]})
    @property
    def response(self):
    	return self.__response		

    # IDEAS
    
    # GET question, store in 
    
    # 
    
     
