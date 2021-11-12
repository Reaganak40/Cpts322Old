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
# Relationship: Every post can have multiple tags
# ================================================================
postTags = db.Table('postTags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))
def __repr__(self):
        return '<Post ID: {} , Tag Name: {}>'.format(self.post_id,self.tag_name)

# ================================================================
#   Name:           User Model
#   Description:    Class Definition for User
#   Last Changed:   11/11/21
#   Changed By:     Reagan Kelley
#   Change Details: Fixed is_student error 
#                   (was returning false for students)
# ================================================================
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)
    email = db.Column(db.String(120), unique = True, index = True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='writer', lazy = 'dynamic')
    user_type = db.Column(db.Integer, default = 0)  # default = 0 means Student
    

    def __repr__(self):
        return '<Username: {} - {};>'.format(self.id,self.username)

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)

    def get_user_posts(self):
        return self.posts
    
    def is_student(self):
        if self.user_type == 0:
            return True
        return False

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
    tags = db.relationship('Tag', 
        backref = db.backref('postTags', lazy='dynamic'), 
        secondary = postTags, 
        primaryjoin = (postTags.c.post_id == id),  
        lazy = 'dynamic' 
    )


    def get_tags(self):
        return self.tags
# ================================================================
#   Name:           Tag Model
#   Description:    Class Definition for Tags
#   Last Changed:   11/12/21
#   Changed By:     Reagan Kelley
#   Change Details: Added get name function
# ================================================================
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))

    def get_name(self):
        return self.name
