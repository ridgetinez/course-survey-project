from models import Question, QuestionPool


# Question Tests

firstQ = Question("How fucked are you for 1531?", ["Yes", "Yes in green", "si est verte"])
print(firstQ)
firstQ.add_answer_option("<3")
print(firstQ)
print(firstQ.qid)
secondQ = Question("Did you really sleep when you have 1531?", ["Yes", "No", "No in yes."])
print(secondQ.qid)


# QuestionPool Tests
qp = QuestionPool([firstQ, secondQ])
for q in qp:
    print(q) 
        