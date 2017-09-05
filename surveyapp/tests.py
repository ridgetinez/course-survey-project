from models import Question, QuestionStore
import unittest

# Initialise different questions
q1 = Question("A", ['a', 'b', 'c', 'd'])
q2 = Question("B", ['c', 'd', 'e', 'f'])
q3 = Question("C", ['d', 'e', 'f', 'g'])
q4 = Question("D", ['e', 'f', 'g', 'h'])
identical = Question("A", ['a', 'b', 'c', 'd'])

# Place in QuestionStore
store = QuestionStore([q1, q2, q3, q4, identical])

# print out the dictionary that holds the question store
print(store)            # prints out address
