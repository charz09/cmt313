from flask import Blueprint, render_template

bp = Blueprint('teachers', __name__, url_prefix='/teacher')


@bp.route('/')
def index():
    return render_template('teacher.html')
