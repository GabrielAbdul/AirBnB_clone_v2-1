#!/usr/bin/python3
"""This module generates views for the State class"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET', 'POST'])
def cities_no_id(state_id=None):
    '''returns json object and either gets or posts'''

    # Call state object
    state_obj = storage.get('State', state_id)

    # NULL check
    if state_obj is None:
        abort(404)

    # Read
    if request.method == "GET":
        cities = storage.all('City')
        list_of_cities = [c_obj.to_dict() for c_obj in cities.values()
                          if c_obj.state_id == state_id]
        return(jsonify(list_of_cities))

    # Create
    if request.method == "POST":
        # convert to json
        j_obj = request.get_json()
        # null/not json check
        if j_obj is None:
            abort(400, 'Not a JSON')
        # no name check
        if j_obj.get('name') is None:
            abort(400, 'Missing name')
        j_obj['state_id'] = state_id
        new_city = City(**j_obj)
        new_city.save()
        return(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<id>',
                 strict_slashes=False, methods=["GET", "PUT", "DELETE"])
def cities_with_id(id):
    obj = storage.get('City', id)
    if obj is None:
        abort(404)
    # Read
    if request.method == "GET":
        return(jsonify(obj.to_dict()))

    # Delete
    if request.method == "DELETE":
        obj.delete()
        storage.save()
        del obj
        return (jsonify({}))

    # Update
    if request.method == "PUT":
        j_obj = request.get_json()
        if j_obj is None:
            abort(400, 'Not a JSON')
        # List of objects to be ignored on iteration
        ignore_list = ['id', 'created_at', 'updated_at', 'state_id']
        # create dictionary of items to be updated
        bounce = {k: v for k, v in j_obj.items() if k not in ignore_list}
        # iter. across dict of items to be updated; setattr to update class obj
        for k, v in bounce.items():
            setattr(obj, k, v)
        obj.save()
        return(jsonify(obj.to_dict()))
