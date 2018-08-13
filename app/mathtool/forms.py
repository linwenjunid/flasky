from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField,SelectMultipleField,IntegerField
from wtforms.validators import DataRequired,Length

class QuestionsForm(FlaskForm):
    result = StringField('',validators=[Length(0,64)])
    submit = SubmitField('确认')


class ConfigForm(FlaskForm):
    isInt  = BooleanField('是否整数')
    type   = SelectMultipleField('计算类型', choices=[('1','加'),('2','减'),('3','乘'),('4','除')])
    minval = IntegerField('数值下限')
    maxval = IntegerField('数值上限')
    count  = IntegerField('题目数量')
    submit = SubmitField('确认')
