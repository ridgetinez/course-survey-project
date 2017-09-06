from models import Question, QuestionStore, Survey
from writers import ResponseWriter, SurveyWriter
from models import Question, QuestionStore, Survey, Course
from readers import CourseReader, SurveyReader
import unittest
def printStore(store):
    for item in store.get_all_questions():
        print(item)
    print("\n\n")
# Initialise different questions
q1 = Question("A", ['a', 'b', 'c', 'd'])
q2 = Question("B", ['c', 'd', 'e', 'f'])
q3 = Question("C", ['d', 'e', 'f', 'g'])
q4 = Question("D", ['e', 'f', 'g', 'h'])
identical = Question("A", ['a', 'b', 'c', 'd'])
# Place in QuestionStore
store = QuestionStore([q1, q2, q3, q4, identical])
# print out the dictionary that holds the question store
print(store.get_question(q1.id))
printStore(store)
# adding a question to an existing question pool
qNew = Question("E", ['f', 'g', 'h', 'i'])
store.add_question(qNew)
printStore(store)
# adding a duplicate to an existing question pool
store.add_question(qNew)
printStore(store)
# SURVEY TEST
survey = Survey([q1, q2, q3, q4, identical], "COMP6331")
printStore(survey)
print(survey.course)
# RESPONSE WRITER

# SURVEY WRITER  TEST
v = SurveyWriter(survey)
v.append_row(survey)

#SURVEY READER TEST
#sr = SurveyReader()
#for item in sr.read('./static/survey.csv'):
#    print(item)
#print('\n\n')
#surveys = sr.read('./static/survey.csv')
#COMP6331 = Survey([q1, q2, q3, q4, identical], surveys[0][1])
#print(comp6331.id, comp6331.course)
#printStore(COMP6331)



# COURSE READER TEST
cr = CourseReader()
for item in cr.read('./static/courses.csv'):
    print(item)
print('\n\n')
# COURSE TEST
courses = cr.read('./static/courses.csv')
comp2041 = Course(courses[0][0], courses[0][1])
print(comp2041.surveys, comp2041.id)
comp2041.add_survey(survey)
print(comp2041.surveys)
print(comp2041.get_survey(survey.id))