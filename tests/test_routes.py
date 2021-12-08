import os
import pytest
from app import create_app, db
from app.Model.models import User, Post
from config import Config


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = 'bad-bad-key'
    WTF_CSRF_ENABLED = False
    DEBUG = True
    TESTING = True

pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(config_class=TestConfig)

    db.init_app(flask_app)
    testing_client = flask_app.test_client()
 
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client 
    ctx.pop()

def new_user(user_name, wsuid, e_mail, usertype, passw):
    user = User(username = user_name, wsu_id = wsuid, email = e_mail, user_type = usertype)
    user.set_password(passw)
    return user

def init_majors():
    pass

def init_fields():
    pass

@pytest.fixture
def init_database():
    db.create_all()
    init_majors()
    init_fields()
    user1 = new_user(user_name = 'sakire', wsuid = '111111111', e_mail = 'sakire@wsu.edu', usertype = 'Faculty', passw = 'abc')
    user2 = new_user(user_name = 'denise', wsuid = '222222222', e_mail = 'denise.tanumihardja@wsu.edu', usertype = 'Student', passw = '123')
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    yield 

    db.drop_all()

def test_register_page(test_client):
    response = test_client.get('/register')
    assert response.status_code == 200
    assert b"Register" in response.data

def test_register(test_client, init_database):
    response = test_client.post('/register', data = dict(username = 'reagan', wsu_id = '333333333', email = 'reagan.kelley@wsu.edu', user_type = 'Student', password = "abc", password2 = "abc"), follow_redirects = True)
    assert response.status_code == 200

    reg = db.session.query(User).filter(User.username == 'reagan')
    assert reg.count() == 1
    assert reg.first().wsu_id == '333333333'
    assert reg.first().email == 'reagan.kelley@wsu.edu'
    assert reg.first().user_type == 'Student'
    assert b"Sign In" in response.data   
    assert b"Please log in to access this page." in response.data

def test_register2(test_client, init_database):

    ## Testing for all individual empty fields (username, id, email, password, and repeat password)
    
    response1 = test_client.post('/register', data = dict(username = '', wsu_id = '333333333', email = 'reagan.kelley@wsu.edu', user_type = 'Student', password = "abc", password2 = "abc"), follow_redirects = True)
    assert response1.status_code == 200
    assert b"Please fill out this field" in response1.data

    response2 = test_client.post('/register', data = dict(username = 'reagan', wsu_id = '', email = 'reagan.kelley@wsu.edu', user_type = 'Student', password = "abc", password2 = "abc"), follow_redirects = True)
    assert response2.status_code == 200
    assert b"Please fill out this field" in response2.data

    response3 = test_client.post('/register', data = dict(username = 'reagan', wsu_id = '333333333', email = '', user_type = 'Student', password = "abc", password2 = "abc"), follow_redirects = True)
    assert response3.status_code == 200
    assert b"Please fill out this field" in response3.data

    response4 = test_client.post('/register', data = dict(username = 'reagan', wsu_id = '333333333', email = 'reagan.kelley@wsu.edu', user_type = 'Student', password = "", password2 = "abc"), follow_redirects = True)
    assert response4.status_code == 200
    assert b"Please fill out this field" in response4.data

    response5 = test_client.post('/register', data = dict(username = 'reagan', wsu_id = '333333333', email = 'reagan.kelley@wsu.edu', user_type = 'Student', password = "abc", password2 = ""), follow_redirects = True)
    assert response5.status_code == 200
    assert b"Please fill out this field" in response5.data

def test_invalidlogin(test_client,init_database):
    response1 = test_client.post('/login', data = dict(username='denise', password = '321'), follow_redirects = True)
    assert response1.status_code == 200
    assert b"Invalid username or password" in response1.data

    response2 = test_client.post('/login', data = dict(username = 'sakire', password = 'cba'), follow_redirects = True)
    assert response2.status_code == 200
    assert b"Invalid username or password" in response2.data

def test_login_logout(request,test_client,init_database):
    response1 = test_client.post('/login', data = dict(username = 'sakire', password = 'abc'), follow_redirects = True)
    assert response1.status_code == 200
    assert b"Welcome to Smile Portal!" in response1.data
    #TODO: Tbh I have no idea what the response should even be.

    response1 = test_client.get('/logout', follow_redirects = True)
    assert response1.status_code == 200
    assert b"Sign In" in response1.data
    assert b"Please log in to access this page." in response1.data

    response2 = test_client.post('/login', data = dict(username = 'denise', password = '123'), follow_redirects = True)
    assert response2.status_code == 200
    assert b"Welcome to Smile Portal!" in response2.data
    #TODO: Tbh I have no idea what the response should even be.

    response2 = test_client.get('/logout', follow_redirects = True)
    assert response2.status_code == 200
    assert b"Sign In" in response2.data
    assert b"Please log in to access this page." in response2.data

def test_post(test_client, init_database):
    response = test_client.post('/login', data = dict(username = 'sakire', password = 'abc', remember_me = False), follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome to Smile Portal!" in response.data
    #TODO: Tbh I have no idea what the response should even be.

    response = test_client.get('/postposition')
    assert response.status_code == 200
    assert b"Post New Smile" in response.data
    #TODO: Tbh I have no idea what the response should even be.

    