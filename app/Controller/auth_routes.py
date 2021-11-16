from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for
from flask_sqlalchemy import sqlalchemy
from app.Controller.routes import index
from config import Config
from app.Model.models import Permissions, User
from app import db
from flask_login import current_user, login_user, logout_user, login_required
from app.Controller.auth_forms import LoginForm, RegisterForm

## Reagan added bp_auth blueprint 10/26/21
bp_auth = Blueprint('auth', __name__)
bp_auth.template_folder = Config.TEMPLATE_FOLDER 

# ================================================================
#   Name:           Register Route
#   Description:    Handles Registers Forms, Creates an account for both student and faculty.
#   Last Changed:   11/15/21
#   Changed By:     Reagan Kelley
#   Change Details: FIxed register to compensate for 
#                   new database model
# ================================================================

@bp_auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: #logged in users can't re-register
        flash('You are already registered!')
        return redirect(url_for('routes.index')) #If user type is faculty (1)     
    rForm = RegisterForm()
    if rForm.validate_on_submit():

        if(rForm.type.data == '0'): # New user is a student
            new_user = User(username = rForm.username.data, email = rForm.email.data, user_type = 'Student')
        else: # New User is a faculty
            new_user = User(username = rForm.username.data, email = rForm.email.data, user_type = 'Faculty')

        new_permissions = Permissions(user_id = new_user.id)

        new_user.set_password(rForm.password.data)
        db.session.add(new_user)
        db.session.add(new_permissions)
        db.session.commit()
        flash('You are registered!')
        return redirect(url_for('routes.index')) #redirect new registed user
    return render_template('register.html', form = rForm)

# ================================================================
#   Name:           Login Route
#   Description:    Handles Login Forms, Allows user to login
#   Last Changed:   11/15/21
#   Changed By:     Reagan Kelley
#   Change Details: Login heavily revised to work with new 
#                   database model
# ================================================================
@bp_auth.route('/login', methods = ['GET', 'POST'])
def login(): 
    if current_user.is_authenticated: ##current user is logged in -> redirect to index
        redirect(url_for('routes.index'))

    form_login = LoginForm()
    if form_login.validate_on_submit():

        ##initially check if user exists
        user = User.query.filter_by(username = form_login.username.data).first()

        if (user is None) or user.check_password(form_login.password.data) is False:
                flash('Invalid username or password.')
                return redirect(url_for('auth.login'))

        login_user(user, remember = form_login.remember_me.data)
            
        print(current_user)
        current_user.init()


        if current_user.get_user_type() == 'Student': ## user is a student
            return redirect(url_for('routes.index')) #Change depending on if student account or faculty account
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