from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_ckeditor import CKEditor
from flask_apscheduler import APScheduler
from flask_elastic import Elastic
from .jinjafilters import myfilter
from flask_celery import Celery

bootstrap=Bootstrap()
moment=Moment()
mail=Mail()
db=SQLAlchemy()
pagedown=PageDown()
ckeditor = CKEditor()
scheduler=APScheduler()
elastic = Elastic()
celery = Celery()

login_manager=LoginManager()
login_manager.session_protection='strong'
login_manager.login_view='auth.login'
login_manager.login_message='请先登录。'

def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    #jinja2过滤器注册
    env = app.jinja_env
    env.filters['myfilter']=myfilter

    bootstrap.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    ckeditor.init_app(app)
    elastic.init_app(app)

    celery.init_app(app)

    scheduler.init_app(app)
    scheduler.start()

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint,url_prefix='/api/v1.0')

    from .jobtool import jobtool as jobtool_blueprint
    app.register_blueprint(jobtool_blueprint,url_prefix='/jobtool')
    
    from .mathtool import mathtool as math_blueprint
    app.register_blueprint(math_blueprint,url_prefix='/mathtool')

    from .search import search as search_blueprint
    app.register_blueprint(search_blueprint,url_prefix='/search')

    from .celery import celerytool as celery_blueprint
    app.register_blueprint(celery_blueprint,url_prefix='/celery')

    return app
