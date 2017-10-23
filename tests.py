"""
tests.py ... contains unit testing for the survey

Helpful instructions:

- Need to test 5 core user stories
    USER - submitting the course survey ----> dont do this yet
    STAFF - review of survey ---------------> dont do this yet
- NOTE: I MUST TEST THE FOLLOWING
    1. create mandatory/optional questions
    2. create a survey
    3. enrol a student
- General set up of unit test
    1. import unittest
    2. set up a class with (unittest.TestCase)
    3. have a setup() function
    4. set up multiple tests starting with "test_" and ending in "in/valid"
    5. have a teardown() function
    6. compile/execute using python3 -m unittest -v test.py
- Docstrings include detail of what should happens
        :pre : pre condition message
        :post : post condition message
"""

import unittest # Vital library used for unit tests
from surveyapp import * # Import all associated functions/variables from surveyapp's files
#from writers import CourseLoader, EnrolmentLoader, UserLoader # Functions to use for testing
# TODO: i may need more
import datetime
# --------------------------------------------------------------------------------------------
class Test_Creation_of_Survey(unittest.TestCase):

    """
    ACCEPTANCE CRITERIA (BACKEND):
    - Admin can click on Create Survey button from the dashboard to begin creating survey.
    - Admin can identify which course and session this survey is specifically for.
    - Admin can select any number of questions of any type to be in the survey. They must at least choose one question to appear in the survey.
    - Admin can select a start time and end time for the survey.
    - Admin finalises survey creation by pressing Create button.
    - This newly created survey should be in Review state and is available on the associated staff for final review.
    - Admin can view the state of the newly created survey from their dashboard
    """

    def setUp(self):
        """
        Load appropriate .csv's for testing and start database session
        """
        self.surveys = modelcontrollers.SurveyController()

    def test_start_end_time_valid(self):
        questions = ["A", ["Hello", "Hey"]]
        now = datetime.datetime.now()
        later = datetime.datetime.now() + datetime.timedelta(minutes=10)
        modelcontrollers.SurveyController.write_survey("COMP1531", "17s2", now, later, questions)
        survey = modelcontrollers.SurveyController.get_survey("COMP1531", "17s2")
        self.assertNotEqual(survey, None)
        start_time = datetime.datetime.now()
        end_time = survey.endtime
        self.assertSmaller(start_time, end_time);

    def test_start_end_time_invalid(self):
        questions = ["A", ["Hello", "Hey"]]
        now = datetime.datetime.now()
        before = datetime.datetime.now() - datetime.timedelta(minutes=10)
        modelcontrollers.SurveyController.write_survey("COMP1531", "17s2", now, before, questions)
        survey = modelcontrollers.SurveyController.get_survey("COMP1531", "17s2")
        self.assertNotEqual(survey, None)
        start_time = datetime.datetime.now()
        end_time = survey.endtime
        self.assertGreater(start_time, end_time);

    def test_creation_valid(self):

        questions = ["A", ["Hello", "Hey"]]
        now = datetime.datetime.now()
        later = datetime.datetime.now() + datetime.timedelta(minutes=1)
        modelcontrollers.SurveyController.write_survey("COMP1531", "17s2", now, later, questions)
        survey = modelcontrollers.SurveyController.get_survey("COMP1531", "17s2")
        self.assertNotEqual(survey, None)
        self.assertEqual(survey.course_name, "COMP1531")
        self.assertEqual(survey.course_session, "17s2")
        self.assertEqual(survey.starttime, now)
        self.assertEqual(survey.endtime,  later)
        self.assertEqual(survey.state, 'review')
        self.assertEqual(survey.questions, questions) #need to implement

    def test_creation_duplicates(self):
        questions = ["A", ["Hello", "Hey"]]
        now = datetime.datetime.now()
        later = datetime.datetime.now() + datetime.timedelta(minutes=1)
        modelcontrollers.SurveyController.write_survey("COMP1531", "17s2", now, later, questions)
        with self.assertRaises(exc.IntegrityError):
            modelcontrollers.SurveyController.write_survey("COMP1531", "17s2", now, later, questions)

    def test_availability_in_staff_review(self):

        survey = session.query(models.Survey).filter(models.Survey.course_name == survey.course_name).filter(models.Survey.course_session == survey.course_session).first()
        modelcontrollers.SurveyController.set_review_after_start()
        assertEqual(survey.state, 'review')

    def tearDown(self):
        pass
# ---------------------------------------------------------------------------------------------


engine = create_engine('sqlite:///tests.db')

from surveyapp import models

try:
    Base.metadata.create_all(engine) # Creates database if not there already
except:
    print('Table already there.')

# --------------------------------------------------------------------------------------------
if __name__=="__main__":
    #   Runs the tests
    unittest.main()
# ---------------------------------------------------------------------------------------------

from surveyapp import modelcontrollers

modelcontrollers.CSVloader.get_users_csv()  # loads .csv files
modelcontrollers.CSVloader.get_course_csv()
modelcontrollers.CSVloader.get_enrolement_csv()
"""
-----------------------------------------------------------
 THE CODE BELOW WAS USED AS REFERENCE
-------------------------------------------------------------
"""
