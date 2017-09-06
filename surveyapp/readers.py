from abc import abstractmethod
import csv


class CSVReader(object):
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
