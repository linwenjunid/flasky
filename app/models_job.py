from . import db,scheduler
from flask import jsonify,current_app
from apscheduler.jobstores.base import ConflictingIdError, JobLookupError

class Job(db.Model):
    __tablename__='jobs'
    id      = db.Column(db.Integer,primary_key=True)
    jobname = db.Column(db.String(64))
    func    = db.Column(db.String(64))
    args    = db.Column(db.String(64))
    jobtype = db.Column(db.String(64))
    trigger = db.Column(db.String(64),default='cron')
    year    = db.Column(db.String(64))
    month   = db.Column(db.String(64))
    day     = db.Column(db.String(64))
    hour    = db.Column(db.String(64))
    minute  = db.Column(db.String(64))
    second  = db.Column(db.String(64))
    week    = db.Column(db.String(64))
    day_of_week = db.Column(db.String(64))
    last_timestamp=db.Column(db.DateTime())
    is_enable  = db.Column(db.Boolean,default=False)
    status  = db.Column(db.String(64),default='None')

    @staticmethod
    def get_jobs():
        return scheduler.get_jobs()

    @staticmethod
    def add_job(id):
        job=Job.query.filter(Job.id==id).first()
        if job:
            try:
                args=[job.id,job.jobname]
                args=args+job.args.split(",")
                scheduler.add_job(func='__main__:runjob',
                              id          = str(job.id),
                              name        = job.jobname,
                              args        = args,
                              trigger     = job.trigger,
                              year        = job.year,
                              month       = job.month,
                              day         = job.day,
                              hour        = job.hour,
                              minute      = job.minute,
                              day_of_week = job.day_of_week,
                              second      = job.second,
                              replace_existing=True)
                job.is_enable=True
                db.session.add(job)
                db.session.commit()
                return True
            except ConflictingIdError:
                current_app.logger.info("作业%s已经启用。"%id) 
                return False
            except Exception as e:
                current_app.logger.info("作业%s启用操作出现异常:"%id+str(e))
                return False
        else:
            current_app.logger.info("作业%s不存在。"%id)
            return False

    @staticmethod
    def remove_job(id):
        job=Job.query.filter(Job.id==id).first()
        if job:
            try:
                scheduler.remove_job(str(job.id))
                job.is_enable=False
                db.session.add(job)
                db.session.commit()
                return True
            except JobLookupError:
                current_app.logger.info("作业%s未启用。"%id)
                return False
            except Exception as e:
                current_app.logger.info("作业%s禁用操作出现异常:"%id+str(e))
                return False
        else:
            current_app.logger.info("作业%s不存在。"%id)
            return False
