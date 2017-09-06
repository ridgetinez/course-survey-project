from abc import ABCMeta, abstractmethod
from ast import literal_eval
import csv


class CSVReader(metaclass=ABCMeta):
    """ Super-class for reading specific DB formats

    Args:
    file -- string containing the file to read from
    """

    @abstractmethod
    def read(self):
        pass

class CourseReader(CSVReader):
    """ Reads from a course CSV file """

    def read(self, path):
        """ Reads a file containing all the courses into a list

        Args:
        path -- string of the path to file holding the courses in CSV form
        """

        course_reader = csv.reader(open(path, 'r', newline=''), delimiter=' ')
        return list(course_reader)[1:]

class SurveyReader(CSVReader):
    """ Reads from a course CSV file """

    def read(self, path):
        """ Reads a file containing all the courses into a list

        Args:
        path -- string of the path to file holding the courses in CSV form
        """

        survey_reader = csv.reader(open(path, 'r', newline=''), delimiter=' ')
        unstringify = [[literal_eval(x[0]), literal_eval(x[1]), literal_eval(x[2])] for x in survey_reader]
        return unstringify

