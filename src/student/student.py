from flask import Blueprint, render_template

bp = Blueprint('students', __name__, url_prefix='/student')


@bp.route('/')
def index():
    return render_template('student/index.html')
