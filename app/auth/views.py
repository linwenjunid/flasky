from flask import render_template,redirect,request,url_for,flash
from . import auth
from ..models import User
from .forms import LoginForm,RegistrationForm,ChangePasswordForm,PasswordResetRequestForm,PasswordResetForm,ChangeEmailRequestForm
from flask_login import login_user,login_required,logout_user,current_user
from .. import db
from ..email import send_email

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.user',username=user.username))
        flash('Invalid username or password.')
    return render_template('auth/login.html',form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已退出登录。')
    return redirect(url_for('main.index'))

@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user=User(email=form.email.data,
                  username=form.username.data,
                  password=form.password.data)

        db.session.add(user)
        db.session.commit()
        token=user.generate_confirmation_token()

        send_email(user.email,'确认注册','auth/email/confirm',user=user,token=token)
        
        flash('A confirmation email has beeen sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('你已经确认了你的账户。谢谢！')
    else:
        flash('确认链接无效或已过期!')
    return redirect(url_for('main.index'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or  current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.before_app_request
def before_request():
    if current_user.is_authenticated: 
        current_user.ping()
        if not current_user.confirmed and request.endpoint[:5]!='auth.' and request.endpoint!='static':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token=current_user.generate_confirmation_token()
    send_email(current_user.email,'Confirm Your Account','auth/email/confirm',user=current_user,token=token)
    flash('一封新的确认邮件已经发送到你的注册邮箱。')
    return  redirect(url_for('main.index'))


@auth.route('/change_password',methods=['GET','POST'])
@login_required
def change_password():
    form=ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('密码已修改。')
            return redirect(url_for('main.index'))
        else:
            flash('密码不正确。')
    return render_template('auth/change_password.html',form=form)

@auth.route('/reset',methods=['GET','POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form=PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email,'密码重置','auth/email/resetpassword',user=user,token=token)
        flash('一封密码重置邮件已发送至你的邮箱，请查收！')
        return redirect(url_for('auth.login'))
    return render_template('auth/passwordresetrequest.html',form=form)

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form=PasswordResetForm()
    if form.validate_on_submit():
        if User.resetpassword(token,form.password.data):
            db.session.commit()
            flash('密码已重置。')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/passwordreset.html',form=form)

@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form=ChangeEmailRequestForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            token=current_user.generate_email_change_token(form.email.data)
            send_email(current_user.email,'变更邮箱','auth/email/changeemail',user=current_user,token=token)
            flash('一封变更邮箱的确认邮件已发送至你的邮箱，请查收！')
            return redirect(url_for('main.index'))
        else:
            flash('密码错误。')
    return render_template('auth/changeemailrequest.html',form=form)

@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('邮箱已变更。')
    else :
        flash('链接无效。')
    return redirect(url_for('main.index'))
