from app import create_app, db
from app.Model.models import Faculty, User, Student, Post, Major, Field, postMajors, majorFields
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

    # Creates Majors and Research Fields
    if Major.query.count() == 0:
        # Majors
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

        print("Majors")
        for major in Major.query.all():
            print('\t', major)

        print('\nResearch Fields:')
        for field in Field.query.all():
            print('\t', field)
            
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

# ================================================================
#   Name:           Fill Database
#   Description:    If in debug fills database with data
#   Last Changed:   12/1/21
#   Changed By:     Reagan Kelley
#   Change Details: Added time commitment and research fields to 
#                   posts
# ================================================================
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
    new_user = Student(username = 'denise', email = 'denisetanumihardja@wsu.edu', user_type = 'student')
    new_user.set_password('abc')
    db.session.add(new_user)
    print("Debug: Added New Student: [denise]")

    # User: tay
    # Type: Student
    # Password: abc
    new_user = Student(username = 'tay', email = 'jrtay123456@wsu.edu', user_type = 'student')
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
    _majors = Major.query.slice(0,2) # Gets first two majors in list (TODO: if you can find a better way of sorts majors please change)
    fields = _majors.first().fields
    faculty_user = User.query.filter_by(username = 'sakire').first()
    newPost = Post(user_id = faculty_user.id, title= 'Database Integrity', 
            body = 'We are looking for 3-4 year undergrad students who enjoy working in the fields of networking and cybersecurity. We are teaming up with Amazon to make penetration software that will test the integrity of their AWS systems. You do not need to be an expert on databases nor security, but it would be very helpful.', 
            majors = _majors,
            fields = fields,
            time_commitment = '25',
            start_date = datetime.datetime(2022, 1, 10),
            end_date = datetime.datetime(2022, 5, 21)
            )
    db.session.add(newPost)
    print("Debug: Added New Post: [Database Integrity]")

    # Post: Checkers AI
    # Posted By: Andy
    _majors = Major.query.all()
    fields = _majors[3].fields
    faculty_user = User.query.filter_by(username = 'andy').first()
    newPost = Post(user_id = faculty_user.id, title= 'Everyone Loves Checkers', 
            body = 'If you are interested in machine learning, do I have a lab position for you. We are teaming up with the International Association for Professional Checkers Players to create a machine learning AI that will test the skills of the best checker players across the world. Applicants who have taken intro to machine learning courses and further will have a competitive advantage in receiving a position for this lab.', 
            majors = _majors,
            fields = fields,
            time_commitment = '10-20',
            start_date = datetime.datetime(2022, 6, 2),
            end_date = datetime.datetime(2022, 8, 28)
            )
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

