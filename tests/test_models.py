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


# TEST: APPLICATION

    def test_application_1(self):
        init_majors_and_fields()
        # faculty user
        f1 =  create_user1('Faculty', 'sakire', 'sakire@wsy.edu', 'abc', '55555555')
        db.session.add(f1)

        # student user
        s1 = create_user2('Student', 'reagan', 'reagan.kelley@wsu.edu', 'abc', '11663871', 'Reagan', 'Kelley', '2094804983', 
                            'Computer Science', ['Machine Learning', 'Robotics', 'Circuit Design', 'Unix-Linux Systems'], 
                            2.67, datetime.datetime(2023, 5, 20), 'cs360 - A, cs322 - A, cs223 - A', 'C/C++, Javascript, Haskell, Java', 'None')
        db.session.add(s1)
        db.session.commit()

        self.assertEqual(2, User.query.count()) # verify users are made
        
        p1 = Post(user_id = f1.id, title='Test Position 1', body='This is my test post.', time_commitment = '20', start_date = datetime.datetime(2023, 5, 11), end_date = datetime.datetime(2024, 1, 21))
        db.session.add(p1)
        db.session.commit()

        a2 = Application(applicant_id = s1.id, post_id = p1.id, student_applied = s1, position_for = p1, faculty_ref = "KC WANG (000)-000-000")
        db.session.add(a2)
        db.session.commit()

        self.assertEqual(1, Application.query.count())           #    testing: if expected application count is correct
        self.assertEqual(s1.id, a2.get_applicant().id)           #    testing: if application belongs to student
        self.assertEqual('Test Position 1', a2.get_position())   #    testing: if application relationship with post is correct

    def test_application_2(self):
        init_majors_and_fields()
        # faculty user 1
        f1 =  create_user1('Faculty', 'sakire', 'sakire@wsu.edu', 'abc', '55555555')
        db.session.add(f1)

        # faculty user 2
        f2 = create_user1('Faculty', 'andy', 'aofallon@wsu.edu', 'abc', '444444444')
        db.session.add(f2)

        # faculty user 3
        f3 = create_user1('Faculty', 'ted', 'ted@wsu.edu', 'abc', '333333333')
        db.session.add(f3)

        # student user 1
        s1 = create_user2('Student', 'reagan', 'reagan.kelley@wsu.edu', 'abc', '11663871', 'Reagan', 'Kelley', '2094804983', 
                            'Computer Science', ['Machine Learning', 'Robotics', 'Circuit Design', 'Unix-Linux Systems'], 
                            2.67, datetime.datetime(2023, 5, 20), 'cs360 - A, cs322 - A, cs223 - A', 'C/C++, Javascript, Haskell, Java', 'None')
        db.session.add(s1)

        # student user 2
        s2 = create_user2('Student', 'bobby', 'bobby@wsu.edu', 'abc', '232323231', 'Bob', 'Marley', '1123456785', 
                           'Electrical Engineering', ['Machine Learning', 'Robotics', 'Circuit Design'], 
                            3.67, datetime.datetime(2026, 5, 20), 'Bio102 - C, cs322 - A, cs223 - D', 'C/C++, Javascript, HTML', 'None')
        db.session.add(s2)

        # student user 3
        s3 = create_user2('Student', 'tay', 'tay@wsu.edu', 'abc', '783625424', 'jing ren', 'tay', '5672341234', 
                            'Computer Engineering', ['Machine Learning', 'Robotics', 'Circuit Design'], 
                            2.67, datetime.datetime(2022, 5, 20), 'cs360 - C, cs322 - A, cs355 - F', 'C/C++, Haskell, HTML', 'None')
        db.session.add(s3)

        db.session.commit()          

        self.assertEqual(6, User.query.count()) # verify users are made

        p1 = Post(user_id = f1.id, title='Test Position 1', body='This is my test post.', time_commitment = '20', start_date = datetime.datetime(2023, 5, 11), end_date = datetime.datetime(2024, 1, 21))
        db.session.add(p1)
        db.session.commit()

        a1 = Application(applicant_id = s3.id, post_id = p1.id, student_applied = s3, position_for = p1, faculty_ref = "BOB (111)-111-111")
        db.session.add(a1)
        db.session.commit()

        a2 = Application(applicant_id = s1.id, post_id = p1.id, student_applied = s1, position_for = p1, faculty_ref = "KC WANG (000)-000-000")
        db.session.add(a2)
        db.session.commit()

        self.assertEqual(2, Application.query.count())           #    testing: works correctly with multiple applications
        self.assertEqual(s3.id, a1.get_applicant().id)           #    testing: if application belongs to student 3
        self.assertEqual(s1.id, a2.get_applicant().id)           #    testing: if application belongs to student 1
        self.assertEqual([], s2.applications)                    #    testing: that student 2 never applied


    def test_application_3(self):
        init_majors_and_fields()
        # faculty user
        f1 =  create_user1('Faculty', 'sakire', 'sakire@wsy.edu', 'abc', '55555555')
        db.session.add(f1)

        # student user
        s1 = create_user2('Student', 'reagan', 'reagan.kelley@wsu.edu', 'abc', '11663871', 'Reagan', 'Kelley', '2094804983', 
                            'Computer Science', ['Machine Learning', 'Robotics', 'Circuit Design', 'Unix-Linux Systems'], 
                            2.67, datetime.datetime(2023, 5, 20), 'cs360 - A, cs322 - A, cs223 - A', 'C/C++, Javascript, Haskell, Java', 'None')
        db.session.add(s1)
        db.session.commit()

        self.assertEqual(2, User.query.count()) # verify users are made
    
        p1 = Post(user_id = f1.id, title='Test Position 1', body='This is my test post.', time_commitment = '20', start_date = datetime.datetime(2023, 5, 11), end_date = datetime.datetime(2024, 1, 21))
        db.session.add(p1)
        db.session.commit()

        a2 = Application(applicant_id = s1.id, post_id = p1.id, student_applied = s1, position_for = p1, faculty_ref = "KC WANG (000)-000-000")
        db.session.add(a2)
        db.session.commit()

        self.assertEqual(1, Application.query.count())           #    testing: if expected application count is correct
        self.assertEqual(s1.id, a2.get_applicant().id)           #    testing: if application belongs to student
        self.assertEqual('Test Position 1', a2.get_position())   #    testing: if application relationship with post is correct

        applications = p1.get_applicants()

        for application in applications: # Remove connection in applications
            application.phantom_name = p1.title
            application.make_phantom()  # Retain post information
        
        db.session.delete(p1)
        db.session.commit()

        self.assertEqual(0, Post.query.count())                          #    testing: verify post has been deleted
        self.assertEqual(1, Application.query.count())                   #    testing: verify application was never deleted
        self.assertEqual([p1.title, 'No Longer Available'], a2.get_phantom())     #    testing: application is now in phantom mode







if __name__ == '__main__':
    unittest.main(verbosity=2)