from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.core import BooleanField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import  DataRequired, Length
from wtforms.widgets.core import Select
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from app.Model.models import Post, Tag


def all_tags():
    return Tag.query.all()

# ================================================================
#   Name:           Post form
#   Description:    Class definition to create a new position post
#   Last Changed:   11/11/21
#   Changed By:     Reagan Kelley
#   Change Details: Initial Implementation
# ================================================================

class PostForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired()])
    body = TextAreaField("Job Description", [Length(min=0, max = 1500)])
    tags = QuerySelectMultipleField( 'Application Tags', query_factory= all_tags, get_label= lambda t: t.get_name(), widget=ListWidget(prefix_label=False), option_widget=CheckboxInput() )
    submit = SubmitField('Post')