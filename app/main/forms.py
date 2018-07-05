from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,SelectField,BooleanField
from wtforms.validators import Length,Email,Regexp,DataRequired
from wtforms import ValidationError
from ..models import Role,User
from flask_pagedown.fields import PageDownField
from flask_ckeditor import CKEditorField

class PostForm(FlaskForm):
    body=CKEditorField("",validators=[DataRequired('内容不能为空！')])
    submit = SubmitField('发布')

class NameForm(FlaskForm):
    name = StringField('What is your name?',validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
    name = StringField('姓名',validators=[Length(0,64)])
    location = StringField('地址',validators=[Length(0,64)])
    about_me = TextAreaField('自我介绍')
    submit = SubmitField('确定')

class EditProfileAdminForm(FlaskForm):
    email=StringField('邮箱',validators=[DataRequired(),Length(1,64),Email()])
    username=StringField('Username',
                         validators=[DataRequired(),
                                     Length(1,64),
                                     Regexp('^[A-Za-z\u4E00-\u9FA5][A-Za-z0-9\u4E00-\u9FA5_.]*$',0,'Usernames must have only letters,numbers,dots or underscores')])

    confirmed = BooleanField('认证')
    role = SelectField('角色',coerce=int)
    name = StringField('姓名',validators=[Length(0,64)])
    location = StringField('地址',validators=[Length(0,64)])
    about_me = TextAreaField('自我介绍')
    submit = SubmitField('确定')

    def __init__(self,user,*args,**kwargs):
        super(EditProfileAdminForm,self).__init__(*args,**kwargs)
        self.role.choices=[(role.id,role.name) for role in Role.query.order_by(Role.name).all()]
        self.user=user

    def validate_email(self,field):
        if field.data!=self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册！')

    def validate_username(self,field):
        if field.data!=self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被使用！')
