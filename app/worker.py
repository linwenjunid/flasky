#启动CELERY的WORKER专用的对象
from flask import Flask
from flask_celery import Celery
from config import config

app = Flask('worker')
app.config.from_object(config['default'])
celery = Celery(app)
