"""通用接口层"""
from flask import Blueprint

api = Blueprint('common', __name__)

from views.common.primary import *
