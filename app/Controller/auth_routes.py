from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for
from flask_sqlalchemy import sqlalchemy
from config import Config
from app.Model.models import User
from app import db
from flask_login import current_user, login_user, logout_user, login_required
from app.Controller.auth_forms import LoginForm, RegisterForm

## Reagan added bp_auth blueprint 10/26/21
bp_auth = Blueprint('auth', __name__)
bp_auth.template_folder = Config.TEMPLATE_FOLDER 

# ================================================================
#   Name:           Register Route
#   Description:    Handles Registers Forms, Creates an account for both student and faculty.
#   Last Changed:   10/27/21
#   Changed By:     Tay Jing Ren
#   Change Details: Change naming convention from form_auth to form 
# ================================================================

@bp_auth.route('/register', methods=['GET', 'POST'])
def register():
    auth = RegisterForm()
    if auth.validate_on_submit():
        new_user = User(username = auth.username.data, email = auth.email.data)
        new_user.set_password(auth.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('You are registered!')
        if new_user.user_type is 0:
            return redirect(url_for('routes.index')) #Change depending on if student account or faculty account
        return redirect(url_for('routes.index')) #If user type is faculty (1)     
    return render_template('register.html', form = auth)

# ================================================================
#   Name:           Login Route
#   Description:    Handles Login Forms, Allows user to login
#   Last Changed:   10/27/21
#   Changed By:     Tay Jing Ren
#   Change Details: Change naming convention from login_form to form 
# ================================================================
@bp_auth.route('/login', methods = ['GET', 'POST'])
def login(): 
    if current_user.is_authenticated:
        redirect(url_for('routes.index'))
    form_login = LoginForm()
    user = User()
    if form_login.validate_on_submit():
        user.query.filter_by(username = form_login.username.data).first()
        if (user is None) or (user.check_password(form_login.password.data) is False):
            flash('Invalid username or password.')
            return redirect(url_for('auth.login'))
        if user.user_type is 0:
            return redirect(url_for('routes.index')) #Change depending on if student account or faculty account
        login_user(user, remember = form_login.remember_me.data)
        return redirect(url_for('routes.index'))
    return render_template('login.html', title='Sign In', form = form_login)

# ================================================================
#   Name:           Logout Route
#   Description:    Logs out user
#   Last Changed:   10/26/21
#   Changed By:     Denise Tanumihardja
#   Change Details: Initial implementation of logout route. (taken from smile project)
# ================================================================

@bp_auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))