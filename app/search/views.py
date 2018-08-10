from flask import render_template,redirect,session,url_for,flash,current_app,request,abort,g
from .forms import SearchForm
from . import search
from .. import elastic

@search.route('/search', methods = ['POST'])
def search():
    form = SearchForm()
    #这里的表单可以从g里面获取
    if form.validate_on_submit():
        body = {
            "query":{
                "match":{
                    "body":form.text.data
                }
            },
            "highlight": {
                "fields": {
                    "body":{
                        "pre_tags"  : ["<em><font color='red'>"],
                        "post_tags" : ["</font></em>"]
                    }
                }
            }
        }
        res=elastic.search(index="flasky",doc_type="posts",body=body)
        posts=res['hits']['hits'][0:9]
        return render_template('search/list_search.html', posts=posts)
    return redirect(url_for('main.index'))
