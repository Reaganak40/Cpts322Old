from typing import Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.core import BooleanField, DateField, FloatField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import  DataRequired, Email, Length, NumberRange, Length, ValidationError
from wtforms.widgets.core import Select
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms_sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField
from app.Model.models import Permissions, Post, Major, User, Field
from flask_login import current_user


def get_majorlabel(theMajor):
    return theMajor.name

def all_majors():
    return Major.query.all()

def all_research_topics():
    #return ResearchField.query.all() #TODO: Change based on ResarchField object in models.py, otherwise comment out for testing
    pass

# ================================================================
#   Name:           Post form
#   Description:    Added sortform for filter posts on faculty view
#   Last Changed:   14/11/21
#   Changed By:     Reagan Kelley
#   Change Details: Initial Implementation
# ================================================================

class PostForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired()])
    body = TextAreaField("Job Description", [Length(min=0, max = 1500)])
    majors = QuerySelectMultipleField('Recommended Majors', query_factory= all_majors, get_label= lambda t: t.get_major_name(), widget=ListWidget(prefix_label=False), option_widget=CheckboxInput() )
    submit = SubmitField('Post')

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

class ApplicationForm(FlaskForm):
    personal_statement = TextAreaField("Brief Statement - Why do you want this position?", validators=[DataRequired(), Length(min=0, max = 1500)])
    faculty_ref_name = StringField("Provide One Faculty reference and their contact information", validators=[DataRequired(), Length(min=0, max = 60)])
    submit = SubmitField('Send Application')



