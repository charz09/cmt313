from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app():

    app = Flask(__name__, instance_relative_config=False)

    # configure app using the Config class defined in src/config.py
    app.config.from_object('src.config.Config')

    db.init_app(app)  # initialise the database for the app

    with app.app_context():
        # this import allows us to create the table if it does not exist
        from src.models.user import User
        db.create_all()

        from src.routes import bp as users_bp
        app.register_blueprint(users_bp)

    return app
