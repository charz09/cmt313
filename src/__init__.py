from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from src.seed import seed
from datetime import datetime
# Create the database
db = SQLAlchemy()


def init_app():  # Factory function for creating app instance

    # initialise app instance
    app = Flask(__name__, instance_relative_config=False)

    # configure app using the Config class defined in src/config.py
    app.config.from_object('src.config.Config')
    # print("App Config: ", app.config, "/n #####################################")

    moment = Moment(app)
    moment.init_app(app)

    # initialise the database using the app instance
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    # taken from other project
    # login_manager.login_message_category = 'unsuccessful'

    with app.app_context():
        # imports for use in seed file.
        from src.models.user import User
        from src.models.role import Role
        from src.models.assessment import Assessment
        from src.models.question import Question
        from src.models.choice import Choice
        from src.models.attempt import Attempt
        from src.models.answer import Answer
        from src.models.module import Module

        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        from .auth import auth
        app.register_blueprint(auth)

        from .teacher import teacher
        app.register_blueprint(teacher)

        from .student import student
        app.register_blueprint(student)

        # seed the database with fake user data
        seed(db, Role, User, Assessment, Question,
             Choice, Attempt, Answer, Module)

        return app
