#/usr/bin/python3

import os
from app import create_app
from app.models_job import Job
from app import db
from datetime import datetime

app=create_app(os.getenv('FLASK_CONFIG') or 'default')

def runjob(*args):
    with app.app_context():
        from app.models_job import Job
        job=Job.query.filter(Job.id==args[0]).first()
        app.logger.info("作业编码：%s作业名：%s"%(job.id,job.jobname))
        job.last_timestamp=datetime.now()
        db.session.add(job)
        db.session.commit()


import atexit
import fcntl
f = open("scheduler.lock", "wb")
try:
    with app.app_context():
        jobs=Job.query.filter(Job.is_enable==True).all()
        for job in jobs:
            Job.add_job(job.id)
except:
    pass
def unlock():
    fcntl.flock(f, fcntl.LOCK_UN)
    f.close()
atexit.register(unlock)

if __name__=='__main__':
    app.run()

