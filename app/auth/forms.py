from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    email=StringField('邮箱',validators=[DataRequired(),Length(1,64),Email()])

    password=PasswordField('密码',validators=[DataRequired()])

    remember_me=BooleanField('自动登录')

    submit = SubmitField('登录')

class RegistrationForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Length(1,64),Email()])

    username=StringField('Username',
                         validators=[DataRequired(),
                                     Length(1,64),
                                     Regexp('^[A-Za-z\u4E00-\u9FA5][A-Za-z0-9\u4E00-\u9FA5_.]*$',0,'Usernames must have only letters,numbers,dots or underscores')])

    password=PasswordField('Password',
                           validators=[DataRequired(),
                                       EqualTo('password2',message='Passwords must match.')])

    password2=PasswordField('Confirm password',
                           validators=[DataRequired()])

    submit = SubmitField('Register')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

class ChangePasswordForm(FlaskForm):

    old_password = PasswordField('旧密码', validators=[DataRequired()])

    password = PasswordField('新密码', validators=[DataRequired(), EqualTo('password2', message='新密码两次输入不一致。')])

    password2 = PasswordField('重复新密码',validators=[DataRequired()])

    submit = SubmitField('确定')

class PasswordResetRequestForm(FlaskForm):
   
    email=StringField('邮箱',validators=[DataRequired(),Length(1,64),Email()])

    submit = SubmitField('重置密码')
    
class PasswordResetForm(FlaskForm):
    
    password = PasswordField('新密码', validators=[DataRequired(), EqualTo('password2', message='新密码两次输入不一致。')])

    password2 = PasswordField('重复新密码',validators=[DataRequired()])

    submit = SubmitField('确定')

class ChangeEmailRequestForm(FlaskForm):
    
    email=StringField('新邮箱',validators=[DataRequired(),Length(1,64),Email()])

    password = PasswordField('密码',validators=[DataRequired()])

    submit = SubmitField('变更邮箱')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已注册。')


