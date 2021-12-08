import os
import pytest
from app import create_app, db
from app.Model.models import User, Student, Faculty, Post, Major, Field
from config import Config


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = 'bad-bad-key'
    WTF_CSRF_ENABLED = False
    DEBUG = True
    TESTING = True

pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(config_class = TestConfig)

    db.init_app(flask_app)
    testing_client = flask_app.test_client()
 
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client 
    ctx.pop()

def new_user(user_name, wsuid, e_mail, usertype, passw): # Initializes a new user
    user = User(username = user_name, wsu_id = wsuid, email = e_mail, user_type = usertype)
    user.set_password(passw)
    return user

def init_majors_and_fields():
    if Major.query.count() == 0:
        major1 = Major(name = 'Computer Science', id = 1)
        major2 = Major(name = 'Computer Engineering', id = 2)
        major3 = Major(name = 'Electrical Engineering', id = 3)
        major4 = Major(name = 'Mechanical Engineering', id = 4)

        fieldNA = Field(field = 'Empty Field', id = -1)
        # Research Fields
        field1 = Field(field = 'Machine Learning', id = 1)
        field2 = Field(field = 'Networking', id = 2)
        field3 = Field(field = 'Data Science', id = 3)
        field4 = Field(field = 'Logic Circuits', id = 4)
        field5 = Field(field = 'Unix-Linux Systems', id = 5)
        field6 = Field(field = 'Quantum Computing', id = 6)
        field7 = Field(field = 'Circuit Design', id = 7)
        field8 = Field(field = 'Robotics', id = 8)
        field9 = Field(field = 'Electronics', id = 9)
        field10 = Field(field = 'Cyber Security', id = 10)
        field11 = Field(field = 'Mobile Devices', id = 11)

        # Build relationship between majors and fields
        # Computer Science
        major1.fields.append(field1)
        major1.fields.append(field2)
        major1.fields.append(field3)
        major1.fields.append(field5)
        major1.fields.append(field6)
        major1.fields.append(field10)

        # Computer Engineering
        major2.fields.append(field1)
        major2.fields.append(field2)
        major2.fields.append(field4)
        major2.fields.append(field6)
        major2.fields.append(field8)
        major2.fields.append(field11)

        # Electrical Engineering
        major3.fields.append(field4)
        major3.fields.append(field6)
        major3.fields.append(field7)
        major3.fields.append(field8)
        major3.fields.append(field9)
        major3.fields.append(field11)

        # Mechanical Engineering
        major4.fields.append(field4)
        major4.fields.append(field7)
        major4.fields.append(field8)
        major4.fields.append(field9)
        major4.fields.append(field11)

        db.session.add(major1) # Add Majors
        db.session.add(major2)
        db.session.add(major3)
        db.session.add(major4) 

        db.session.add(field1) # Add Fields
        db.session.add(field2)
        db.session.add(field3)
        db.session.add(field4)
        db.session.add(field5)
        db.session.add(field6)
        db.session.add(field7)
        db.session.add(field8)
        db.session.add(field9)
        db.session.add(field10)
        db.session.add(field11)

        db.session.add(fieldNA)
        
        db.session.commit()
        pass
    pass

@pytest.fixture
def init_database(): # Initializes the database
    db.create_all()
    init_majors_and_fields()
    user1 = new_user(user_name = 'sakire', wsuid = '111111111', e_mail = 'sakire@wsu.edu', usertype = 'Faculty', passw = 'abc')
    user2 = new_user(user_name = 'denise', wsuid = '222222222', e_mail = 'denise.tanumihardja@wsu.edu', usertype = 'Student', passw = '123')
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    yield 

    db.drop_all()

def test_register_page(test_client): # Tests the register page
    response = test_client.get('/register')
    assert response.status_code == 200
    assert b"Register" in response.data

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

    