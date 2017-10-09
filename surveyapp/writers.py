from abc import abstractmethod, ABCMeta
from ast import literal_eval
import csv


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
        self.__csv_path = 'surveyapp/static/response{0}.csv'.format(survey.id)
        try:
            self.__csv_file = open(self.__csv_path)
            self.__csv_file.close()
        except:
            with open(self.__csv_path, 'w') as f:
                response_writer = csv.writer(f, delimiter=' ')
                for q in survey.get_all_questions():
                    response_writer.writerow([q.id, len(q.answer_list)*[0]])

    def __csv_to_list(self, qid, ans_index):
        """ Convert csv response file to nested list """
        with open(self.__csv_path, 'r') as f:
            tmp_list = list(csv.reader(f, delimiter=' '))
            unstringify = [[literal_eval(x[0]), literal_eval(x[1])] for x in tmp_list]
            print(unstringify)
            return unstringify

    def update_row(self, qid, ans_index):
        """ Increment csv to add a response to a given question """
        l = self.__csv_to_list(qid, ans_index)
        # for i, x in enumerate(l):
        #     if int(qid) in x:
        #         l[i][1][int(ans_index)] += 1
        row = [x for x in l if int(qid) in x][0]
        l[l.index(row)][1][int(ans_index)] += 1
        with open(self.__csv_path, 'w') as f:
            response_writer = csv.writer(f, delimiter=' ')
            for q in l:
                response_writer.writerow(q)


class QuestionWriter(Writer):
    """ Writer specific for question instances """

    def __init__(self):
        self.__csv_path = './static/questions.csv'
        with open(self.__csv_path, 'w') as f:
            pass

    def append_row(self, q):
        """ Appends a row, saving question fields to flat file CSV
        Question in CSV is formatted: qid | question_text | answers_list

        Args:
        q -- question instance to be saved into csv
        """
        keys = ['QID', 'Q_TEXT', 'ANS_LIST']
        with open(self.__csv_path, 'a') as f:
            q_writer = csv.DictWriter(f, fieldnames=keys)
            q_writer.writerow({keys[0]: q.id, keys[1]: q.text, keys[2]: q.answer_list})
