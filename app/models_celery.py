from . import db
from datetime import datetime

class Celery_task(db.Model):
    __tablename__='celery_tasks'
    id           = db.Column(db.Integer,primary_key=True)
    start_time   = db.Column(db.DateTime(),default=datetime.utcnow)
    end_time     = db.Column(db.DateTime())
    task_id      = db.Column(db.String(64))
    task_status  = db.Column(db.String(64))
    task_percent = db.Column(db.Float)
    user_id      = db.Column(db.Integer,db.ForeignKey('users.id')) 

