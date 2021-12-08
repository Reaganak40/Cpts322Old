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
from project import create_user1, create_user2, init_majors_and_fields

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


    ##Tests whether has the student has actually applied to a post after sending the application
    def test_has_applied(self):
        f1 = create_user1('Faculty', 'andy', 'aofallon@wsy.edu', 'abc', '444444444')
        db.session.add(f1)
        p1 = Post(user_id =f1.id, title='My post', body='This is my test post.', time_commitment = '20', start_date = datetime.datetime(2023, 5, 11), end_date = datetime.datetime(2024, 1, 21))
        db.session.add(p1)
        db.session.commit()
        self.assertEqual(Post.query.all.first().id, p1.id)
        u2 = Student(username='Tay', wsu_id = '111127598', email ='jingren.tay@wsu.edu', user_type = 'Student')
        u2.set_password('abc')
        u2.apply(p1,'Hi','Bob')
        db.session.commit()
        self.assertEqual(u2.has_applied(p1), True)
        
        
    
    ##Tests both student and faculty are displaying the correct status before and after reviewing
    def test_get_status(self):
        # u1 = Faculty(username='test', wsu_id = '111111111', email='testy.tester@wsu.com', user_type = 'Faculty')
        # u1.set_password('123')
        # p1 = Post(user_id = u1.id, title='My post', body='This is my test post.', time_commitment = '20', start_date = datetime.datetime(2023, 5, 11), end_date = datetime.datetime(2024, 1, 21))
        # db.session.add(p1)
        # db.session.commit()
        # u2 = Student(username='Tay', wsu_id = '111127598', email ='jingren.tay@wsu.edu', user_type = 'Student')
        # u2.set_password('abc')
        # u2.apply(p1,'Hi','Bob')
        # db.session.commit()
        # self.assertEqual(u2.get_status(u2), 'Pending')
        pass
        
    
    ##Tests both student and faculty have correct user type registered into the database
    def test_get_user_type(self):
        u1 = Student(username='test', wsu_id = '111111111', email='testy.tester@wsu.com', user_type = 'Student')
        db.session.add(u1)
        db.session.commit()
        self.assertEqual(u1.get_user_type(), 'Student')

        u2 = Faculty(username='test2', wsu_id = '111111117', email='testy2.tester@wsu.com', user_type = 'Faculty')
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u2.get_user_type(), 'Faculty')

    ##test the function can_apply where student should not be able to apply if there is no wsu_id
    def test_can_apply_student(self):
        u1 = Student(username='test', wsu_id = '111111111', email='testy.tester@wsu.com', user_type = 'Student')
        db.session.add(u1)
        db.session.commit()
        self.assertEqual(u1.can_apply(), True)

        u2 = Student(username='tay', wsu_id = None, email='testy2.tester@wsu.com', user_type = 'Student')
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u2.can_apply(), False)


    def test_apply_student(self):
        pass

    def test_unapply_student(self):
        pass

    def test_can_apply_faculty(self):
        u1 = Faculty(username='test', wsu_id = '111111111', email='testy.tester@wsu.com', user_type = 'Faculty')
        db.session.add(u1)
        db.session.commit()
        self.assertEqual(u1.can_apply(), False)

    

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

        p2 = Post(user_id = u1.id, title='Second post', body='This is my 2nd test post.', time_commitment = '100', start_date = datetime.datetime(2024, 10, 12), end_date = datetime.datetime(2025, 1, 17))
        db.session.add(p2)
        db.session.commit()
        self.assertEqual(u1.posts.count(), 2)
        self.assertEqual(u1.posts[1].title, 'Second post')
        self.assertEqual(u1.posts[1].body, 'This is my 2nd test post.')
        self.assertEqual(u1.posts[1].time_commitment, '100')
        self.assertEqual(u1.posts[1].start_date, datetime.datetime(2024, 10, 12).date())
        self.assertEqual(u1.posts[1].end_date, datetime.datetime(2025, 1, 17).date())

    


if __name__ == '__main__':
    unittest.main(verbosity=2)