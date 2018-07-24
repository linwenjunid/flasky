#/usr/bin/python3

import os
from app import create_app,db
from app.models import User,Role,Post,Follow,Comment
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand,upgrade

app=create_app(os.getenv('FLASK_CONFIG') or 'default')

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

