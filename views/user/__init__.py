"""用户层"""
from flask import Blueprint

api = Blueprint('user', __name__, url_prefix='/user')

from views.user.primary import *
