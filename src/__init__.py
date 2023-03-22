from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Create the database
db = SQLAlchemy()


def init_app():  # Factory function for creating app instance

    # initialise app instance
    app = Flask(__name__, instance_relative_config=False)

    # configure app using the Config class defined in src/config.py
    app.config.from_object('src.config.Config')

    # initialise the database using the app instance
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'

    with app.app_context():
        # this import allows us to create the table if it does not exist
        from src.models.user import User
        db.create_all()

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

        return app
