from datetime import datetime
from enum import unique
from app import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from app import login

postTags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))
def __repr__(self):
        return '<Post ID: {} , Tag Name: {}>'.format(self.post_id,self.tag_name)


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
        if self.user_type is 0:
            return True
        return False


class PositionPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(1500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    tags = db.relationship('Tag', backref = 'post_tags', secondary = postTags, primaryjoin = (postTags.c.post_id == id),  lazy = 'dynamic' )


    def get_tags(self):
        return self.tags

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
