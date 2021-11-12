from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config

from app import db
from app.Model.models import Post, Tag, postTags
from app.Controller.forms import PostForm
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
    return render_template('index.html', title="Lab Opportunities", posts=posts.all(), post_count = posts.count())

# ================================================================
#   Name:           Post Position Route
#   Description:    Post Position route for basic flask implementation
#   Last Changed:   11/11/21
#   Changed By:     Reagan Kelley
#   Change Details: Initial Implementation
# ================================================================
@bp_routes.route('/postposition', methods=['GET', 'POST'])
@login_required
def postposition():
    pForm = PostForm()
    if pForm.validate_on_submit():
        newPost = Post(user_id = current_user.id, title=pForm.title.data, body = pForm.body.data, tags = pForm.tags.data)
        db.session.add(newPost)
        db.session.commit()
        flash('New Position Post "' + newPost.title + '" is on the Job Board!')
        return redirect(url_for('routes.index'))
    if current_user.is_student():
        flash('You do not have permission to access this page.')
        return redirect(url_for('routes.index'))
    return render_template('create.html', title="New Post", form = pForm)