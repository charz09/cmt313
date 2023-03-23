from flask import render_template
from . import student
from flask_login import login_required, current_user


# View all assessment attempts
@student.route('/')
@login_required
def index():
    print(current_user, current_user.username, current_user.is_authenticated)
    return render_template('student/index.html')


# Create new Assessment attempt

# View assessment attempt

# Edit assessment attempt

# Delete assessment attempt


# View question attempt

# Edit question attempt

# Delete question attempt
