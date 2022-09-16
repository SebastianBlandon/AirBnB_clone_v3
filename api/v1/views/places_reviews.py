#!/usr/bin/python3
"""
    Create a new view for Review object that handles
    all default RESTFul API actions:
"""
from models.amenity import Amenity
from models.place import Place
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_place_rev(place_id):
    """ Retrieves the list of all Amenities objects """
    place_rev = storage.get(Place, place_id)
    if not place_rev:
        abort(404)
    list_rev = []
    for pl_rev in place_rev.reviews:
        list_rev.append(pl_rev.to_dict())
    return jsonify(list_rev)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves a specific Amenity """
    ame_obj = storage.get(Amenity, amenity_id)
    if not ame_obj:
        abort(404)
    return jsonify(ame_obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes a Amenity Object """
    amenit = storage.get(Amenity, amenity_id)
    if not amenit:
        abort(404)
    storage.delete(amenit)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """ Creates a Amenity """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    data = request.get_json()
    instance = Amenity(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """ Updates a Amenity object """
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    ignore = ['id', 'created_at', 'updated_at']
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(amenity_obj, key, value)
    storage.save()
    return make_response(jsonify(amenity_obj.to_dict()), 200)
