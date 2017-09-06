from abc import abstractmethod, ABCMeta
from ast import literal_eval
import csv
import os

class Writer(metaclass=ABCMeta):
    """ Super class for writers to CSV DB flat files """

    @abstractmethod
    def update_row(self, path):
        pass


class ResponseWriter(Writer):
    """ Writer specific for a survey's response

    Args:
    survey -- responses recorded are for this specific survey
    """

    def __init__(self, survey):
        self.__csv_path = './static/{0}.csv'.format(survey.id)
        try:
            self.__csv_file = open(self.__csv_path)
            self.__csv_file.close()
        except:
            with open(self.__csv_path, 'w') as f:
                response_writer = csv.writer(self.__csv_file, delimiter=' ')
                for q in survey.get_all_questions():
                    response_writer.writerow([q.id, q.num_answers*[0]])

    def __csv_to_list(self, qid, ans_index):
        """ Convert csv response file to nested list """
        with open(self.__csv_path, 'r') as f:
            tmp_list = list(csv.reader(f, delimiter=' '))
            unstringify = [[literal_eval(x[0]), literal_eval(x[1])] for x in tmp_list]
            return unstringify

    def update_row(self, qid, ans_index):
        """ Increment csv to add a response to a given question """
        l = self.__csv_to_list(qid, ans_index)
        row = [x for x in l if qid in x][0]
        l[l.index(row)][1][ans_index] += 1
        with open(self.__csv_path, 'w') as f:
            response_writer = csv.writer(f, delimiter=' ')
            for q in l:
                response_writer.writerow(q)
