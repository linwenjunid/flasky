from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired,Length

class QuestionsForm(FlaskForm):
    result = StringField('',validators=[Length(0,64)])
    submit = SubmitField('确认')

