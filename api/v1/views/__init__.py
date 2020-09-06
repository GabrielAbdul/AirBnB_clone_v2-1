#!/usr/bin/python3
'''__init__ module'''

from flask import Blueprint

app_views = Blueprint('app_views', __name__)
from api.v1.views.index import *
