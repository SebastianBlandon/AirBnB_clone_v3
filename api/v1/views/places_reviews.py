#!/usr/bin/python3
"""
    Same as City, create a new view for Place objects
    that handles all default RESTFul API actions:
"""
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """ Retrieves the list of all City objects """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    list_reviews = []
    for reviews in place.reviews:
        list_reviews.append(reviews.to_dict())
    return jsonify(list_reviews)


@app_views.route('reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ Retrieves a specific Place """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a Place Object """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_revi(place_id):
    """ Creates a Place """
    revie_w = storage.get(Place, place_id)
    if not revie_w:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'user_id' not in data:
        abort(400, description="Missing user_id")

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    if 'text' not in request.get_json():
        abort(400, description="Missing text")

    data['place_id'] = place_id
    instance = Review(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_reviews(review_id):
    """ Updates a Review object """
    place = storage.get(Review, review_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
