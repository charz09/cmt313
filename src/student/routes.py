from flask import render_template
from . import student
# from flask_login import login_required


# View all assessment attempts
@student.route('/')
def index():
    return render_template('student/index.html')
# @login_required


# Create new Assessment attempt

# View assessment attempt

# Edit assessment attempt

# Delete assessment attempt


# View question attempt

# Edit question attempt

# Delete question attempt
