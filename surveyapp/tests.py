from writers import CourseLoader, EnrolmentLoader, UserLoader

cloader = CourseLoader()
cloader.csv_to_db("courses.csv")

eloader = EnrolmentLoader()
eloader.csv_to_db("enrolments.csv")
eloader.get_all()

uloader = UserLoader()
uloader.csv_to_db("passwords.csv")
uloader.get_all()
