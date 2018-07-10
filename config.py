import os

class Config:
    '''
    本地加载JS   BOOTSTRAP_SERVE_LOCAL
    '''
    BOOTSTRAP_SERVE_LOCAL = True
    SECRET_KEY=os.environ.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_MAIL_SUBJECT_PREFIX='Flasky'
    FLASKY_MAIL_SENDER='Flasky Admin <'+os.environ.get('MAIL_USERNAME')+'>'
    FLASKY_ADMIN=os.environ.get('FLASKY_ADMIN')
    #分页每页显示记录数
    FLASKY_POSTS_PER_PAGE=10
    FLASKY_FOLLOWERS_PER_PAGE=10
    FLASKY_COMMENTS_PER_PAGE=10
    FLASKY_USER_PER_PAGE=10
    #ckeditor引入本地资源
    CKEDITOR_SERVE_LOCAL=True
    #ckeditor代码高亮
    CKEDITOR_ENABLE_CODESNIPPET=True
    CKEDITOR_CODE_THEME='github'
    CKEDITOR_HEIGHT=400
    CKEDITOR_FILE_UPLOADER='main.upload'
    UPLOADED_PATH=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    #UPLOADED_PATH='/uploads'

    @staticmethod
    def init_app(app):
        pass

class DeveConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVE_SQLURL')
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:hadoop@192.168.134.201:3306/flasky?charset=utf8'
    DEBUG=True
    MAIL_SERVER='smtp.163.com'
    MAIL_PORT=465
    MAIL_USE_SSL=True
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
   
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_SQLURL')
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:hadoop@192.168.134.201:3306/flaskytest?charset=utf8'
    TESTING=True

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_SQLURL')
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:hadoop@192.168.134.201:3306/flasky?charset=utf8'
    TESTING=False

config={
    'development':DeveConfig,
    'testing':TestConfig,
    'production':ProdConfig,

    'default':DeveConfig
}

