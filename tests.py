"""
tests.py ... contains unit testing for the survey
"""

import unittest # Vital library used for unit tests
from surveyapp import * # Import all associated functions/variables from surveyapp's files
import sqlite3
#from writers import CourseLoader, EnrolmentLoader, UserLoader # Functions to use for testing
# TODO: i may need more
import datetime
# --------------------------------------------------------------------------------------------
class Test_Creation_of_Survey(unittest.TestCase):
    def test_creation_valid(self):

        now = datetime.datetime.now()
        later = datetime.datetime.now() + datetime.timedelta(minutes=1)
        modelcontrollers.SurveyController.write_survey("COMP1531", "17s2", now, later, [0])
        survey = modelcontrollers.SurveyController.get_survey("COMP1531", "17s2")
        self.assertNotEqual(survey, None)
        self.assertEqual(survey.course_name, "COMP1531")
        self.assertEqual(survey.course_session, "17s2")
        self.assertEqual(survey.starttime, now)
        self.assertEqual(survey.endtime,  later)
        self.assertEqual(survey.state, 'review')

    def test_creation_duplicates(self):
        now = datetime.datetime.now()
        later = datetime.datetime.now() + datetime.timedelta(minutes=1)
        modelcontrollers.SurveyController.write_survey("COMP3421", "18s2", now, later, [0])
        success = modelcontrollers.SurveyController.write_survey("COMP3421", "18s2", now, later, [0])
        self.assertEqual(success, False)

    def test_get_invalid_survey(self):
        survey = modelcontrollers.SurveyController.get_survey("COMP1531", "20s2")
        self.assertEqual(survey, None)

    def tearDown(self):
        pass

class Test_CSV_Loaders(unittest.TestCase):
    def test_course(self):
        course = modelcontrollers.CourseController.get_courses()
        self.assertNotEqual(course, None)

    def test_enrolment(self):
        enrolment = modelcontrollers.EnrolmentController.get_enrolment('50')
        self.assertNotEqual(enrolment, None)

    def test_user(self):
        user = modelcontrollers.UserController.get_user('51')
        self.assertNotEqual(user, None)

class Test_User(unittest.TestCase):
    def test_guest(self):
        modelcontrollers.UserController.write_user(['Minjie', 'password', 'guest', 'COMP1521 17s1'])
        guests = modelcontrollers.UserController.get_unnaproved_guests()
        self.assertEqual(guests[0].uid, 'Minjie')

    def test_duplicate_user(self):
        success = modelcontrollers.UserController.write_user(['Minjie', 'password', 'guest', 'COMP1521 17s1'])
        self.assertNotEqual(success, False)
# ---------------------------------------------------------------------------------------------

from surveyapp import modelcontrollers

modelcontrollers.CSVloader.get_users_csv()  # loads .csv files
modelcontrollers.CSVloader.get_course_csv()
modelcontrollers.CSVloader.get_enrolement_csv()

modelcontrollers.QuestionController.write_question([['text'], ['a1', 'a2'], 'False'])

# --------------------------------------------------------------------------------------------
if __name__=="__main__":
    #   Runs the tests
    unittest.main()
# ---------------------------------------------------------------------------------------------
"""
-----------------------------------------------------------
 THE CODE BELOW WAS USED AS REFERENCE
-------------------------------------------------------------
"""
