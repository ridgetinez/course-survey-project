from surveyapp import modelcontrollers
from math import ceil
import matplotlib.pyplot as plt
# from matplotlib.dates import DateFormatter
import numpy as np


class Visualiser(object):
    """ Matplotlib class interface for generating metrics for a given survey
    Args:
    course_name -- course requiring survey visualisations
    course_session -- year and semester to identify the course
    """
    def __init__(self, course_name:str, course_session:str):
        self.__sname = course_name
        self.__session = course_session
        print(self.__sname, self.__session)

    """ Visualise how many responses the survey has received """ 
    def visualise_student_engagement(self):
        # number of unique responses is number of responses for survey / number of questions in survey
        responses = modelcontrollers.ResponsesController.get_responses(self.__sname, self.__session)
        questions = modelcontrollers.SurveyController.get_survey_questions(self.__sname, self.__session)
        num_respondents = modelcontrollers.UserController.get_respondents(self.__sname, self.__session)
        responded = ceil(len(responses)/len(questions))
        data = [[responded], [num_respondents-responded]]
        fig = Visualiser.draw_segmented_bargraph(data, "Respondents", [1], "Responses for " + self.__sname + self.__session)
        fig.savefig('./surveyapp/static/' +  self.__sname + self.__session)
        # jndividual questions will have 0 length answers

    """ Given the number of bars required and the data, construct a bar graph """
    @staticmethod
    def draw_segmented_bargraph(bar_data:list, x:str, y:list, title: str):
        
        plt.rcdefaults()
        fig, ax = plt.subplots()

        N = 5
        menMeans = (20, 35, 30, 35, 27)
        womenMeans = (25, 32, 34, 20, 25)
        menStd = (2, 3, 4, 1, 2)
        womenStd = (3, 5, 2, 3, 3)
        ind = np.arange(N)
        width = 0.35

        p1 = ax.bar(ind, menMeans, width, yerr=menStd)
        p2 = ax.bar(ind, womenMeans, width, bottom=menMeans, yerr=womenStd)

        ax.set_ylabel('Scores')
        ax.set_title('Scores by group and gender')
        ax.set_xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5'))
        ax.set_yticks(np.arange(0, 81, 10))
        ax.legend((p1[0], p2[0]), ('Men', 'Women'))

        return fig


        # plt.rcdefaults()
        # fig, ax = plt.subplots()    # whats the difference between ax and plt?
        # ys = np.arange(len(y))
        # ax.bar(ys, data, align='center', color='green', ecolor='black')
        # ax.bar()
        # ax.set_yticks(ys)
        # ax.set_yticklabels(y)
        # ax.invert_yaxis()  # labels read top-to-bottom
        # ax.set_xlabel(x)
        # ax.set_title(title)
        # return fig
       
  


        # # for now assume that bar_data is a 1x2 array for visualise student engagement
        # ys = np.array(y)
        # y_pos = np.arange(len(ys))

        # p1 = plt.barh(y_pos, bar_data[0], align='center', color='#FF9F24', ecolor='black')
        # #p2 = plt.barh(y_pos, bar_data[1], align='center', color='black', ecolor='black')

        # plt.ylabel(x)
        # plt.title(title)
        # #plt.legend((p1[0]), ('Completed'))

        # plt.show()


    def visualise_survey_response(self):
        pass 
    
