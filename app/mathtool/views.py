from flask import render_template,redirect,session,url_for,flash,current_app,request,abort
from flask_login import login_required,current_user
from .. import db
from ..models_math import Math_paper,Math_question
from . import mathtool
from .forms import QuestionsForm
from sqlalchemy import and_

@mathtool.route('/newpaper/', methods=['GET','POST'])
@login_required
def newpaper():
    Math_paper.generate_paper(current_user,isInt=True,minval=0,maxval=20,type='12',count=20)
    return redirect(url_for('mathtool.listpaper'))

@mathtool.route('/listpaper/')
@login_required
def listpaper():
    page = request.args.get('page', 1, type=int)
    pagination = Math_paper.query.filter(Math_paper.user_id==current_user.id).order_by(Math_paper.id.desc()).paginate(
        page, per_page=current_app.config['FLASKY_PAPER_PER_PAGE'],
        error_out=False)
    papers = pagination.items
    return render_template('mathtool/listpaper.html', papers=papers, pagination=pagination,page=page)

@mathtool.route('/delpaper/<int:id>')
@login_required
def delpaper(id):
    page = request.args.get('page', 1, type=int)
    paper=Math_paper.query.get_or_404(id)
    db.session.query(Math_question).filter(Math_question.paper_id==paper.id).delete()
    db.session.delete(paper)
    db.session.commit()
    return redirect(url_for('mathtool.listpaper',page=page))

@mathtool.route('/startpaper/<int:pid>/<int:qid>', methods=['GET','POST'])
@login_required
def startpaper(pid,qid):
    paper=Math_paper.query.get_or_404(pid)
    if paper.score_flag :
        flash('测试已完成，不能再次测试')
        page = request.args.get('page', 1, type=int)
        return redirect(url_for('mathtool.listpaper',page=page))
    form=QuestionsForm()
    if form.validate_on_submit():
        question=Math_question.query.filter(Math_question.paper_id==pid).order_by(Math_question.id).offset(qid).first()
        question.result=form.result.data or 0
        db.session.add(question)
        db.session.commit()
        if qid==Math_paper.query.get_or_404(pid).count-1:
            paper=Math_paper.query.get_or_404(pid)
            paper.score=(100/Math_paper.query.get_or_404(pid).count)*Math_question.query.filter(and_(Math_question.paper_id==pid,Math_question.key==Math_question.result)).count()
            paper.score_flag=True
            db.session.add(paper)
            db.session.commit()
            return redirect(url_for('mathtool.listpaper'))
        return redirect(url_for('mathtool.startpaper',pid=pid,qid=qid+1))
    question=Math_question.query.filter(Math_question.paper_id==pid).order_by(Math_question.id).offset(qid).first()
    return render_template('mathtool/startpaper.html',form=form,q=question,qid=qid)

@mathtool.route('/listquestion/<int:id>')
@login_required
def listquestion(id):
    paper=Math_paper.query.get_or_404(id)
    questions=Math_question.query.filter(Math_question.paper_id==id).order_by(Math_question.id).all()
    return render_template('mathtool/listquestion.html',questions=questions,paper=paper)



