from flask import render_template
from . import student


# View all assessment attempts
@student.route('/')
def index():
    return render_template('student/index.html')


# Create new Assessment attempt

# View assessment attempt

# Edit assessment attempt

# Delete assessment attempt


# View question attempt

# Edit question attempt

# Delete question attempt
