from flask import Blueprint, render_template

comments = Blueprint('comments', __name__)

@comments.route('/comments')
def comments_index():
    # This is where you would retrieve comments from the database
    comments = []

    return render_template('comments/index.html', comments=comments)
