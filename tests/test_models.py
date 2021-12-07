import warnings
warnings.filterwarnings("ignore")
import os
basedir = os.path.abspath(os.path.dirname(__file__))

from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.Model.models import User, Student, Faculty, Application, Post, Major, Field
from config import Config
import datetime

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
        u1.set_password('abc')
        u2.set_password('123')

        self.assertFalse(u1.check_password('123'))
        self.assertTrue(u1.check_password('abc'))

        self.assertFalse(u2.check_password('abc'))
        self.assertTrue(u2.check_password('123'))

    def test_post_1(self):
        u1 = Faculty(username='test', wsu_id = '111111111', email='testy.tester@wsu.com', user_type = 'faculty')
        db.session.add(u1)
        db.session.commit()
        self.assertEqual(u1.posts.all(), [])
        p1 = Post(user_id = u1.id, title='My post', body='This is my test post.', time_commitment = '20', start_date = datetime.datetime(2023, 5, 11), end_date = datetime.datetime(2024, 1, 21))
        db.session.add(p1)
        db.session.commit()
        self.assertEqual(u1.posts.count(), 1)
        self.assertEqual(u1.posts[0].title, 'My post')
        self.assertEqual(u1.posts[0].body, 'This is my test post.')
        self.assertEqual(u1.posts[0].time_commitment, '20')
        self.assertEqual(u1.posts[0].start_date, datetime.datetime(2023, 5, 11).date())
        self.assertEqual(u1.posts[0].end_date, datetime.datetime(2024, 1, 21).date())


if __name__ == '__main__':
    unittest.main(verbosity=2)