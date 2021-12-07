import os
from textwrap import fill
import pytest
from app import create_app, db
from app.Model.models import User, Student, Faculty, Post, Major, Field
from flask_login import current_user
from config import Config
from project import create_user1, create_user2, init_majors_and_fields, fill_db
import datetime

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = 'bad-bad-key'
    WTF_CSRF_ENABLED = False
    DEBUG = True
    TESTING = True

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(config_class = TestConfig)

    db.init_app(flask_app)
    testing_client = flask_app.test_client()
 
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client 
    ctx.pop()

@pytest.fixture
def init_database():

    db.create_all()

    # these two functions are project debug functions that do what we want: fill db with users and posts
    init_majors_and_fields()
    fill_db()
    db.session.commit()

    yield 

    db.drop_all()

def test_register_page(test_client): # Tests the register page
    response = test_client.get('/register')
    assert response.status_code == 200
    assert b"Register" in response.data

def test_postposition_page(test_client, init_database):

    #login
    response = test_client.post('/login', 
                        data=dict(username='sakire', password='abc',remember_me=False),
                        follow_redirects = True)
    assert response.status_code == 200

    response = test_client.get('/postposition')
    assert response.status_code == 200
    assert b"New Post" in response.data


def test_postposition_form(test_client, init_database):

    #login
    response = test_client.post('/login', 
                        data=dict(username='sakire', password='abc',remember_me=False),
                        follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome to Lab Opportunities!" in response.data


    #make a post
    major_ids = [1,3,4]
    majors = db.session.query(Major).filter(Major.id.in_(n for n in major_ids)).all()

    field_id_list = []
    fields = Field.query.all()

    for field in fields: # look at every field
        majors_for_field = field.majors # get the majors for that field
        for major in majors_for_field:
            if major.id in major_ids:   # if a selected major is assigned to this field add it to the list
                field_id_list.append(field.id)
                break
    fields = db.session.query(Field).filter(Field.id.in_(n for n in field_id_list)).all()

    response = test_client.post('/postposition', 
                        data=dict(title='New Position Post', body='This is a description of the position',majors= majors, fields = fields,
                        time_commitment = "30 to 40", start_date = "1/10/2022",
                        end_date = "5/21/2022", follow_redirects = True))
    assert response.status_code == 200
    ##assert b"Welcome to Lab Opportunities!" in response.data






# def test_register(test_client, init_database): # Tests the register function
#     response = test_client.post('/register', data = dict(username = 'reagan', wsu_id = '333333333', email = 'reagan.kelley@wsu.edu', user_type = 'Student', password = "abc", password2 = "abc"), follow_redirects = True)
#     assert response.status_code == 200

#     reg = db.session.query(User).filter(User.username == 'reagan')
#     assert reg.count() == 1
#     assert reg.first().wsu_id == '333333333'
#     assert reg.first().email == 'reagan.kelley@wsu.edu'
#     assert reg.first().user_type == 'Student'
#     assert b"Sign In" in response.data   
#     assert b"Please log in to access this page." in response.data

# def test_login_page(test_client): # Tests the login page
#     response = test_client.get('/login')
#     assert response.status_code == 200
#     assert b"Login" in response.data

# def test_logout_page(test_client): # Tests the logout page
#     response = test_client.get('/logout')
#     assert response.status_code == 200
#     assert b"Logout" in response.data

# def test_invalidlogin(test_client,init_database): # Tests for invalid login
#     response1 = test_client.post('/login', data = dict(username='denise', password = '321'), follow_redirects = True)
#     assert response1.status_code == 200
#     assert b"Invalid username or password" in response1.data

#     response2 = test_client.post('/login', data = dict(username = 'sakire', password = 'cba'), follow_redirects = True)
#     assert response2.status_code == 200
#     assert b"Invalid username or password" in response2.data

# def test_login_logout(request,test_client,init_database): # Tests for logging in and logging out
#     response1 = test_client.post('/login', data = dict(username = 'sakire', password = 'abc'), follow_redirects = True)
#     assert response1.status_code == 200
#     assert b"Welcome to Lab Opportunities!" in response1.data

#     response1 = test_client.get('/logout', follow_redirects = True)
#     assert response1.status_code == 200
#     assert b"Sign In" in response1.data
#     assert b"Please log in to access this page." in response1.data

#     response2 = test_client.post('/login', data = dict(username = 'denise', password = '123'), follow_redirects = True)
#     assert response2.status_code == 200
#     assert b"Welcome to Lab Opportunities!" in response2.data

#     response2 = test_client.get('/logout', follow_redirects = True)
#     assert response2.status_code == 200
#     assert b"Sign In" in response2.data
#     assert b"Please log in to access this page." in response2.data

# def test_index_page(test_client): # Tests the index page
#     response1 = test_client.get('/')
#     response2 = test_client.get('/index')
#     assert response1.status_code == 200
#     assert response2.status_code == 200
#     assert b"Welcome to Lab Opportunities!" in response1.data
#     assert b"Welcome to Lab Opportunities!" in response2.data

# def test_index_posts(test_client): # Tests if index shows posts
#     pass

# def test_index_sort(test_client): # Tests if the index autosorts posts as recommended
#     pass
    

# def test_profile_page(test_client): # Tests the student profile page
#     response = test_client.get('/student_profile')
#     assert response.status_code == 200

# def test_profile_access(test_client): # Tests if only student users can access profile page.
#     response1 = test_client.post('/login', data = dict(username='denise', password = '321'), follow_redirects = True)
#     assert response1.status_code == 200
#     response1 = test_client.get('/logout', follow_redirects = True)

#     response2 = test_client.post('/login', data = dict(username='denise', password = '321'), follow_redirects = True)
#     assert response1.status_code == 200
#     assert b"You do not have permission to access this page" in response2.data
#     response2 = test_client.get('/logout', follow_redirects = True)

# def test_update_profile_page(test_client): # Tests the student profile update page
#     response = test_client.get('/student_profile_update')
#     assert response.status_code == 200

# def test_update_profile(test_client): # Tests the updating of the student's profile
#     pass

# def test_post(test_client, init_database):
#     response = test_client.post('/login', data = dict(username = 'sakire', password = 'abc', remember_me = False), follow_redirects = True) # Tests 
#     assert response.status_code == 200
#     assert b"Welcome to Lab Opportunities!" in response.data

#     response = test_client.get('/postposition')
#     assert response.status_code == 200
#     assert b"Post New Smile" in response.data

    