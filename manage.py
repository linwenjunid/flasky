#/usr/bin/python3

import os
from datetime import datetime
from app import create_app,db,scheduler
from app.models import User,Role,Post,Follow,Comment
from app.models_job import Job
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand,upgrade

app=create_app(os.getenv('FLASK_CONFIG') or 'default')

def runjob(*args):
    with app.app_context():
        from app.models_job import Job
        job=Job.query.filter(Job.id==args[0]).first()
        app.logger.info("作业编码：%s作业名：%s"%(job.id,job.jobname))
        job.last_timestamp=datetime.utcnow()
        db.session.add(job)
        db.session.commit()

#初始化启动作业
with app.app_context():
    jobs=Job.query.filter(Job.is_enable==True).all()
    for job in jobs:
        Job.add_job(job.id)

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

if __name__=='__main__':
    manager.run()

