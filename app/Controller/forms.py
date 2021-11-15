from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.core import BooleanField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import  DataRequired, Length
from wtforms.widgets.core import Select
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from app.Model.models import Post, Major


def all_majors():
    return Major.query.all()

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
    majors = QuerySelectMultipleField( 'Recommended Majors', query_factory= all_majors, get_label= lambda t: t.get_major_name(), widget=ListWidget(prefix_label=False), option_widget=CheckboxInput() )
    submit = SubmitField('Post')

class SortForm(FlaskForm):
    refresh = SubmitField('Refresh')
    checkbox = BooleanField('Display all other posts')