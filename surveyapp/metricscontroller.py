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
        data = [responded, num_respondents-responded]
        fig = Visualiser.draw_segmented_hbargraph(data, "Respondents", ["Respondents", "Not Responded"], "Responses for " + self.__sname + self.__session)
        fig.savefig('./surveyapp/static/' +  self.__sname + self.__session)
        # jndividual questions will have 0 length answers

    """ Given the number of bars required and the data, construct a bar graph 
    
    Returns:
    Constructed horizontal bar matplotlib figure object
    """
    @staticmethod
    def draw_segmented_hbargraph(data:list, x:str, y:list, title: str):
        plt.rcdefaults()
        fig, ax = plt.subplots()    # whats the difference between ax and plt?
        ys = np.arange(len(y))
        ax.barh(ys, data, align='center', color='#343a40', ecolor='black')
        ax.set_yticks(ys)
        ax.set_yticklabels(y)
        ax.invert_yaxis()
        ax.set_xlabel(x)
        ax.set_title(title)
        return fig

    """ Create visualisations for the multiple choice questions of the survey
    
    Returns:
    List of filenames of the png's containing the question visualisations
    """
    def visualise_survey_questions(self):
        filenames = []
        for q in modelcontrollers.SurveyController.get_survey_questions(self.__sname, self.__session):
            column_data = []
            x_ticks = []
            if not q[2] == []:
                for i in range(len(q[2])):
                    num_responses = modelcontrollers.ResponsesController.num_answers(self.__sname, self.__session, q[0], i)
                    column_data.append(num_responses)
                    x_ticks.append(i)
                fig = Visualiser.draw_column_graph(column_data, 'responses', x_ticks, q[1])
                fig.savefig('./surveyapp/static/{0}{1}{2}'.format(self.__sname, self.__session, q[0]))
                filenames.append('{0}{1}{2}'.format(self.__sname, self.__session, q[0]))
        return filenames
    
    
    @staticmethod
    def draw_column_graph(data:list, y:str, x:list, title:str):
        plt.rcdefaults()
        fig, ax = plt.subplots()
        xs = np.arange(len(x))
        width = 0.35
        #print(data)
        ax.bar(xs, data, width, align='center', color='#343a40', ecolor='black')
        ax.set_xticks(xs)
        ax.set_xticklabels(x)
        ax.set_ylabel(y)
        ax.set_title(title)
        return fig
    
