#!/usr/bin/python3
'''__init__ module'''
from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/status')
def api_stats():
    '''returns JSON stats of API'''
    return(jsonify({'status': 'OK'}))


@app_views.route('/stats')
def stats():
    '''returns JSON stats of API'''
    resp = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
        }
    return(jsonify(resp))
