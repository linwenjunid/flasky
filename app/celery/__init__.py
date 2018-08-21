from flask import Blueprint

celerytool=Blueprint('celerytool',__name__)

from . import views

