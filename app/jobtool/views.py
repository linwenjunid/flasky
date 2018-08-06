from flask import render_template,redirect,session,url_for,flash,current_app,request,abort
from flask_login import login_required,current_user
from .. import db,scheduler
from ..models_job import Job
from . import jobtool
from .forms import JobForm
import datetime

@jobtool.route('/addjob/', methods=['GET','POST'])
@login_required
def addjob():
    form=JobForm()
    if form.validate_on_submit():
        job=Job()
        job.jobname=form.jobname.data
        job.args=form.args.data
        job.jobtype='start'
        job.trigger='cron'
        job.year=form.year.data
        job.month=form.month.data
        job.day=form.day.data
        job.hour=form.hour.data
        job.minute=form.minute.data
        job.second=form.second.data
        job.day_of_week=form.day_of_week.data
        db.session.add(job)
        db.session.commit()
        current_app.logger.info('添加一个启动作业，ID：{}'.format(job.id))
        Job.add_job(job.id)
        return redirect(url_for('jobtool.listjob'))
    return render_template('jobtool/addjob.html',form=form)

@jobtool.route('/listjob/')
@login_required
def listjob():
    page = request.args.get('page', 1, type=int)
    pagination = Job.query.order_by(Job.id.desc()).paginate(
        page, per_page=current_app.config['FLASKY_JOB_PER_PAGE'],
        error_out=False)
    jobs = pagination.items
    return render_template('jobtool/listjob.html', jobs=jobs, pagination=pagination)

@jobtool.route('/status/<int:id>')
@login_required
def statusjob(id):
    job=Job.query.filter(Job.id==id).first()
    if job.is_enable:
        Job.remove_job(job.id)
    else :
        Job.add_job(job.id)

    return redirect(url_for('jobtool.listjob'))

@jobtool.route('/deljob/<int:id>')
@login_required
def deljob(id):
    job=Job.query.filter(Job.id==id).first()
    if job.is_enable:
        Job.remove_job(id)
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('jobtool.listjob'))




