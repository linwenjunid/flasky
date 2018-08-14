from . import db
from datetime import datetime
from random import seed,randint

class Math_config(db.Model):
    __tablename__='math_configs'
    id         = db.Column(db.Integer,primary_key=True)
    isInt      = db.Column(db.Boolean,default=True)
    minval     = db.Column(db.Integer,default=5)
    maxval     = db.Column(db.Integer,default=15)
    type       = db.Column(db.String(64),default='12')
    count      = db.Column(db.Integer,default=20)
    user_id    = db.Column(db.Integer,db.ForeignKey('users.id')) 

class Math_paper(db.Model):
    __tablename__='math_papers'
    id         = db.Column(db.Integer,primary_key=True)
    timestamp  = db.Column(db.DateTime(),index=True)
    user_id    = db.Column(db.Integer,db.ForeignKey('users.id'))
    q_args     = db.Column(db.String(64))
    score      = db.Column(db.Integer)
    score_flag = db.Column(db.Boolean,default=False)
    isInt      = db.Column(db.Boolean,default=True)
    minval     = db.Column(db.Integer)
    maxval     = db.Column(db.Integer)
    type       = db.Column(db.String(64))
    count      = db.Column(db.Integer,default=20)
    questions  = db.relationship('Math_question',backref='math_paper',lazy='dynamic')

    @staticmethod
    def generate_paper(current_user,isInt=True,minval=10,maxval=20,type='12',count=20):
        type1=tuple(type)
        flag=''
        if '1' in type1:
           flag='加'
        if '2' in type1:
           flag=flag+'减'
        if '3' in type1:
           flag=flag+'乘'
        if '4' in type1:
           flag=flag+'除'
        paper=Math_paper()
        paper.user=current_user
        paper.timestamp=datetime.utcnow()
        paper.q_args='整数：'+str(isInt)+', 范围：'+str(minval)+'-'+str(maxval)+', 数量：'+str(count)+', 类型：'+flag
        paper.isInt=isInt
        paper.minval=minval
        paper.maxval=maxval
        paper.type=type
        paper.count=count
        db.session.add(paper)
        db.session.commit()
        Math_question.generate_questions(paper)
        db.session.commit()
        return paper

class Math_question(db.Model):
    __tablename__='math_questions'
    id=db.Column(db.Integer,primary_key=True)
    paper_id=db.Column(db.Integer,db.ForeignKey('math_papers.id'))
    a=db.Column(db.Float)
    b=db.Column(db.Float)
    op=db.Column(db.Integer)
    val=db.Column(db.Float)
    key=db.Column(db.Float)
    result=db.Column(db.Float)

    @staticmethod
    def generate_questions(paper):
        for i in range(paper.count):
            if paper.isInt:
                db.session.add(Math_question.generate_questions_int(paper))

    @staticmethod
    def generate_questions_int(paper):
        q=Math_question()
        q.math_paper=paper
        type=tuple(paper.type)
        q.op=type[randint(0,50)%len(type)]
        a=randint(paper.minval,paper.maxval)
        b=randint(paper.minval,paper.maxval)
        #加法
        if q.op=='1':
            if randint(0,50)%3==0:
                q.b=min(a,b)
                q.val=max(a,b)
                q.key=abs(a-b)
            elif randint(0,50)%3==1:
                q.a=min(a,b)
                q.val=max(a,b)
                q.key=abs(a-b)
            else:
                q.a=a
                q.b=b
                q.key=a+b
        elif q.op=='2':
            if randint(0,50)%3==0:
                q.b=a
                q.val=b
                q.key=a+b
            elif randint(0,50)%3==1:
                q.a=max(a,b)
                q.val=min(a,b)
                q.key=q.a-q.val
            else:
                q.a=max(a,b)
                q.b=min(a,b)
                q.key=q.a-q.b
        elif q.op=='3':
            if randint(0,50)%3==0:
                q.b=b
                q.val=a*b
                q.key=a
            elif randint(0,50)%3==1:
                q.a=a
                q.val=a*b
                q.key=b
            else:  
                q.a=a
                q.b=b
                q.key=a*b
        elif q.op=='4':
            if randint(0,50)%3==0:
                q.b=a
                q.val=b
                q.key=a*b
            elif randint(0,50)%3==1:
                q.a=a*b
                q.val=b
                q.key=a
            else:
                q.a=a*b
                q.b=a
                q.key=b
        return q
