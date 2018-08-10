#/usr/bin/python3

import os
from datetime import datetime
from app import create_app,db,scheduler
from app.models import User,Role,Post,Follow,Comment
from app.models_job import Job
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand,upgrade

def runjob(*args):
    with app.app_context():
        from app.models_job import Job
        job=Job.query.filter(Job.id==args[0]).first()
        app.logger.info("作业编码：%s作业名：%s"%(job.id,job.jobname))
        job.last_timestamp=datetime.now()
        db.session.add(job)
        db.session.commit()

app=create_app(os.getenv('FLASK_CONFIG') or 'default')

#文件锁保证任务只初始化一次
import atexit
import fcntl
f = open("scheduler.lock", "wb")
try:
    fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
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

manager=Manager(app)
migrate = Migrate(app,db)

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role,Post=Post,Follow=Follow,Comment=Comment)
manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

@manager.command
def deploy():
    upgrade()
    Role.insert_roles()
    Post.init_es_post()

if __name__=='__main__':
    manager.run()
