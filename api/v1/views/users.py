#!/bin/usr/python3
"""This module generates views for the User class"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users/', strict_slashes=False, methods=['GET', 'POST'])
def users_no_id():
    '''returns json object and either gets or posts'''

    # Read
    if request.method == "GET":
        users = storage.all('User')
        list_of_users = [user.to_dict() for user in users.values()]
        return(jsonify(list_of_users))

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
        if j_obj.get('email') is None:
            abort(400, 'Missing email')
        if j_obj.get('password') is None:
            abort(400, 'Missing password')
        new_user = User(**j_obj)
        new_user.save()
        return(jsonify(new_object.to_dict()), 201)


@app_views.route('/users/<id>', strict_slashes=False, methods=["GET","PUT", "DELETE"])
def users_with_id(id):
    obj = storage.get('User', id)
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
        ignore_list = ['id','created_at','updated_at']
        # create dictionary of items to be updated
        bounce = {k: v for k, v in j_obj.items() if k not in ignore_list}
        # iter. across dict of items to be updated; setattr to update class obj
        for k, v in bounce.items():
            setattr(obj, k, v)
        obj.save()
        return(jsonify(obj.to_dict()))
