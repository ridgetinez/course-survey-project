from abc import abstractmethod,  ABCMeta
from ast import literal_eval
import sqlite3
from collections import OrderedDict

class Writer(metaclass=ABCMeta):
    """ Super class for writers to CSV DB flat files
        Implemented to refactor later versions
    """
    pass


class ResponseWriter(Writer):
    """ Writer specific for a survey's response

    Args:
    survey -- responses recorded are for this specific survey
    """

    def __init__(self, survey):
        self.__db_path = './static/response{0}.db'.format(survey.id)
        try:
            self.__db_file = open(self.__db_path)
            self.__db_file.close()
        except:

            connection = sqlite3.connect(self.__db_path)
            cursorObj = connection.cursor()

            cursorObj.execute("CREATE TABLE RESPONSE (ID INT, ANSWER_ID INT, Answer TEXT, PRIMARY KEY (ID, ANSWER_ID))")
            i = 0;
            for q in survey.get_all_questions():
              for s in q.answer_list:
                cursorObj.execute("INSERT INTO RESPONSE VALUES (%d, %d, 0)" % (q.id, i))
                i += 1
              i = 0;
            connection.commit()
            connection.close()
            

    def update_row(self, qid, ans_index):
            #""" Increment csv to add a response to a given question """
      connection = sqlite3.connect(self.__db_path)
      cursorObj = connection.cursor()

      cursorObj.execute("SELECT * FROM RESPONSE WHERE ID = %d AND ANSWER_ID = %d" % (qid, ans_index))
      value = cursorObj.fetchall()
      lst = list(map(int, value[0]));
      lst[2] += 1
      print(value)
      cursorObj.execute("UPDATE RESPONSE SET Answer= %d WHERE ID= %d AND ANSWER_ID = %d" % (lst[2], qid, ans_index))
      connection.commit()
      connection.close()


class QuestionWriter(Writer):
    #""" Writer specific for question instances """

    def __init__(self):
      self.__db_path = './static/questions.db'
      try:
        self.__db_file = open(self.__db_path)
        self.__db_file.close()
      except:

        connection = sqlite3.connect(self.__db_path)
        cursorObj = connection.cursor()
        cursorObj.execute("CREATE TABLE QUESTIONS (QID INT, ANSWER_ID INT, Q_TEXT TEXT, Answer TEXT, PRIMARY KEY (QID, ANSWER_ID))")
        connection.commit()
        connection.close()
    def append_row(self, q):
      """ 
      Appends a row, saving question fields to flat file CSV
      Question in CSV is formatted: qid | question_text | answers_list
    
      Args:
      q -- question instance to be saved into csv
      """
      connection = sqlite3.connect(self.__db_path)
      cursorObj = connection.cursor()
      increment = 0;
      for s in q.answer_list:
        try:
          cursorObj.execute("CREATE TABLE QUESTIONS (SID INT, COURSE TEXT, QID TEXT, PRIMARY KEY(SID, QID))")
        except:
          print("Error")
        increment = increment + 1
      connection.commit()
      connection.close()
class SurveyWriter(Writer):
    """ Writer specific for a survey
    Args:
    survey -- survey ID, course name and question IDs recorded are for this specific survey
    """
    
    def __init__(self):
      self.__db_path = './static/survey.db'
      try:
        self.__db_file = open(self.__db_path)
        self.__db_file.close()
      except:

        connection = sqlite3.connect(self.__db_path)
        cursorObj = connection.cursor()
        cursorObj.execute("CREATE TABLE QUESTIONS (SID INT, COURSE TEXT, QID TEXT, PRIMARY KEY(SID, QID))")

        connection.commit()
        connection.close()

    def append_row(self, survey):

      connection = sqlite3.connect(self.__db_path)
      cursorObj = connection.cursor()
      for s in survey.get_all_questions():
        try:
          cursorObj.execute("INSERT INTO QUESTIONS VALUES (%d, '%s', '%s')" % (survey.id, survey.course, s.id))
        except:
          print("Error")
      connection.commit()
      connection.close()