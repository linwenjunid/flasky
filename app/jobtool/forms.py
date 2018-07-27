from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired,Length

class JobForm(FlaskForm):
    jobname = StringField('名称',validators=[DataRequired(),Length(1,64)])
    args    = StringField('参数',validators=[Length(0,64)])
    year    = StringField('年',validators=[Length(0,64)])
    month   = StringField('月',validators=[Length(0,64)])
    day     = StringField('日',validators=[Length(0,64)])
    hour    = StringField('时',validators=[Length(0,64)])
    minute  = StringField('分',validators=[Length(0,64)])
    second  = StringField('秒',validators=[Length(0,64)])
    day_of_week = StringField('周',validators=[Length(0,64)])
    submit = SubmitField('添加')
