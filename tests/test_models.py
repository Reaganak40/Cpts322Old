import warnings
warnings.filterwarnings("ignore")
import os
basedir = os.path.abspath(os.path.dirname(__file__))

from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.Model.models import User, Student, Faculty, Application, Post, Major, Field
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ROOT_PATH = '..//'+basedir

class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    #Tests password hashing for both student and faculty users.
    def test_password_hashing(self): 
        u1 = User(username = 'test', wsu_id = '111111111', email='testy.tester@wsu.edu', user_type = 'Student')
        u2 = User(username = 'test2', wsu_id = '222222222', email='testy2.tester@wsu.edu', user_type = 'Faculty')
        u1.set_password('test123')
        u2.set_pasword('testabc')

        self.assertFalse(u1.set_password('testabc'))
        self.assertTrue(u1.set_password('test123'))

        self.assertFalse(u2.set_password('test123'))
        self.assertTrue(u2.set_password('testabc'))

    def test_post_1(self):
        u1 = User(username='test', wsu_id = '111111111', email='testy.tester@wsu.com', user_type = 'Faculty')
        db.session.add(u1)
        db.session.commit()
        self.assertEqual(u1.get_user_posts().all(), [])
        p1 = Post(user_id = u1.id, title='My post', body='This is my test post.', time_commitment = '20', start_date = '12/05/2021', end_date = '12/06/2021')
        db.session.add(p1)
        db.session.commit()
        self.assertEqual(u1.get_user_posts().count(), 1)
        self.assertEqual(u1.get_user_posts().first().title, 'My post')
        self.assertEqual(u1.get_user_posts().first().body, 'This is my test post.')
        self.assertEqual(u1.get_user_posts().first().time_commitment, '20')
        self.assertEqual(u1.get_user_posts().first().start_date, '12/05/2021')
        self.assertEqual(u1.get_user_posts().first().end_date, '12/06/2021')


if __name__ == '__main__':
    unittest.main(verbosity=2)