from datetime import datetime, timedelta
import random


def seed(db, Role, User, Assessment, Question, Choice, Attempt, Answer, Module):

    # delete the database
    db.drop_all()

    # craete the database tables
    db.create_all()

    # craete the Roles
    student = Role()
    teacher = Role()

    # give them a name
    student.name = "Student"
    teacher.name = "Teacher"

    # add them to the db session
    db.session.add(student)
    db.session.add(teacher)

    # commit changes to the database
    db.session.commit()

    # create the modules
    module1 = Module.create("Web Development", "313")
    module2 = Module.create("Fundermentals of Programming", "224")
    module3 = Module.create("Data Structures & Algorithms", "120")

    # craete students
    jess = User.create('Jess', "password", student.id)
    adam = User.create('Adam', "password", student.id)

    jess.modules.append(module1)
    jess.modules.append(module2)

    # create teachers
    matt = User.create('Matt', "password", teacher.id)
    sara = User.create('Sara', "password", teacher.id)

    matt.modules.append(module2)
    matt.modules.append(module3)


# A1
    js_assessment = Assessment.create("Javascript Quiz",  # quiz name
                                      True,  # visible
                                      "Simple javascript quiz on basics.",  # description
                                      module1.id,  # module code
                                      "Summative",  # Assessment Type: Formative or Summative
                                      matt.id,  # assign a user_id
                                      datetime.utcnow() + timedelta(minutes=1),  # time assessment available from
                                      datetime.utcnow() + timedelta(minutes=3),  # time assessment available to
                                      datetime.utcnow() + timedelta(minutes=5)  # time feedback available from
                                      )
    print(js_assessment.module_id)

# Q1
    question = Question.create("Which of the following methods is used to access HTML elements using Javascript?",  # question content
                               js_assessment.id,  # assessment_id
                               'Multiple Choice')  # question type

    Choice.create("getElementById()", True, question.id)
    Choice.create("getElementByItem()", False, question.id)
    Choice.create("getIdByElement()", False, question.id)
    Choice.create("elementSelectorAll()", False, question.id)

# Q2
    question = Question.create("Javascript is an _______ language?",  # question content
                               js_assessment.id,  # assessment_id
                               'Multiple Choice')  # question type

    Choice.create("Object Oriented", True, question.id)
    Choice.create("Object Based", False, question.id)
    Choice.create("Procedural", False, question.id)
    Choice.create("Low Level", False, question.id)

# Q3
    question = Question.create("Which of the following keywords is used to define a variable in Javascript??",  # question content
                               js_assessment.id,  # assessment_id
                               'Multiple Choice')  # question type

    Choice.create("var", False, question.id)
    Choice.create("let", False, question.id)
    Choice.create("const", False, question.id)
    Choice.create("all of the above", True, question.id)

# Q4
    question = Question.create("Upon encountering empty statements, what does the Javascript Interpreter do?",  # question content
                               js_assessment.id,  # assessment_id
                               'Multiple Choice')  # question type

    Choice.create("Throw an error", False, question.id)
    Choice.create("Ignores the statement", True, question.id)
    Choice.create("Give a warning", False, question.id)
    Choice.create("None of the above", False, question.id)

# Q5
    question = Question.create("""What will be the output of the following code snippet?
                               a=5 + "9";
                               document.write(a)""",  # question content
                               js_assessment.id,  # assessment_id
                               'Multiple Choice')  # question type

    Choice.create("Runtime Error", False, question.id)
    Choice.create("14", False, question.id)
    Choice.create("59", True, question.id)
    Choice.create("Compilation Error", False, question.id)

# Q6
    question = Question.create("When an operator’s value is NULL, the typeof returned by the unary operator is",  # question content
                               js_assessment.id,  # assessment_id
                               'Multiple Choice')  # question type

    Choice.create("Boolean", False, question.id)
    Choice.create("Undefined", False, question.id)
    Choice.create("Object", True, question.id)
    Choice.create("Integer", False, question.id)

# Q7
    question = Question.create("""What will be the output of the following code snippet?
    var a = Math.max();
    var b = Math.min();
    print(a);
    print(b);
""",  # question content
                               js_assessment.id,  # assessment_id
                               'Multiple Choice')  # question type

    Choice.create("-Infinity Infinity", True, question.id)
    Choice.create("Infinity -Infinity", False, question.id)
    Choice.create("Infinity Infinity", False, question.id)
    Choice.create("None of the above", False, question.id)

# Q8
    question = Question.create("""What will be the output of the following code snippet?
var a = true + true + true * 3;
print(a)""",  # question content
                               js_assessment.id,  # assessment_id
                               'Multiple Choice')  # question type

    Choice.create("0", False, question.id)
    Choice.create("5", False, question.id)
    Choice.create("3", True, question.id)
    Choice.create("Error", False, question.id)

# Q9
    question = Question.create("What does the ‘toLocateString()’ method do in JS?",  # question content
                               js_assessment.id,  # assessment_id
                               'Multiple Choice')  # question type

    Choice.create("Returns a parsed string.", False, question.id)
    Choice.create(
        "Returns a localized string representation of an object.", True, question.id)
    Choice.create("Returns a localised object representation.",
                  False, question.id)
    Choice.create("None of the above", False, question.id)

# Q10
    question = Question.create("Which function is used to serialize an object into a JSON string in Javascript?",  # question content
                               js_assessment.id,  # assessment_id
                               'Multiple Choice')  # question type

    Choice.create("stringify()", True, question.id)
    Choice.create("parse()", False, question.id)
    Choice.create("convert()", False, question.id)
    Choice.create("toJSON()", False, question.id)

# A2
    python_assessment = Assessment.create("Python Quiz",
                                          True,
                                          "Harder Python quiz on classes.",
                                          module2.id,
                                          "Summative",
                                          matt.id,
                                          datetime.utcnow() + timedelta(minutes=0),
                                          datetime.utcnow() + timedelta(minutes=0.5),
                                          datetime.utcnow() + timedelta(minutes=1)
                                          )

# Q1
    question = Question.create("Which of the following functions is a built-in function in python?",  # question content
                               python_assessment.id,  # assessment_id
                               'Multiple Choice')  # question type

    Choice.create("factorial()", False, question.id)
    Choice.create("print()", False, question.id)
    Choice.create("seed()", False, question.id)
    Choice.create("sqrt()", True, question.id)

# Q2
    question = Question.create("""What will be the output of the following Python function?
    min(max(False,-3,-4), 2,7)""",  # question content
                               python_assessment.id,  # assessment_id
                               'Multiple Choice')  # question type

    Choice.create("-4", False, question.id)
    Choice.create("-3", True, question.id)
    Choice.create("2", False, question.id)
    Choice.create("False", False, question.id)

# Q2
    question = Question.create("Which of the following is not a core data type in Python programming?",  # question content
                               python_assessment.id,  # assessment_id
                               'Multiple Choice')  # question type

    Choice.create("Tuples", False, question.id)
    Choice.create("Lists", False, question.id)
    Choice.create("Class", True, question.id)
    Choice.create("Dictionary", False, question.id)

# Q3
    question = Question.create("""What will be the output of the following Python code snippet?
for i in [1, 2, 3, 4][::-1]:
    print (i)""",  # question content
                               python_assessment.id,  # assessment_id
                               'Multiple Choice')  # question type

    Choice.create("4 3 2 1", True, question.id)
    Choice.create("error", False, question.id)
    Choice.create("1 2 3 4", False, question.id)
    Choice.create("none of the mentioned", False, question.id)

# Q4
    question = Question.create("Which one of the following is not a keyword in Python language?",  # question content
                               python_assessment.id,  # assessment_id
                               'Multiple Choice')  # question type

    Choice.create("pass", False, question.id)
    Choice.create("eval", True, question.id)
    Choice.create("assert", False, question.id)
    Choice.create("nonlocal", False, question.id)

# Q5
    question = Question.create("""What will be the output of the following Python code?
    class tester:
        def __init__(self, id):
            self.id = str(id)
            id="224"

    >>>temp = tester(12)
    >>>print(temp.id)""",  # question content
                               python_assessment.id,  # assessment_id
                               'Multiple Choice')  # question type

    Choice.create("12", False, question.id)
    Choice.create("224", True, question.id)
    Choice.create("None", False, question.id)
    Choice.create("Error", False, question.id)

# Q6
    question = Question.create("Which one of the following is the use of function in python?",  # question content
                               python_assessment.id,  # assessment_id
                               'Multiple Choice')  # question type

    Choice.create(
        "Functions don’t provide better modularity for your application", False, question.id)
    Choice.create("you can’t also create your own functions",
                  False, question.id)
    Choice.create("Functions are reusable pieces of programs",
                  True, question.id)
    Choice.create("All of the mentioned", False, question.id)

# Q7
    question = Question.create("""Which of the following Python statements will result in the output: 6?
A = [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]""",  # question content
                               python_assessment.id,  # assessment_id
                               'Multiple Choice')  # question type

    Choice.create("A[2][1]", False, question.id)
    Choice.create("A[1][2]", True, question.id)
    Choice.create("A[3][2]", False, question.id)
    Choice.create("A[2][3]", False, question.id)

# Q8
    question = Question.create("Which of the following is a Python tuple?",  # question content
                               python_assessment.id,  # assessment_id
                               'Multiple Choice')  # question type

    Choice.create("{1, 2, 3}", False, question.id)
    Choice.create("{}", False, question.id)
    Choice.create("(1, 2, 3)", True, question.id)
    Choice.create("[1, 2, 3]", False, question.id)

# Q9
    question = Question.create("""What will be the output of the following Python code?
print("abc. DEF".capitalize())
""",  # question content
                               python_assessment.id,  # assessment_id
                               'Multiple Choice')  # question type

    Choice.create("Abc. def", True, question.id)
    Choice.create("abc. def", False, question.id)
    Choice.create("Abc. Def", False, question.id)
    Choice.create("ABC. DEF", False, question.id)

# Q10
    question = Question.create("What are the two main types of functions in Python?",  # question content
                               python_assessment.id,  # assessment_id
                               'Multiple Choice')  # question type

    Choice.create("System function", False, question.id)
    Choice.create("Custom function", False, question.id)
    Choice.create("Built-in function & User defined function",
                  True, question.id)
    Choice.create("User function", False, question.id)

# # AT1
#     attempt = Attempt.create(python_assessment.id, jess.id)

#     for question in attempt.assessment.questions:
#         print(question)
#         choices = question.choices
#         correct_choice = [
#             c.content for c in choices if c.is_correct == True][0]
#         choice = random.choice(choices)
#         answer = Answer.create(
#             choice.content, choice.is_correct, correct_choice, attempt.assessment.id, question.id, jess.id)
