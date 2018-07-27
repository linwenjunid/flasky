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
        scheduler.add_job(func='__main__:runjob',id=str(job.id),trigger=job.trigger,second=job.second)
        return redirect(url_for('jobtool.joblist'))
    return render_template('jobtool/addjob.html',form=form)

@jobtool.route('/joblist/')
@login_required
def joblist():
    page = request.args.get('page', 1, type=int)
    pagination = Job.query.order_by(Job.id.desc()).paginate(
        page, per_page=current_app.config['FLASKY_JOB_PER_PAGE'],
        error_out=False)
    jobs = pagination.items
    return render_template('jobtool/joblist.html', jobs=jobs, pagination=pagination)
