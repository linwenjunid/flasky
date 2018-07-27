from flask import Blueprint

jobtool=Blueprint('jobtool',__name__)

from . import views

