"""业务层"""
from flask import Blueprint

api = Blueprint('business', __name__)

from views.business.primary import *
