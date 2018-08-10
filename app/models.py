from . import db, elastic
from sqlalchemy import event
from flask import current_app, url_for
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,AnonymousUserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from markdown import markdown
from app.exceptions import ValidationError
import bleach
from app.models_math import Math_paper

class Warnsql(db.Model):
    __tablename__='warnsqls'
    id=db.Column(db.Integer,primary_key=True)
    timestamp=db.Column(db.DateTime(),index=True,default=datetime.utcnow)
    sql_statement=db.Column(db.Text())
    sql_parameters=db.Column(db.Text())
    sql_duration=db.Column(db.Float())
    sql_context=db.Column(db.Text())

class Post(db.Model):
    __tablename__='posts'
    id=db.Column(db.Integer,primary_key=True)
    body=db.Column(db.Text())
    body_html = db.Column(db.Text)
    timestamp=db.Column(db.DateTime(),index=True,default=datetime.utcnow)
    author_id=db.Column(db.Integer,db.ForeignKey('users.id'))

    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def to_json(self):
        json_post={
            'url': url_for('api.get_post', id=self.id),
            'body': self.body,
            'timestamp': self.timestamp,
            'author_url': url_for('api.get_user', id=self.author_id),
            'comments_url': url_for('api.get_post_comments', id=self.id),
            'comment_count': self.comments.count()
        }
        return json_post

    def to_es_json(self):
        import re
        dr = re.compile(r'<[^>]+>',re.S)
        body = dr.sub('',self.body)
        json_post={
            'id': self.id,
            'body': body,
            'timestamp': self.timestamp,
            'author_id': self.author_id,
            'body_html': self.body_html
        }
        return json_post

    @staticmethod
    def from_json(json_post):
        body = json_post.get('body')
        if body is None or body == '':
            raise ValidationError('不能保存空文章！')
        return Post(body=body)

    def get_enable_comments_count(self):
        return self.comments.filter(Comment.disabled==False).count()
    
    @staticmethod
    def generate_fake(count=100):
        from random import seed,randint
        import forgery_py
        
        seed()
        user_count=User.query.count()
        for i in range(count):
            u=User.query.offset(randint(0,user_count-1)).first()
            p=Post(body=forgery_py.lorem_ipsum.sentences(randint(1,3)),
                   timestamp=forgery_py.date.date(True),
                   author=u)
            db.session.add(p)
            db.session.commit()

    @staticmethod
    def init_comment():
        from random import seed,randint
        import forgery_py

        seed()
        user_count=User.query.count()
        for post in Post.query.all():
            seed()
            followed = randint(0,50)
            i=0
            while  i<followed:
                u=User.query.offset(randint(0,user_count-1)).first()
                p=Comment(body=forgery_py.lorem_ipsum.sentences(randint(1,3)),
                          timestamp=forgery_py.date.date(True),
                          author=u,
                          disabled = False,
                          post=post)
                db.session.add(p)
                i+=1
        db.session.commit()

#    @staticmethod
#    def on_changed_body(target, value, oldvalue, initiator):
#        pass
        #current_app.logger.info("文章编号："+str(target.id))
        #allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
        #                'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
        #                'h1', 'h2', 'h3', 'p', 'span', 'div', 'hr']
        #allowed_attr = ['class', 'id']        
        #
        #target.body_html = bleach.linkify(bleach.clean(
        #    markdown(value, output_format='html',extensions=['markdown.extensions.extra','markdown.extensions.codehilite','markdown.extensions.toc']),
        #    tags=allowed_tags, attributes=allowed_attr, strip=True))
        #
        #渲染内容 
        #target.body_html=markdown(value, output_format='html', extensions=['markdown.extensions.extra','markdown.extensions.codehilite','markdown.extensions.toc'])

#注册监听
#event.listen(MyBaseMixin, 'before_insert', get_created_by_id, propagate=True)
#db.event.listen(Post.body, 'set', Post.on_changed_body)

#文章自动添加索引
@db.event.listens_for(Post, 'after_update')
@db.event.listens_for(Post, 'after_insert')
def post_after_update(mapper, connection, target):
    elastic.index(index='flasky', doc_type='posts', id=target.id, body=target.to_es_json())
    current_app.logger.info("文章索引："+str(target.id))

class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    default=db.Column(db.Boolean,default=False,index=True)
    permissions=db.Column(db.Integer)
    users=db.relationship('User',backref='role',lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' %self.name

    @staticmethod
    def insert_roles():
        roles={
            'User':          [Permission.FOLLOW, Permission.COMMENT,Permission.WRITE],
            'Moderator':     [Permission.FOLLOW, Permission.COMMENT,Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT,Permission.WRITE, Permission.MODERATE,Permission.ADMIN],
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions=0
            for perm in roles[r]:
                role.permissions=role.permissions|perm
            if role.name == 'User':
                role.default=True
            else:
                role.default=False
            db.session.add(role)
        db.session.commit()
    
    #@permissions.setter
    #def permissions(self,perm):
    #    self.permissions=perm

class Follow(db.Model):
    __tablename__='follows'
    follower_id = db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    followed_id = db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    timestamp   = db.Column(db.DateTime,default=datetime.utcnow)

class User(UserMixin,db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(64),unique=True,index=True)
    username=db.Column(db.String(64),unique=True,index=True)
    password_hash=db.Column(db.String(128))
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))
    confirmed=db.Column(db.Boolean,default=False)
    
    name=db.Column(db.String(64))
    location=db.Column(db.String(64))
    about_me=db.Column(db.Text())
    member_since=db.Column(db.DateTime(),default=datetime.utcnow)
    last_seen=db.Column(db.DateTime(),default=datetime.utcnow)

    posts      = db.relationship('Post',backref='author',lazy='dynamic')
    math_papers= db.relationship('Math_paper',backref='user',lazy='dynamic')
    followed   = db.relationship('Follow',
                                foreign_keys=[Follow.follower_id],
                                backref=db.backref('follower',lazy='joined'),
                                lazy='dynamic',
                                cascade='all,delete-orphan')
    followers  = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed',lazy='joined'),
                                lazy='dynamic',
                                cascade='all,delete-orphan')
    comments   = db.relationship('Comment', backref='author', lazy='dynamic')

    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id),
            'username': self.username,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
            'posts_url': url_for('api.get_user_posts', id=self.id),
            'post_count': self.posts.count()
        }
        return json_user
    
    #获取API接口的密钥令牌 
    def generate_auth_token(self,expiration):
        s=Serializer(current_app.config['SECRET_KEY'],expires_in=expiration)
        return s.dumps({'id':self.id}).decode('utf-8')

    #接收一个密钥令牌并解析返回对应用户
    def verify_auth_token(token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def is_following(self,user):
        return self.followed.filter_by(followed_id=user.id).first() is not None  

    def follow(self,user):
        if not self.is_following(user):
            f=Follow(follower=self,followed=user)
            db.session.add(f)

    def unfollow(self,user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_followed(self,user):
        return self.followers.filter_by(follower_id=user.id).first() is not None

    def ping(self):
        self.last_seen=datetime.utcnow()
        db.session.add(self) 

    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        self.follow(self)
        if self.role is None:
            if self.email==current_app.config['FLASKY_ADMIN']:
                self.role=Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role=Role.query.filter_by(default=True).first()

    def generate_confirmation_token(self,expiration=3600):
        s=Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm':self.id})

    def confirm(self,token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token)
        except:
            return False
        if data.get('confirm')!=self.id:
            return False
        self.confirmed=True
        db.session.add(self)
        return True

    def generate_reset_token(self,expiration=3600):
        s=Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'resetpassword':self.id})

    @staticmethod
    def resetpassword(token,new_password):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token)
        except:
            return False
        user = User.query.get(data.get('resetpassword'))
        if user is None:
            return False
        user.password=new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self,new_email,expiration=3600):
        s=Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps( {'change_email': self.id, 'new_email': new_email})

    def change_email(self,token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    @property
    def password(self):
        raise AttributeError('password is not a readable attribut')

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return '<User %r>' %self.username

    def can(self,permissions):
        return self.role is not None and (self.role.permissions & permissions)==permissions

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    @staticmethod
    def generate_fake(count=100):
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u=User(email        = forgery_py.internet.email_address(),
                   username     = forgery_py.internet.user_name(True),
                   password     = forgery_py.lorem_ipsum.word(),
                   confirmed    = True,
                   name         = forgery_py.name.full_name(),
                   location     = forgery_py.address.city(),
                   about_me     = forgery_py.lorem_ipsum.sentence(),
                   member_since = forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
            except :
                db.session.rollback()

    @property
    def followed_posts(self):
        return Post.query.join(Follow, Follow.followed_id==Post.author_id).filter(Follow.follower_id==self.id)
    
    @staticmethod
    #初始化关注记录
    def init_follows():
        from random import randint
        user_count=User.query.count()
        for user in User.query.all():
            if not user.is_following(user):
                user.follow(user)
                db.session.add(user)
            followed = randint(0,10)
            i=0
            while  i<followed:
                u=User.query.offset(randint(0,user_count-1)).first()
                if not user.is_following(u):
                    user.follow(u)
                db.session.add(user)
                i+=1
        db.session.commit()

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def to_json(self):
        json_comment = {
            'url': url_for('api.get_comment', id=self.id),
            'post_url': url_for('api.get_post', id=self.post_id),
            'body': self.body,
            'timestamp': self.timestamp,
            'author_url': url_for('api.get_user', id=self.author_id),
        }
        return json_comment

    @staticmethod
    def from_json(json_comment):
        body = json_comment.get('body')
        if body is None or body == '':
            raise ValidationError('评论不能为空！')
        return Comment(body=body)

class AnonymousUser(AnonymousUserMixin):
    def can(self,permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user=AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#权限常量
class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE  = 4
    MODERATE = 8
    ADMIN = 16
    
