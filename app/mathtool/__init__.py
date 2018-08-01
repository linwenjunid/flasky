from flask import Blueprint

mathtool=Blueprint('mathtool',__name__)

from . import views

