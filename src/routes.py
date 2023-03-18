from flask import Blueprint, render_template
from src.models.user import User

bp = Blueprint('users', __name__)


@bp.route('/')
def index():
    return render_template('home.html')
