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
# Relationship: Every subfield can have multiple majors
# ================================================================
subField = db.Table('subField', 
    db.Column('major_id', db.Integer, db.ForeignKey('major.id')),
    db.Column('field_id', db.Integer, db.ForeignKey('field.id')))
def __repr__ (self):
    return '<Major Name: {}, Field Name: {}>'.format(self.major_name, self.field_name)
# ================================================================
#   Name:           User Model
#   Description:    Class Definition for User
#   Last Changed:   11/16/21
#   Changed By:     Reagan Kelley
#   Change Details: Revised User database model
# ================================================================
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)
    email = db.Column(db.String(120), unique = True, index = True)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(20))

    permissions = db.relationship('Permissions', backref='writer', lazy = 'dynamic')
    posts = db.relationship('Post', backref='writer', lazy = 'dynamic')

    def __repr__(self):
        return '<Username: {} - {};>'.format(self.id,self.username)

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)

    def get_user_type(self):
        return self.user_type

    def get_user_posts(self):
        return self.posts
# ================================================================
#   Name:           Permissions Model
#   Description:    Class Definition for Permissions
#   Last Changed:   11/16/21
#   Changed By:     Reagan Kelley
#   Change Details: Initial Implementation
# ================================================================
class Permissions(db.Model):

    permission_identifier = db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Student Permissions
    wsu_id = db.Column(db.Integer, unique = True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(100))
    phone_no = db.Column(db.String(10))
    #major = db.Column(db.ForeignKey('major.id'))
    #print(major)
    majorofstudent = db.relationship('StudentMajor', back_populates = '_permissions') ## TODO: Need to impelement majors
    gpa = db.Column(db.Float(precision = 1))
    expected_grad_date = db.Column(db.Date)
    elect_courses = db.Column(db.String(1500))
    research_topics = db.Column(db.String(20)) ## TODO: Need to implement research topics
    languages = db.Column(db.String(700))
    prior_research = db.Column(db.String(1500))

    def init_permissions(self):
        if self.permission_identifier == 'Student':
            self.first_name = 'No'
            self.last_name = 'Name'

    def get_permission_identifier(self):
        return self.permission_identifier

    def get_user_posts(self):
        return self.posts

    def __repr__(self):
        owner = User.query.filter_by(id = self.user_id).first()
        return "<Permissions Object for: {}>".format(owner.id)

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
    name = db.Column(db.String(20), primary_key = True)
    studentsinmajor = db.relationship('StudentMajor', back_populates = '_major')
    print(name)
    def get_major_name(self):
        return self.name

class StudentMajor(db.Model):
      studentmajor = db.Column(db.String(20), db.ForeignKey('major.name'), primary_key = True)
      studentid = db.Column(db.Integer, db.ForeignKey('permissions.id'), primary_key = True)
      startdate = db.Column(db.DateTime)
      primary = db.Column(db.Boolean)
      _permissions = db.relationship('Permissions')
      _major = db.relationship('Major')
      def __repr__(self):
          return '<StudentMajor ({}, {}, {}, {}) >'.format(self.studentmajor, self.studentid, self.startdate, self.primary)




# ================================================================
#   Name:           Research Field Model
#   Description:    Class Definition for Research Field (Tag)
#   Last Changed:   11/16/21
#   Changed By:     Tay Jing Ren
#   Change Details: Skeleton Code
# ================================================================


class Field(Major):
    id = db.Column(db.Integer, primary_key = True)
    #field = db.Column(db.String(50), primary_key = True)
    #major_name= db.Column(db.String(30))
    #major_id = db.Column(db.Integer, db.ForeignKey('major.id'))
    majors = db.relationship('Major', backref = db.backref('subField', lazy = 'dynamic'), secondary = subField)
    def get_research_field(self):
        return self.field_name






