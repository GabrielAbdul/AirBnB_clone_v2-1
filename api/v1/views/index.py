#!/usr/bin/python3
'''__init__ module'''
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status')
def api_stats():
    '''reuturns JSON stats of API'''
    return(jsonify({'status': 'OK'}))
