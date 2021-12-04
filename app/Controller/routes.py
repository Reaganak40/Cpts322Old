from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config

from app import db
from app.Model.models import Application, Field, Post, Major, User, Student, Faculty, postMajors
from app.Controller.forms import ApplicationForm, PostForm, ProfileForm, SortForm
from flask_login import current_user, login_user, logout_user, login_required


bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'

# ================================================================
#   Name:           Index Route
#   Description:    index route for basic flask implementation
#   Last Changed:   11/12/21
#   Changed By:     Reagan Kelley
#   Change Details: Added posts query to get all position posts :)
# ================================================================
@bp_routes.route('/', methods=['GET', 'POST'])
@bp_routes.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    posts = Post.query.order_by(Post.timestamp.desc())
    sform = SortForm()
    #print(current_user)
    if sform.validate_on_submit():
        if (sform.checkbox.data == False):
            posts = current_user.get_user_posts()
    return render_template('index.html', title="Lab Opportunities", posts=posts.all(), post_count = posts.count(), form= sform)

# ================================================================
#   Name:           Post Position Route
#   Description:    Post Position route for basic flask implementation
#   Last Changed:   12/1/21
#   Changed By:     Reagan Kelley
#   Change Details: Added time commitment
# ================================================================
@bp_routes.route('/postposition', methods=['GET', 'POST'])
@login_required
def postposition():
    if current_user.get_user_type() == 'student':
        flash('You do not have permission to access this page.')
        return redirect(url_for('routes.index'))
    pForm = PostForm()
    if pForm.validate_on_submit():
        newPost = Post(user_id = current_user.id, 
                       title=pForm.title.data, 
                       body = pForm.body.data, 
                       majors = pForm.majors.data,
                       fields = pForm.fields.data, 
                       time_commitment = pForm.time_commitment.data,
                       start_date = pForm.start_date.data,
                       end_date = pForm.end_date.data)
        db.session.add(newPost)
        db.session.commit()
        flash('New Position Post "' + newPost.title + '" is on the Job Board!')
        return redirect(url_for('routes.index'))

    return render_template('create.html', title="New Post", form = pForm)

# ================================================================
#   Name:           updateposition Route
#   Description:    The Page that allows a faculty to manage an existing
#                   post
#   Last Changed:   12/3/21
#   Changed By:     Reagan Kelley
#   Change Details: Initial Implementation
# ================================================================
@bp_routes.route('/updateposition/<post_id>', methods=['GET', 'POST'])
@login_required
def updateposition(post_id):
    post = Post.query.filter_by(id = post_id).first()

    if(post is None): #if post could not be found
        flash('Could not find this post.')
        return redirect(url_for('routes.index'))
    
    if (post.user_id != current_user.id): # if post does not belong to this user
        flash('You do not have permission to access this page.')
        return redirect(url_for('routes.index'))
    
    pForm = PostForm()

    if request.method == 'GET': # Populate fields with existing data
        pForm.title.data = post.title
        pForm.body.data = post.body
        pForm.time_commitment.data = post.time_commitment
        pForm.start_date.data = post.start_date
        pForm.end_date.data = post.end_date
        pForm.majors.data = post.majors
        pForm.fields.data = post.fields

    if pForm.validate_on_submit():
        post.user_id = current_user.id
        post.title=pForm.title.data
        post.body = pForm.body.data 
        post.majors = pForm.majors.data
        post.fields = pForm.fields.data 
        post.time_commitment = pForm.time_commitment.data
        post.start_date = pForm.start_date.data
        post.end_date = pForm.end_date.data
        db.session.commit()
        flash('Post Edit Successful')
        return redirect(url_for('routes.index'))

    return render_template('updateposition.html', title="Update Post", post = post, form = pForm)
    
# ================================================================
#   Name:           Delete Post
#   Description:    Deletes an existing post
#   Last Changed:   12/3/21
#   Changed By:     Reagan Kelley
#   Change Details: Initial Implementation
# ================================================================
@bp_routes.route('/delete_post/<post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id = post_id).first()
    print('testing')

    if(post is None): #if post could not be found
        flash('Could not find this post.')
        return redirect(url_for('routes.index'))
    
    if (post.user_id != current_user.id): # if post does not belong to this user
        flash('You do not have permission to access this page.')
        return redirect(url_for('routes.index'))

    applications = post.get_applicants()

    for application in applications: # Remove connection in applications
        application.make_phantom()  # Retain post information

    db.session.delete(post)
    db.session.commit()
    #flash('Deleted Post [' + post.title + ']')
    return redirect(url_for('routes.index'))


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
    if(current_user.get_user_type() == 'faculty'):
        flash('You do not have permission to access this page.')
        return redirect(url_for('routes.index'))

    return render_template('profile.html', title="Student Profile", profile = current_user)


# ================================================================
#   Name:           Student Profile Update Route
#   Description:    Updates the student profile with inputed information
#   Last Changed:   11/24/21
#   Changed By:     Reagan Kelley
#   Change Details: Revised to compensate for new database model
# ================================================================
@bp_routes.route('/student_profile_update', methods=['GET', 'POST'])
@login_required
def update_student_profile():
    if(current_user.get_user_type() == 'Faculty'):
        flash('You do not have permission to access this page.')
        return redirect(url_for('routes.index'))
    proForm = ProfileForm()
   

    if request.method == 'GET': # Populate fields with existing data
        proForm.first_name.data = current_user.first_name
        proForm.last_name.data = current_user.last_name
        proForm.wsu_id.data = current_user.wsu_id
        proForm.phone_no.data = current_user.phone_no
        proForm.gpa.data = current_user.gpa
        proForm.expected_grad_date.data = current_user.expected_grad_date
        proForm.elect_courses.data = current_user.elect_courses
        proForm.languages.data = current_user.languages
        proForm.prior_research.data = current_user.prior_research

    if proForm.validate_on_submit():
        
        major_name = Major.query.filter_by(id = (proForm.major.data).id).first()
        if(Student.query.filter_by(wsu_id = proForm.wsu_id.data).count() > 0): ##if wsu_id already exists
            if(Student.query.filter_by(wsu_id = proForm.wsu_id.data).first().wsu_id != current_user.wsu_id): ## if its not your current one
                flash('That WSUID is already in use!')
                return render_template('updateprofile.html', title = "Student Profile", update = proForm, user = current_user)

        # update current user with form info
        current_user.wsu_id = proForm.wsu_id.data
        current_user.first_name = proForm.first_name.data
        current_user.last_name = proForm.last_name.data
        current_user.phone_no = proForm.phone_no.data
        current_user.major = major_name.get_major_name()
        current_user.gpa = proForm.gpa.data
        current_user.expected_grad_date = proForm.expected_grad_date.data
        current_user.elect_courses = proForm.elect_courses.data
        ##current_user.research_topics = research_tags.get_research_field()
        current_user.languages = proForm.languages.data
        current_user.prior_research = proForm.prior_research.data

        # commit changes
        db.session.commit()
        flash('Profile Successfully Updated!')
        return redirect(url_for('routes.student_profile'))
    return render_template('updateprofile.html', title = "Student Profile", update = proForm, user = current_user)

# ================================================================
#   Name:           Apply Route
#   Description:    Backend route to apply to position post
#   Last Changed:   11/16/21
#   Changed By:     Reagan Kelley
#   Change Details: Initial Implementation
# ================================================================
@bp_routes.route('/apply/<postid>/<brief>/<ref>', methods = ['GET', 'POST'])
@login_required
def apply(postid, brief, ref):
    thepost = Post.query.filter_by(id = postid).first()
    if thepost is None:
        flash('Class with id "{}" not found.'.format(postid))
        return redirect(url_for('routes.index'))
    current_user.apply(thepost, brief, ref)
    db.session.commit()
    flash('You applied for: {}!'.format(thepost.title))
    return redirect(url_for('routes.index'))

# ================================================================
#   Name:           Unapply Route
#   Description:    Backend route to unapply to position post
#   Last Changed:   11/16/21
#   Changed By:     Reagan Kelley
#   Change Details: Initial Implementation
# ================================================================
@bp_routes.route('/unapply/<postid>', methods = ['POST'])
@login_required
def unapply(postid):
    thepost = Post.query.filter_by(id = postid).first()
    if thepost is None:
        flash('Class with id "{}" not found.'.format(postid))
        return redirect(url_for('routes.index'))
    current_user.unapply(thepost)
    db.session.commit()
    flash('You redrew your application for: {}!'.format(thepost.title))
    return redirect(url_for('routes.index'))

# ================================================================
#   Name:           Submit Application Route
#   Description:    Form Page students are directed to when they 
#                   want to apply to a postion post.
#   Last Changed:   11/24/21
#   Changed By:     Reagan Kelley
#   Change Details: Revised to compensate for new database model
# ================================================================
@bp_routes.route('/submit_application/<postid>', methods = ['GET', 'POST'])
@login_required
def submit_application(postid):
    thepost = Post.query.filter_by(id = postid).first()
    aForm = ApplicationForm()

    if aForm.validate_on_submit():
        return redirect(url_for('routes.apply', postid = postid, brief = aForm.personal_statement.data, ref = aForm.faculty_ref_name.data))

    return render_template('submit.html', title="Apply for Position", post = thepost, form = aForm, profile = current_user)

# ================================================================
#   Name:           Applications Route
#   Description:    Prints all applications for faculty postion posts
#   Last Changed:   11/24/21
#   Changed By:     Reagan Kelley
#   Change Details: Revised to compensate for new database model
# ================================================================
@bp_routes.route('/applications', methods=['GET', 'POST'])
@login_required
def applications():
    myposts = current_user.get_user_posts()
    print(myposts.count())
    return render_template('applications.html', title="Applications", posts = myposts)

# ================================================================
#   Name:           Review Route
#   Description:    Displays application of desired student who 
#                   applied to the faculty's position post.
#   Last Changed:   11/16/21
#   Changed By:     Reagan Kelley
#   Change Details: Initial Implementation
# ================================================================
@bp_routes.route('/review/<postid>/<userid>', methods = ['GET', 'POST'])
@login_required
def review(postid, userid):
    application = Application.query.filter_by(applicant_id = userid, post_id = postid).first()
    return render_template('review.html', title="Review Application", application = application)

# ================================================================
#   Name:           Update Route
#   Description:    Backend route that changes 
#                   the status of an application
#   Last Changed:   11/16/21
#   Changed By:     Reagan Kelley
#   Change Details: Initial Implementation
# ================================================================
@bp_routes.route('/update/<postid>/<userid>/<change>', methods = ['GET', 'POST'])
@login_required
def update(postid, userid, change):
    
    application = Application.query.filter_by(applicant_id = userid, post_id = postid).first()

    if change == 'Interview':
        application.status = 'Interview'
    elif (change == 'Reject'):
        application.status = 'Reject'
    
    db.session.commit()

    return redirect(url_for('routes.applications'))