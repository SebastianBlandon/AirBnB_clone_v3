#!/usr/bin/python3
"""
    Same as City, create a new view for Place objects
    that handles all default RESTFul API actions:
"""
from models.amenity import Amenity
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response
import os


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """ Retrieves the list of all City objects """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    list_amenities = []
    for amenities in place.amenities:
        list_amenities.append(amenities.to_dict())
    return jsonify(list_amenities)


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """ Deletes a Place Object """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)

    if os.environ.get('HBNB_TYPE_STORAGE') == "db":
        if amenity not in place.amenities:
            abort(404)
        storage.delete(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        storage.delete(amenity_id)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """ Creates a Place """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)
    
    return make_response(jsonify(amenity.to_dict()), 201)
