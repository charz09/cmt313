from flask import Blueprint

# #############################
# from flask import Flask
# from .routes import teacher
# from .comments import comments
# from . import db
# ###############################

# app = Flask(__name__)
# app.config.from_object('config')

# app.register_blueprint(teacher)
# app.register_blueprint(comments)
# db.init_app(app)








teacher = Blueprint('teachers', __name__, url_prefix='/teacher')

from . import routes
