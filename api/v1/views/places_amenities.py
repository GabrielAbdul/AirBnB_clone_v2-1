#!/usr/bin/python3
"""This module generates views for the State class"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage, storage_t
from models.review import Review


@app_views.route('/places/<place_id>/amenities', strict_slashes=False,
                 methods=['GET', 'POST'])
def reviews_no_id(place_id=None):
    '''returns json object and either gets or posts'''
    # Call state object
    place_obj = storage.get('Place', place_id)

    # NULL check
    if place_obj is None:
        abort(404)

    # Read
    if request.method == "GET":
        reviews = storage.all('Review')
        list_of_reviews = [c_obj.to_dict() for c_obj in reviews.values()
                           if c_obj.place_id == place_id]
        return(jsonify(list_of_reviews))

    # Create
    if request.method == 'POST':
        j_obj = request.get_json()
        if j_obj is None:
            abort(400, 'Not a JSON')
        if j_obj.get('user_id') is None:
            abort(400, 'Missing user_id')
        user_id = j_obj.get('user_id')
        user_obj = storage.get("User", user_id)
        if user_obj is None:
            abort(404)
        if j_obj.get('text') is None:
            abort(400, 'Missing text')
        j_obj['place_id'] = place_id
        review = Review(**j_obj)
        review.save()
        return jsonify(review.to_dict()), 201


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'], strict_slashes=False)
def amenities_by_places(place_id=None, amenity_id=None):
    '''method to interact with amenitiy objects'''
    if not place_id or not amenity_id:
        return 404

    # retrieve all places and amenities
    places = storage.all('Place')
    amenities = storage.all('Amenity')

    # get a list of place and amenity ids to compare input id
    valid_place_ids = list(map(lambda x: x.split('.')[1], places.keys()))
    valid_amenity_ids = list(map(lambda x: x.split('.')[1], amenities.keys()))

    if place_id not in valid_place_ids or amenity_id not in valid_amenity_ids:
        return 404

    # retrieve amenity and place obj that corresponds to input id
    amenity = storage.get('Amenity', amenity_id)
    place = storage.get('Place', place_id)

    if 'db' in storage_t:
        if 'DELETE' in request.methods:
            if amenity not in place.amenities:
                return 404
            place.amenities.remove(amenity)
            place.save()
            return jsonify({})
        elif 'POST' in request.methods:
            if amenity in place.amenities:
                return 202
            place.amenities.append(amenity)
            place.save()
            return jsonify(amenity.to_dict()), 201
    else:
        if 'DELETE' in request.methods:
            if amenity not in place.amenity_ids:
                return 404
            place.amenity_ids.remove(amenity)
            place.save()
            return jsonify({})
        elif 'POST' in request.methods:
            if amenity in place.amenity_ids:
                return 202
            place.amenity_ids.append(amenity)
            place.save()
            return jsonify(amenity.to_dict()), 201
