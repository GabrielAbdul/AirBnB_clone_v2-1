#!/usr/bin/python3
"""This module generates views for the State class"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET', 'POST'])
def amenities_no_id():
    '''returns json object and either gets or posts'''

    # Read
    if request.method == "GET":
        amenities = storage.all('Amenity')
        list_of_amenities = [am.to_dict() for am in amenities.values()]
        return(jsonify(list_of_amenities))

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
        new_am = Amenity(**j_obj)
        new_am.save()
        return(jsonify(new_am.to_dict()), 201)


@app_views.route('/amenities/<id>', strict_slashes=False,
                 methods=["GET", "PUT", "DELETE"])
def amenites_with_id(id):
    obj = storage.get('Amenity', id)
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
        return (jsonify({}), 200)

    # Update
    if request.method == "PUT":
        j_obj = request.get_json()
        if j_obj is None:
            abort(400, 'Not a JSON')
        # List of objects to be ignored on iteration
        ignore_list = ['id', 'created_at', 'updated_at']
        # create dictionary of items to be updated
        bounce = {k: v for k, v in j_obj.items() if k not in ignore_list}
        # iter. across dict of items to be updated; setattr to update class obj
        for k, v in bounce.items():
            setattr(obj, k, v)
        obj.save()
        return jsonify(obj.to_dict()), 200
