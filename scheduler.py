#/usr/bin/python3

import os
from app import create_app,db

app=create_app(os.getenv('FLASK_CONFIG') or 'default')

from flask_apscheduler import APScheduler
scheduler=APScheduler()
scheduler.init_app(app)
scheduler.start()

from app.models_job import Job
from app.jobtool.forms import JobForm
from flask import render_template,redirect,session,url_for,flash,current_app,request,abort,Blueprint

def runjob():
    with app.app_context():
        print('作业数:'+str(Job.query.count()))

@app.route('/addjob/', methods=['GET','POST'])
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
        return redirect(url_for('joblist'))
    return render_template('jobtool/addjob.html',form=form)

@app.route('/joblist/')
def joblist():
    page = request.args.get('page', 1, type=int)
    pagination = Job.query.order_by(Job.id.desc()).paginate(
        page, per_page=current_app.config['FLASKY_JOB_PER_PAGE'],
        error_out=False)
    jobs = pagination.items
    return render_template('jobtool/joblist.html', jobs=jobs, pagination=pagination)

if __name__=='__main__':
    app.run()

