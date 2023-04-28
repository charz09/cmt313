def seed(db, Role, User, Assessment):
    print("Starting Seed file!!")
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

    # craete users
    jess = User.create('Jess', "password", student.id)
    matt = User.create('Matt', "password", teacher.id)

    Assessment.create("Javascript Quiz",  # quiz name
                      True,  # visible
                      "Simple javascript quiz on basics.",  # description
                      "210",  # module
                      "Formative",  # Assessment Type: Formative or Summative
                      matt.id  # assign a user id
                      )

    Assessment.create("Python Quiz",
                      True,
                      "Harder Pythin quiz on classes.",
                      "313",
                      "Summative",
                      matt.id
                      )

    Assessment.create("Java Quiz",
                      True,
                      "Jav quiz on design patterns.",
                      "130",
                      "Formative",
                      matt.id
                      )

    Assessment.create("Data Structures and Algorithms Quiz",
                      True,
                      "Hardeest quiz on Data Structures and Algorithms.",
                      "330",
                      "Summative",
                      matt.id,
                      )
