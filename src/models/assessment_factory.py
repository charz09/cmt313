# src/models/assessment_factory.py
from flask_login import current_user
from src import db
from src.models.feedback import Attempts
from src.models.user import User
from .answer import Answer


def create_assessment():
    from src.models.assessment import Assessment
    return Assessment


