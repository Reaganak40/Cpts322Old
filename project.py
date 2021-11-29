from sqlalchemy.sql.sqltypes import DateTime
from app import create_app, db
from app.Model.models import Faculty, User, Student, Post, Major, Field, postMajors
import datetime
app = create_app()

# ================================================================
#   Name:           Init DB
#   Description:    If there is not db, call this function to initialize it
#   Last Changed:   10/26/21
#   Changed By:     Reagan Kelley
#   Change Details: Skeleton version for initDB (taken from smileApp)
#=================================================================
@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()
    if Major.query.count() == 0:
         majors = ['Computer Science','Computer Engineering', 'Electrical Engineering', 'Chemical Engineering'] ##NEED TO: change tag names
         for m in majors:
             db.session.add(Major(name=m))
         db.session.commit()

    if(app.debug):
        if(User.query.count() == 0): # Don't reinitialize if already initialzed (duh)
            print("Debug: Initializing with pre-existing data...")
            fill_db()

    # if Field.query.count() is None:
    #     field_name = [{'field_name':'Artificial Intelligence', 'major_name':'Computer Science'}]
    #     for f in field_name:
    #         db.session.add(Field(majors = f['majors'], field = f['field']))
    #     db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)

def fill_db():

    # User: Reagan
    # Type: student
    # Password: abc
    new_user = Student(username = 'reagan', email = 'reaganak@gmail.com', user_type = 'student')
    new_user.set_password('abc')
    db.session.add(new_user)
    print("Debug: Added New Student: [reagan]")

    # User: denise
    # Type: Student
    # Password: abc
    new_user = Student(username = 'denise', email = 'denisetanumihardja@gmail.com', user_type = 'student')
    new_user.set_password('abc')
    db.session.add(new_user)
    print("Debug: Added New Student: [denise]")

    # User: tay
    # Type: Student
    # Password: abc
    new_user = Student(username = 'tay', email = 'jrtay123456@gmail.com', user_type = 'student')
    new_user.set_password('abc')
    db.session.add(new_user)
    print("Debug: Added New Student: [tay]")

    # User: sakire
    # Type: Faculty
    # Password: abc
    new_user = Faculty(username = 'sakire', email = 'sakire@wsu.edu', user_type = 'faculty')
    new_user.set_password('abc')
    db.session.add(new_user)
    print("Debug: Added New Faculty: [sakire]")

    # User: Andy
    # Type: Faculty
    # Password: abc
    new_user = Faculty(username = 'andy', email = 'aofallon@wsu.edu', user_type = 'faculty')
    new_user.set_password('abc')
    db.session.add(new_user)
    print("Debug: Added New Faculty: [andy]")

    # Post: Database Integrity
    # Posted By: Sakire
    majors = Major.query.slice(0,2) # Gets first two majors in list (TODO: if you can find a better way of sorts majors please change)
    faculty_user = User.query.filter_by(username = 'sakire').first()
    newPost = Post(user_id = faculty_user.id, title= 'Database Integrity', 
            body = 'We are looking for 3-4 year undergrad students who enjoy working in the fields of networking and cybersecurity. We are teaming up with Amazon to make penetration software that will test the integrity of their AWS systems. You do not need to be an expert on databases nor security, but it would be very helpful.', 
            majors = majors)
    db.session.add(newPost)
    print("Debug: Added New Post: [Database Integrity]")

    # Post: Checkers AI
    # Posted By: Andy
    majors = Major.query.all()
    faculty_user = User.query.filter_by(username = 'andy').first()
    newPost = Post(user_id = faculty_user.id, title= 'Everyone Loves Checkers', 
            body = 'If you are interested in machine learning, do I have a lab position for you. We are teaming up with the International Association for Professional Checkers Players to create a machine learning AI that will test the skills of the best checker players across the world. Applicants who have taken intro to machine learning courses and further will have a competitive advantage in receiving a position for this lab.', 
            majors = majors)
    db.session.add(newPost)
    print("Debug: Added New Post: [Everyone Loves Checkers]")

    # Edit Profile Info: Reagan
    student_user = User.query.filter_by(username = 'reagan').first()
    student_user.wsu_id = 11663871
    student_user.first_name = 'Reagan'
    student_user.last_name = 'Kelley'
    student_user.phone_no = '2094804983'
    student_user.major = Major.query.filter_by(id = 0).first() # TODO: Does not work
    student_user.gpa = 3.96
    student_user.expected_grad_date = datetime.datetime(2023, 5, 20)
    student_user.elect_courses = 'cs360 - A\ncs355 - A\ncs122 - A'
    student_user.research_topics = 'To be Implemented'
    student_user.languages = 'C/C++, Python, Java, Haskell'
    student_user.prior_research = 'None'
    print("Debug: Updated Profile Info: [reagan]")

    # Commit changes to database
    db.session.commit()
    print("Debug: Committing Changes ...")

