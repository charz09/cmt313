from flask import render_template
from . import teacher


@teacher.route('/')
def index():
    return render_template('teacher/index.html')


# View All Assessments

# Create Assessment

# Read Assessment

# Edit Assessment

# Delete Assessment


# View All Questions

# Create Question

# Read Question

# Edit Question

# Delete Question
