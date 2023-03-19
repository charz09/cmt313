from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

from . import routes
