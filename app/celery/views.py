from flask import render_template,redirect,session,url_for,flash,current_app,request,abort
from flask_login import login_required,current_user
from .. import db,celery
import datetime, time, random
from .tasks import mytask
from . import celerytool
from app.models_celery import Celery_task

@celerytool.route('/newtask/')
@login_required
def newtask():
    task = Celery_task()
    task.user=current_user
    db.session.add(task)
    db.session.commit()    

    celery_task = mytask.delay(task.id)

    task.task_id=celery_task.id
    db.session.add(task)
    db.session.commit()

    return redirect(url_for('celerytool.listtask'))

@celerytool.route('/status/<task_id>')
@login_required
def taskstatus(task_id):
    task = mytask.AsyncResult(task_id)
     
    return task.state+str(task.info)

@celerytool.route('/listtask/')
@login_required
def listtask():
    page = request.args.get('page', 1, type=int)
    pagination = Celery_task.query.filter(Celery_task.user_id==current_user.id).order_by(Celery_task.id.desc()).paginate(
        page, per_page=current_app.config['FLASKY_TASK_PER_PAGE'],
        error_out=False)
    tasks = pagination.items
    for task in tasks:
        t=mytask.AsyncResult(task.task_id)
        task.task_status=t.state
        if t.state=='PROGRESS':
            task.end_time=None
            task.task_percent=round(t.info.get('current')/t.info.get('total'),3)
        if t.state=='SUCCESS':
            task.end_time=datetime.datetime.strptime(t.info.get('end_time'),'%Y-%m-%d %H:%M:%S')
            task.task_percent=round(t.info.get('current')/t.info.get('total'),3)
        if t.state=='FAILURE':
            task.end_time=None
            task.task_percent=0
        db.session.add(task)
    db.session.commit() 
    return render_template('celery/listtask.html', tasks=tasks, pagination=pagination,page=page)
