import os
import random

from flask import render_template,redirect,session,url_for,flash,current_app,request,abort,send_from_directory
from datetime import datetime
from flask_login import login_required,current_user

from . import main
from .forms import NameForm,EditProfileForm,EditProfileAdminForm,PostForm
from .. import db
from ..models import User,Permission,Role,Post
from ..email import send_email
from ..decorators import admin_required,permission_required

from flask_ckeditor import upload_fail, upload_success

@main.route('/files/<filename>')
def uploaded_files(filename):
    path = current_app.config['UPLOADED_PATH'] 
    return send_from_directory(path, filename)

@main.route('/upload', methods=['POST'])
@login_required
def upload():
    f = request.files.get('upload')
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='请上传图片!')
    filename = current_user.username+str(datetime.now().strftime("%Y%m%d%H%M%S"))+str(random.randint(100,999))+'.'+extension
    f.save(os.path.join(current_app.config['UPLOADED_PATH'], filename))
    url = url_for('main.uploaded_files', filename=filename)
    return upload_success(url=url)

@main.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit(id):
    post=Post.query.get_or_404(id)
    if current_user != post.author and not current_user.can(Permission.ADMIN):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('博客已经更新.')
        return redirect(url_for('main.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form,post=post)


@main.route('/post/<int:id>')
def post(id):
    post=Post.query.get_or_404(id)
    return render_template('post.html',posts=[post])

@main.route('/',methods=['GET','POST'])
def index():
    form=PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post=Post(body=form.body.data,author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('main.index'))
    page=request.args.get('page',1,type=int)
    pagination=Post.query.order_by(Post.timestamp.desc()).paginate(page,
                                                                   per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                                   error_out=False)
    posts=pagination.items
    return render_template('index.html',form=form,posts=posts,current_time=datetime.utcnow(),pagination=pagination)

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page=request.args.get('page',1,type=int)
    pagination=user.posts.order_by(Post.timestamp.desc()).paginate(page,
                                                                   per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                                                   error_out=False)
    posts=pagination.items
    return render_template('user.html',user=user,posts=posts,pagination=pagination)

@main.route('/editprofile',methods=['GET','POST'])
@login_required
def editprofile():
    form=EditProfileForm()
    if form.validate_on_submit():
        current_user.name=form.name.data
        current_user.location=form.location.data
        current_user.about_me=form.about_me.data
        db.session.add(current_user)
        flash('资料已更新！')
        return redirect(url_for('main.user',username=current_user.username))
    form.name.data= current_user.name
    form.location.data=current_user.location
    form.about_me.data=current_user.about_me
    return render_template('editprofile.html',form=form)

@main.route('/editprofile/<int:id>',methods=['GET','POST'])
@login_required
@admin_required
def editprofileadmin(id):
    user=User.query.get_or_404(id)
    form=EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email     = form.email.data
        user.username  = form.username.data
        user.confirmed = form.confirmed.data
        user.role      = Role.query.get(form.role.data)
        user.name      = form.name.data
        user.location  = form.location.data
        user.about_me  = form.about_me.data
        db.session.add(user)
        flash('资料已更新')
        return redirect(url_for('main.user',username=user.username))
    form.email.data     = user.email      
    form.username.data  = user.username   
    form.confirmed.data = user.confirmed  
    form.role.data      = user.role_id    
    form.name.data      = user.name       
    form.location.data  = user.location   
    form.about_me.data  = user.about_me       
    return render_template('editprofile.html',form=form,user=user)

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
