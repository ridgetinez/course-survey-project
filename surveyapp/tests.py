""" Derek Daquel
- Sample unit test set up from the iteration 3 specs
- Need to test 5 core user stories. Ones I am currently testing are:
    ADMIN - creation of course survey
    USER - submitting the course survey
    STAFF - review of survey
"""

# Vital library used for unit tests
import unittest

# not sure what todo with the below
import os
from server import db
from dbInteractions import *
from models import *
# -----------------------------------

from writers import CourseLoader, EnrolmentLoader, UserLoader

class Test_Creation_of_Survey(unittest.TestCase):

    """
    ACCEPTANCE CRITERIA:
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
        Load appropriate .csv's for testing
        """
        #db.create_all()
        cloader = CourseLoader()
        cloader.csv_to_db("static/courses.csv")
        eloader = EnrolmentLoader()
        eloader.csv_to_db("static/enrolments.csv")
        eloader.get_all()
        uloader = UserLoader()
        uloader.csv_to_db("static/passwords.csv")
        uloader.get_all()

    # TODO: create appropriate tests for create survey
    def test_valid_create_survey_button(self):
    """
    docstrings to detail what should happen
    e.g.
        :pre : pre condition message
        :post : post condition message
    """
    def test_valid_course_session_options(self):
        etc etc

    def test_valid_number_questions(self):

    def test_valid_start_end_time(self):

    def test_valid_creation(self):

    def test_availability_in_staff_review(self):

class Test_Submitting_Of_Course_Survey(unittest.TestCase):
    """
    ACCEPTANCE CRITERIA
    - On clicking “SUBMIT” checks are made to ensure each question has one answer (no blank responses).
    - Reroutes to student dashboard with header notification thanking the student for answering the survey.
    - The survey that was just completed should not be viewable from the student’s dashboard.
    - Invariant: If the student has already submitted the survey, they cannot access the survey to complete another row of data
    """

    def setUp(self):

    def test_valid_responses(self):

    def test_notification_and_reroute(self):

    def test_availability_of_completed_survey(self):
        
    def test_valid_write_to_db(self):



if __name__=="__main__":
    """
    Runs the tests
    """
    unittest.main()





"""
-----------------------------------------------------------
 USE BELOW AS REFERENCE
-------------------------------------------------------------
"""

class TestEnrolment(unittest.TestCase):

    def test_enrol_student_invalid_course(self):
        """
        :post : There will be no changes in the database
        """
        zID = 12
        course_offering = ""

        prev_students = num_enrolled_students(course_offering)
        with self.assertRaises(InvalidInputException):
            enrol_user(zID, course_offering)
        curr_students = num_enrolled_students(course_offering)

        self.assertEqual(prev_students, curr_students)
        self.assertEqual(get_user(zID), None)

    def test_enrol_invalid_user(self):
        """
        :pre  : The student isn't already enrolled in the course
        :post : The database will have a relationship between
                the course offering and the student
        """
        zID = "z511"
        course_offering = "COMP1531 17s2"

        prev_students = num_enrolled_students(course_offering)
        with self.assertRaises(InvalidInputException):
            enrol_user(zID, course_offering)
        curr_students = num_enrolled_students(course_offering)

        self.assertEqual(prev_students, curr_students)
        self.assertEqual(get_user(zID), None)

    def test_enrol_non_existent_user(self):
        """
        :pre  : The student isn't already enrolled in the course
        :post : The database will have a relationship between
                the course offering and the student
        """
        zID = 12
        course_offering = "COMP1531 17s2"

        prev_students = num_enrolled_students(course_offering)
        with self.assertRaises(UserNotFoundException):
            enrol_user(zID, course_offering)
        curr_students = num_enrolled_students(course_offering)

        self.assertEqual(prev_students, curr_students)
        self.assertEqual(get_user(zID), None)

    def test_enrol_valid(self):
        """
        :pre  : The student isn't already enrolled in the course
        :post : The database will have a relationship between
                the course offering and the student
        """
        zID = 571
        course_offering = "COMP1531 17s2"
        assert course_offering not in get_user(zID).courses
        prev_students = num_enrolled_students(course_offering)
        enrol_user(zID, course_offering)
        curr_students = num_enrolled_students(course_offering)

        self.assertEqual(prev_students + 1, curr_students)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestAddStaff(unittest.TestCase):

    def setUp(self):
        """
        Create table for tests
        """
        db.create_all()
        os.system("chmod 766 unique.db")

    def test_add_staff_invalid_id(self):
        """
        :post : No new additions will appear in the db table
        """
        staff_id = ""
        num_staff = len(get_staff(all=True))
        with self.assertRaises(InvalidInputException):
            add_staff(staff_id)

        cur_num_staff = len(get_staff(all=True))
        self.assertEqual(num_staff, cur_num_staff)

    def test_add_staff_valid_id(self):
        """
        :pre : The staff member to be inserted doesn't exist yet
        :post : A new staff member will be added to the table
        """
        staff_id = 290
        self.assertEqual(get_staff(290), None)
        num_staff = len(get_staff(all=True))
        add_staff(staff_id)
        cur_num_staff = len(get_staff(all=True))
        self.assertEqual(num_staff + 1, cur_num_staff)
        self.assertNotEqual(get_staff(staff_id), None)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
