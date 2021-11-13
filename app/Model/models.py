from datetime import datetime
from enum import unique
from app import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from app import login

# ================================================================
# Gets User.id for logged in user (updated 10/27/21): fixed int error
# ================================================================
@login.user_loader
def load_user(id):
    return User.query.get(id)

# ================================================================
# Relationship: Every post can have multiple Majors
# ================================================================
postMajors = db.Table('postMajors',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('major_id', db.Integer, db.ForeignKey('major.id')))
def __repr__(self):
        return '<Post ID: {} , Major Name: {}>'.format(self.post_id,self.major_name)

# ================================================================
#   Name:           User Model
#   Description:    Class Definition for User
#   Last Changed:   11/12/21
#   Changed By:     Reagan Kelley
#   Change Details: Revised Database Model
# ================================================================
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)
    email = db.Column(db.String(120), unique = True, index = True)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.Integer)

    def __repr__(self):
        return '<Username: {} - {};>'.format(self.id,self.username)

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)

    def get_user_type(self):
        if self.user_type == 0:
            return 'Student'
        return 'Faculty'

# ================================================================
#   Name:           Student Model
#   Description:    Class Definition for Student (Child of User)
#   Last Changed:   11/12/21
#   Changed By:     Reagan Kelley
#   Change Details: Initial Implementation of Student
# ================================================================
class Student(User):
    wsu_id = db.Column(db.Integer, unique = True)

    def __repr__(self):
        return '<Username: {} - {}; Type: {}; Class-Object Code: 0>'.format(self.id,self.username, self.get_user_type())

# ================================================================
#   Name:           Faculty Model
#   Description:    Class Definition for Faculty (Child of User)
#   Last Changed:   11/12/21
#   Changed By:     Reagan Kelley
#   Change Details: Initial Implementation of Faculty
# ================================================================
class Faculty(User):
    posts = db.relationship('Post', backref='writer', lazy = 'dynamic')

    def __repr__(self):
        return '<Username: {} - {}; Type: {}; Class-Object Code: 1>'.format(self.id,self.username, self.get_user_type())

    def get_user_posts(self):
        return self.posts

# ================================================================
#   Name:           Post Model
#   Description:    Class Definition for Posts
#   Last Changed:   10/26/21
#   Changed By:     Reagan Kelley
#   Change Details: Changed class name from PositionPost to Post
#                   Reason: Avoid relationship errors
# ================================================================
class Post(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(150))
    body = db.Column(db.String(1500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    majors = db.relationship('Major', 
        backref = db.backref('postMajors', lazy='dynamic'), 
        secondary = postMajors, 
        primaryjoin = (postMajors.c.post_id == id),  
        lazy = 'dynamic' 
    )


    def get_majors(self):
        return self.majors
# ================================================================
#   Name:           Major Model
#   Description:    Class Definition for Major (Tag)
#   Last Changed:   11/12/21
#   Changed By:     Reagan Kelley
#   Change Details: Added get name function
# ================================================================
class Major(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))

    def get_major_name(self):
        return self.name

#
#class ResearchField(Major):
#    id = db.Column(db.Integer, primary_key = True)
#    research_field_name = db.Column(db.String(20))
#
#    def get_research_field(self):
#        return self.research_field_name






