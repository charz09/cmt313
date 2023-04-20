from flask import render_template
from . import student
from ..models.assessment import Assessment
from flask_login import login_required, current_user


# View all assessment attempts
@student.route('/')
@login_required
def index():
    assessments = Assessment.query.all()
    return render_template('student/attempts/index.html', assessments=assessments)

# Create new Assessment attempt

# View assessment attempt

# Edit assessment attempt

# Delete assessment attempt


# View question attempt

# Edit question attempt

# Delete question attempt
