""" Derek Daquel
- Sample unit test set up from the iteration 3 specs
- Need to test 5 core user stories. Ones I am currently testing are:
    ADMIN - creation of course survey
    USER - submitting the course survey
    STAFF - review of survey
- General set up of unit test
    1. import unittest
    2. set up a class with (unittest.TestCase)
    3. have a setup() function
    4. set up multiple tests starting with "test_...()"
    5. have a teardown() function
    6. compile/execute using python3 -m unittest -v test.py
"""

import unittest # Vital library used for unit tests
from surveyapp import * # Import all associated functions/variables from surveyapp's files
from writers import CourseLoader, EnrolmentLoader, UserLoader # Functions to use for testing
# TODO: i may need more

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

    def setup(self):
        """
        Load appropriate .csv's for testing
        """

        db.create_all()
        cloader = CourseLoader()
        cloader.csv_to_db("static/courses.csv")
        eloader = EnrolmentLoader()
        eloader.csv_to_db("static/enrolments.csv")
        eloader.get_all()
        uloader = UserLoader()
        uloader.csv_to_db("static/passwords.csv")
        uloader.get_all()

    def test_valid_number_questions(self):
        """
            :pre : pre condition message
            :post : post condition message
        """

        self.assertGreater(n_chosen_questions, 1)

    def test_valid_start_end_time(self):
    """
        :pre : pre condition message
        :post : post condition message
    """

        start_time = models.Survey.time
        end_time = models.Survey.endtime
        self.assertGreater(start_time, end_time);

    def test_valid_creation(self):
    """
        :pre : pre condition message
        :post : post condition message
    """

    def test_availability_in_staff_review(self):
    """
        :pre : pre condition message
        :post : post condition message
    """
        survey = session.query(models.Survey).filter(models.Survey.course_name == survey.course_name).filter(models.Survey.course_session == survey.course_session).first()
        modelcontrollers.SurveyController.set_review_after_start()
        assertEqual(survey.state, 'review')

    def teardown(self):
        db.session.remove()
        db.drop_all()
# ------------------------------------------------------------------------------------------------------
class Test_Submitting_Of_Course_Survey(unittest.TestCase):
    """
    ACCEPTANCE CRITERIA
    - On clicking “SUBMIT” checks are made to ensure each question has one answer (no blank responses).
    - Reroutes to student dashboard with header notification thanking the student for answering the survey.
    - The survey that was just completed should not be viewable from the student’s dashboard.
    - Invariant: If the student has already submitted the survey, they cannot access the survey to complete another row of data
    """

    def setup(self):
        db.create_all()
        cloader = CourseLoader()
        cloader.csv_to_db("static/courses.csv")
        eloader = EnrolmentLoader()
        eloader.csv_to_db("static/enrolments.csv")
        eloader.get_all()
        uloader = UserLoader()
        uloader.csv_to_db("static/passwords.csv")
        uloader.get_all()
    def test_valid_responses(self):

    #def test_notification_and_reroute(self):

    def test_availability_of_completed_survey(self):

    def test_valid_write_to_db(self):

    def teardown(self):
        db.session.remove()
        db.drop_all()
# --------------------------------------------------------------------------------------
class Test_Staff_Review(unittest.TestCase):
    """
    ACCEPTANCE CRITERIA
    - On the staff dashboard, any surveys available for review will be displayed.
    - Clicking on Review of a particular survey will direct staff to a page with the list of questions on the page. None of these questions will be actionable by the staff.
    - Clicking on Publish will successfully finish the review process of the survey from the staff.
    - Given that the survey’s start date is in the past, the survey is now available on student’s enrolled in that survey’s course.
    """
    def setup(self):
        db.create_all()
        cloader = CourseLoader()
        cloader.csv_to_db("static/courses.csv")
        eloader = EnrolmentLoader()
        eloader.csv_to_db("static/enrolments.csv")
        eloader.get_all()
        uloader = UserLoader()
        uloader.csv_to_db("static/passwords.csv")
        uloader.get_all()
    def test_survey_state_change(self):

    def teardown(self):
        db.session.remove()
        db.drop_all()
# -------------------------------------------------------------------
if __name__=="__main__":
    """
    """
    Runs the tests
    unittest.main()
# --------------------------------------------------------------------




"""
-----------------------------------------------------------
 THE CODE BELOW WAS USED AS REFERENCE
-------------------------------------------------------------
"""

"""
import unittest
import os
from server import db
from dbInteractions import *
from Model import *

class TestEnrolment(unittest.TestCase):

    def setUp(self):
        db.create_all()
        read_all_courses('../courses.csv')
        read_passwords('../passwords.csv')
        read_all_enrolments('../Student_enrolments.csv')

    def test_enrol_student_invalid_course(self):
        """
        #:post : There will be no changes in the database
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
        #:pre  : The student isn't already enrolled in the course
        #:post : The database will have a relationship between
        #        the course offering and the student
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
        #:pre  : The student isn't already enrolled in the course
        #:post : The database will have a relationship between
        #        the course offering and the student
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
        #:pre  : The student isn't already enrolled in the course
        #:post : The database will have a relationship between
        #        the course offering and the student
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
        #Create table for tests
        """
        db.create_all()
        os.system("chmod 766 unique.db")

    def test_add_staff_invalid_id(self):
        """
        #:post : No new additions will appear in the db table
        """
        staff_id = ""
        num_staff = len(get_staff(all=True))
        with self.assertRaises(InvalidInputException):
            add_staff(staff_id)

        cur_num_staff = len(get_staff(all=True))
        self.assertEqual(num_staff, cur_num_staff)

    def test_add_staff_valid_id(self):
        """
        #:pre : The staff member to be inserted doesn't exist yet
        #:post : A new staff member will be added to the table
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

if __name__=="__main__":
    unittest.main()
"""
