from abc import abstractmethod,  ABCMeta
from ast import literal_eval

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapper, clear_mappers, relationship
from models import Question, SurveyQStore, Survey, Course, User, Enrolment, Answer, Responses, TableConnector, TableLoader, AnswerQStore
from sqlalchemy import *
from readers import QuestionReader, UserReader, SurveyReader
engine = create_engine('sqlite:///survey.db')

Base=declarative_base()
metadata = MetaData()

class ResponseWriter(TableLoader):
    def __init__(self):
      super().__init__()

    def save_responses(self, question_id, response_string, survey_id):
      session = self.DBSession()

      print(survey_id)
      new_response = Responses(sid=survey_id, qid=question_id, response=response_string)

      #if session.query(exists().where(Responses.response==response_string)).scalar() is False:
      session.add(new_response)
      session.commit()
      session.close()
      #return True
     # else:
        #print("Error")
       # session.close()
       # return False


class QuestionWriter(TableConnector):
 #
    def __init__(self):
      super().__init__()

    def append_question(self, Q_LIST):
      """ 
      Appends a row, saving question fields to flat file CSV
      Question in CSV is formatted: qid | question_text | answers_list
    
      Args:
      q -- question instance to be saved into csv
      """
      session = self.DBSession()
      for q in Q_LIST:
        print(q)
        new_question = Question(q_text=q)
        for s in Q_LIST[q]:
          new_answer = Answer(ans_text=s)
          new_AnsQstore = AnswerQStore()  
          new_AnsQstore.question = new_question
          new_AnsQstore.answer = new_answer
          try:
            session.add(new_AnsQstore)
            session.commit()
          except:
            print("Error")
      session.close()

class SurveyWriter(TableLoader):
    """ Writer specific for a survey
    Args:
    survey -- survey ID, course name and question IDs recorded are for this specific survey
    """

    def __init__(self):
      super(TableLoader, self).__init__()

    def append_row(self, survey, ENDDATE):
      """ 
      Appends a row, saving question fields to flat file CSV
      Question in CSV is formatted: qid | question_text | answers_list
    
      Args:
      q -- question instance to be saved into csv
      """
      session = self.__DBSession()

      new_survey = Survey(SurveyID=survey.id, ENDDATE=ENDDATE)

      try:
        
        session.add(new_survey)
        session.commit()
      except:
        print("Error")
      session.close()


ins = inspect(engine)
for t in ins.get_table_names(): print(t)

DBSession = sessionmaker(bind=engine)
session = DBSession()

v = Question(q_text="HI")


dict = {"abc":("SCA","BSAF","SDADA"), "bcd":("2S","SA3","SAFA4"), "cde":("SAF3","FA4","SFA5")}
q = QuestionWriter()
q.append_question(dict)
#qs = QuestionReader()
#qs.check_question(str(v.q_text))

new_user = User(uid="z51s251", password="yobitch", role="bitch")
try:
 # session.add(new_user)
  session.commit()
except:
  print("hi")
u = UserReader()
u.authorise_user("z51251s", "yobitch")

u = SurveyReader()
#u.check_survey("yobitch", "bitch")
new_course = Course(name="yobitch", session="bitch")
new_course = Course(name="ysobisstcsh", session="bitscscassdasdadasdh")
new_survey = Survey(state="yo")
new_survey.course = new_course
if u.check_survey(new_course.name, new_course.session) is False:
  session.add(new_survey)
  session.commit()
r = ResponseWriter()


r.save_responses(1, "Yesdasdsas", 0)



#q.check_questions(str(v.q_text))

