from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired,Length

class JobForm(FlaskForm):
    jobname = StringField('名称',validators=[DataRequired(),Length(1,64)])
    args    = StringField('参数',validators=[Length(0,64)])
    year    = StringField('年',validators=[Length(0,64)],default='*')
    month   = StringField('月',validators=[Length(0,64)],default='*')
    day     = StringField('日',validators=[Length(0,64)],default='*')
    hour    = StringField('时',validators=[Length(0,64)],default='*')
    minute  = StringField('分',validators=[Length(0,64)],default='*')
    second  = StringField('秒',validators=[Length(0,64)],default='*')
    day_of_week = StringField('周',validators=[Length(0,64)],default='*')
    submit = SubmitField('添加')
