from typing import Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.core import BooleanField, DateField, FloatField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import  DataRequired, Email, Length, NumberRange, Length, ValidationError
from wtforms.widgets.core import Select
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms_sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField
from app.Model.models import Post, Major, User, Field
from flask_login import current_user
from datetime import datetime

def get_majorlabel(theMajor):
    return theMajor.name

def all_majors():
    return Major.query.all()

def all_fields():
   return Field.query.all()

# ================================================================
#   Name:           Post form
#   Description:    Added sortform for filter posts on faculty view
#   Last Changed:   12/1/21
#   Changed By:     Reagan Kelley
#   Change Details: Added time commitment, start & end date
# ================================================================
class PostForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired()])
    body = TextAreaField("Job Description", [Length(min=0, max = 1500), DataRequired()])
    majors = QuerySelectMultipleField('Recommended Majors', query_factory= all_majors, get_label= lambda t: t.get_major_name(), widget=ListWidget(prefix_label=False), option_widget=CheckboxInput() )
    time_commitment = StringField('Time Commitment (Hours Per Week)', [Length(min = 1, max = 10), DataRequired()])
    start_date = DateField('Start Date', [DataRequired()], format = '%m/%d/%Y')
    end_date = DateField('End Date', [DataRequired()], format = '%m/%d/%Y')
    submit = SubmitField('Post')

    # time_commitment should contain an integer. 
    # NOTE: We make time_commitment a string to allow inputs like 30-40 hours.
    def validate_time_commitment(self, time_commitment):
        has_digit = False
        digits = []
        current_number = ""
        for char in time_commitment.data:
            if char.isdigit():
                has_digit = True
                current_number += char
            else: #if char is not a digit                
                if(len(current_number) > 0): # number has been built
                    digits.append(current_number)
                    current_number = ""   

        # One last check in case number was last in string
        if(len(current_number) > 0):
            digits.append(current_number)

        if(has_digit is False):
            raise ValidationError('Please enter desired hours as an integer.')

        if(len(digits) > 2):
            raise ValidationError('Please keep hours to either one integer or a range (ex. 20-30 hours)')
        # rebuild time commitment string
        time_commitment.data = ""
        time_commitment.data += (digits[0])

        if(len(digits) == 2): #if hour range -> add second hour
            time_commitment.data += (' - ')
            time_commitment.data += (digits[1])

    def validate_end_date(self, end_date):
        # start date must be before end date
        if (self.start_date.data > end_date.data):
            raise ValidationError('Start Date must be before End Date')



        
        

        

## Sort Form: Credit unknown TODO: Make comment block. Take responsibility for your actions.
class SortForm(FlaskForm):
    refresh = SubmitField('Refresh')
    checkbox = BooleanField('Display all other posts')

# ================================================================
#   Name:           Profile form
#   Description:    Class definition to update user's profile information
#   Last Changed:   11/15/21
#   Changed By:     Reagan Kelley
#   Change Details: Fixed run-time issues with form (Needs more work)
# ================================================================
class ProfileForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    wsu_id = StringField('WSU ID', validators=[Length(min = 8, max = 9)])
    phone_no = StringField('Phone Number', validators=[Length(max = 10)])
    #major = SelectField('Major', choices = [(0, 'CptS - Computer Science'), (1, 'EE - Electrical Engineering'), (2, 'CptSE - Computer Engineering'), (3, 'SE - Software Engineering'), (4, 'DA - Data Analytics')])
    major = QuerySelectField('Major', query_factory = all_majors, get_label = get_majorlabel, allow_blank = False)
    #major = TextAreaField("Filler for Major (Implement later)") ## TODO: Implement student major 
    gpa = FloatField('GPA', validators = [NumberRange(min = 0.0, max = 5.0)])
    expected_grad_date = DateField('Expected Graduation Date (mm/dd/yyyy)', format = '%m/%d/%Y')
    elect_courses = TextAreaField("Technical Elective Courses (Include Grades)")
    #research_topics = QuerySelectField('Select Resarch Topics') #TODO: Add tags from relationship
    #research_topics = TextAreaField("Filler for research topics (Implement later)")
    languages = TextAreaField('Programming Languages Experience')
    prior_research = TextAreaField('Describe your Prior Research Experience (If Any)')
    save = SubmitField('Save Changes')

    def is_email(self, email):
        user_emails = User.query.filter_by(email = email.data).all()
        for student_email in user_emails:
            if(student_email.id != current_user):
                raise ValidationError('The email is already associated with another account! Please use a different email address.')

# ================================================================
#   Name:           Application form
#   Description:    Class definition to update user's profile information
#   Last Changed:   11/15/21
#   Changed By:     Reagan Kelley
#   Change Details: Initial Implementation of Application Form
# ================================================================
class ApplicationForm(FlaskForm):
    personal_statement = TextAreaField("Brief Statement - Why do you want this position?", validators=[DataRequired(), Length(min=0, max = 1500)])
    faculty_ref_name = StringField("Provide One Faculty reference and their contact information", validators=[DataRequired(), Length(min=0, max = 60)])
    submit = SubmitField('Send Application')



