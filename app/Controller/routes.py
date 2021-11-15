from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config

from app import db
from app.Model.models import Post, Major, Student, postMajors, Faculty
from app.Controller.forms import PostForm, ProfileForm, SortForm
from flask_login import current_user, login_user, logout_user, login_required


bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'

# ================================================================
#   Name:           Index Route
#   Description:    index route for basic flask implementation
#   Last Changed:   11/12/21
#   Changed By:     Reagan Kelley
#   Change Details: Added posts query to get all position posts
# ================================================================
@bp_routes.route('/', methods=['GET', 'POST'])
@bp_routes.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    posts = Post.query.order_by(Post.timestamp.desc())
    sform = SortForm()
    if sform.validate_on_submit():
        if (sform.checkbox.data == True):
            posts = current_user.get_user_posts()
    return render_template('index.html', title="Lab Opportunities", posts=posts.all(), post_count = posts.count(), form= sform)

# ================================================================
#   Name:           Post Position Route
#   Description:    Post Position route for basic flask implementation
#   Last Changed:   11/11/21
#   Changed By:     Reagan Kelley
#   Change Details: Adjustments to compensate for new database model 
# ================================================================
@bp_routes.route('/postposition', methods=['GET', 'POST'])
@login_required
def postposition():
    if current_user.get_user_type() == 'Student':
        flash('You do not have permission to access this page.')
        return redirect(url_for('routes.index'))
    pForm = PostForm()
    if pForm.validate_on_submit():
        newPost = Post(user_id = current_user.id, title=pForm.title.data, body = pForm.body.data, majors = pForm.majors.data)
        db.session.add(newPost)
        db.session.commit()
        flash('New Position Post "' + newPost.title + '" is on the Job Board!')
        return redirect(url_for('routes.index'))

    return render_template('create.html', title="New Post", form = pForm)

# ================================================================
#   Name:           Student Profile Update Route
#   Description:    Updates the student profile with inputed information
#   Last Changed:   11/14/21
#   Changed By:     Denise Tanumihardja
#   Change Details: Initial Implementation
# ================================================================

@bp_routes.route('/student_profile', methods=['GET'])
@login_required
def student_profile():
    student_profile = Student.query.filter_by(id = current_user.id).first()
    print(student_profile.wsu_id)

    return render_template('profile.html', title="Student Profile", profile = student_profile)

# ================================================================
#   Name:           Student Profile Update Route
#   Description:    Updates the student profile with inputed information
#   Last Changed:   11/15/21
#   Changed By:     Reagan Kelley
#   Change Details: Worked on current bug with updating user info
#                   (still broken)
# ================================================================

@bp_routes.route('/student_profile_update', methods=['GET', 'POST'])
@login_required
def update_student_profile():
    proForm = ProfileForm()
    if proForm.validate_on_submit():
        print('Validated')

        # update current user with form info
        current_user.wsu_id = proForm.wsu_id.data
        current_user.first_name = proForm.first_name.data
        current_user.last_name = proForm.last_name.data
        current_user.phone_no = proForm.phone_no.data
        current_user.major = 'To be Implemented'
        current_user.gpa = proForm.gpa.data
        current_user.expected_grad_date = proForm.expected_grad_date.data
        current_user.elect_courses = proForm.elect_courses.data
        current_user.research_topics = 'To be Implemented'
        current_user.languages = proForm.languages.data
        current_user.prior_research = proForm.prior_research.data

        # commit changes
        db.session.add(current_user)
        db.session.commit()
        flash('Profile Successfully Updated!')
        return redirect(url_for('routes.student_profile'))
    return render_template('updateprofile.html', title = "Student Profile", update = proForm, user = current_user)
        