import factory
from factory.alchemy import SQLAlchemyModelFactory
from src.extensions import db
from src.models.user import User
from src.models.role import Role
from src.models.assessment import Assessment
from src.models.attempt import Attempt
from src.models.question import Question
from src.models.choice import Choice
from src.models.answer import Answer

class RoleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Role
        sqlalchemy_session = db.session

    name = factory.Sequence(lambda n: f"Role {n}")

class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.Faker("password")
    role = factory.SubFactory(RoleFactory)

class AssessmentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Assessment
        sqlalchemy_session = db.session

    name = factory.Sequence(lambda n: f"Assessment {n}")
    assessment_type = 'Summative'
    description = factory.Faker("text")
    module = factory.Faker("word")
    created_by = factory.SubFactory(UserFactory)

class QuestionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Question
        sqlalchemy_session = db.session

    content = factory.Faker("text")
    assessment = factory.SubFactory(AssessmentFactory)
    question_type = factory.Faker("word")
    user = factory.SubFactory(UserFactory)

class ChoiceFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Choice
        sqlalchemy_session = db.session

    content = factory.Faker("text")
    is_correct = factory.Faker("pybool")
    question = factory.SubFactory(QuestionFactory)

class AttemptFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Attempt
        sqlalchemy_session = db.session

    user_score = factory.Faker("pyint")
    total_score = factory.Faker("pyint")
    assessment = factory.SubFactory(AssessmentFactory)
    created_by = factory.SubFactory(UserFactory)

class AnswerFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Answer
        sqlalchemy_session = db.session

    content = factory.Faker("text")
    is_correct = factory.Faker("pybool")
    correct_answer = factory.Faker("text")
    attempt = factory.SubFactory(AttemptFactory)
    question = factory.SubFactory(QuestionFactory)