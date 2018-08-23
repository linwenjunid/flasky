from flask import render_template,redirect,session,url_for,flash,current_app,request,abort,jsonify
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

@celerytool.route('/test/<task_id>')
@login_required
def test(task_id):
    t = mytask.AsyncResult(task_id)
    task_percent=0
    if t.state in ('PROGRESS','SUCCESS'):
        task_percent=round(t.info.get('current')*100/t.info.get('total'),1)
    return render_template('celery/test.html', task_id=task_id ,task_percent=task_percent)

@celerytool.route('/status/<task_id>')
@login_required
def taskstatus(task_id):
    t = mytask.AsyncResult(task_id)
    task_percent=0
    end_time = None
    if t.state in ('PROGRESS','SUCCESS'):
        task_percent = str(round(t.info.get('current')*100/t.info.get('total'),1))
    if t.state in ('SUCCESS'):
        end_time = t.info.get('end_time')
    return jsonify({
        'task_status'  : t.state,
        'task_percent' : task_percent, 
        'end_time'     : end_time
    })

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
            task.task_percent=round(t.info.get('current')*100/t.info.get('total'),1)
        elif t.state=='SUCCESS':
            task.end_time=datetime.datetime.strptime(t.info.get('end_time'),'%Y-%m-%d %H:%M:%S')
            task.task_percent=round(t.info.get('current')*100/t.info.get('total'),1)
        else:
            task.end_time=None
            task.task_percent=0
        db.session.add(task)
    db.session.commit() 
    return render_template('celery/listtask.html', tasks=tasks, pagination=pagination,page=page)
