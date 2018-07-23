from ..models import Post
from flask import jsonify
from . import api
from .authentication import auth

@api.route('/users/<int:id>')
def get_user(id):
    pass

@api.route('/users/<int:id>/posts')
def get_user_posts(id):
    pass

