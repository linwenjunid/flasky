from . import api
from ..models import Comment
from flask import jsonify

@api.route('/comments/<int:id>')
def get_comment(id):
    comment = Comment.query.get_or_404(id)
    return jsonify(comment.to_json())
