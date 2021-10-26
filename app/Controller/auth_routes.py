from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for
from flask_sqlalchemy import sqlalchemy
from config import Config
from app.Model.models import User
from app import db
from flask_login import current_user, login_user, logout_user, login_required

## Reagan added bp_auth blueprint 10/26/21
bp_auth = Blueprint('auth', __name__)
bp_auth.template_folder = Config.TEMPLATE_FOLDER 

# ================================================================
#   Name:           Login Route
#   Description:    Handles Login Forms, Allows use to login
#   Last Changed:   10/26/21
#   Changed By:     Reagan Kelley
#   Change Details: Skeleton version of login
# ================================================================
@bp_auth.route('/login', methods = ['GET', 'POST'])
def login(): 
    ##Login Form still needed
    return render_template('login.html', title='Sign In')