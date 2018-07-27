from . import db

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
