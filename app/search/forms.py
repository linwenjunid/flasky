from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired,Length

class SearchForm(FlaskForm):
    text = StringField('',validators=[Length(1,64)])
    submit = SubmitField('搜索')

