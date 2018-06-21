from flask import render_template,redirect,session,url_for,flash,current_app
from datetime import datetime
from flask_login import login_required

from . import main
from .forms import NameForm
from .. import db
from ..models import User,Permission
from ..email import send_email
from ..decorators import admin_required,permission_required

@main.route('/')
def index():
    return render_template('index.html',current_time=datetime.utcnow())

@main.route('/user',methods=['GET','POST'])
@login_required
@permission_required(Permission.WRITE)
def user():
    form=NameForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.name.data).first()
        if user is None:
            user=User(username=form.name.data)
            db.session.add(user)
            session['known']=False
            flash('New User!')
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['FLASKY_ADMIN'],'New User','mail/new_user',user=user)
        else:
            session['known']=True
        session['name']=form.name.data
        form.name.data=''
        return redirect(url_for('.user'))
    return render_template('user.html',
        name=session.get('name'),form=form,known=session.get('known',False))

@main.route('/admin')
@login_required
@admin_required
def admin():
    return render_template('admin.html')

@main.route('/moder')
@login_required
@permission_required(Permission.MODERATE)
def moder():
    return render_template('moder.html')
