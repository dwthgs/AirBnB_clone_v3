#!/usr/bin/python3
"""
route for handling city objects and operations
"""
from models.review import Review
from flask import jsonify, abort, request
from api.v1.views import app_views, storage


@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def all_reviews(place_id):
    """ Return of all reviews """
    place = storage.get('Place', place_id)

    if place is None:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def find_review(review_id=None):
    """Get a reviews"""
    review = storage.get("Review", review_id)

    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a review """
    review = storage.get("Review", review_id)

    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()

    return jsonify({})


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """ create review """
    newreview = request.get_json(silent=True)
    if newreview is None:
        abort(400, 'Not a JSON')

    if "user_id" not in newreview:
        abort(400, 'Missing user_id')

    if "text" not in newreview:
        abort(400, 'Missing text')

    if not storage.get("Place", place_id):
        abort(404)

    if not storage.get("User", newreview["user_id"]):
        abort(404)

    newreview["place_id"] = place_id
    new_review = Review(**newreview)
    new_review.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route("reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """ Updates review """
    review = storage.get("Review", review_id)

    if review is None:
        abort(404)

    review_obj = request.get_json(silent=True)

    if review_obj is None:
        abort(400, "Not a json")

    for k, v in review_obj.items():
        if k not in ["id", "user_id", "place_id",
                     "created_at", "updated_at"]:
            setattr(review, k, v)
    review.save()
    return jsonify(review.to_dict()), 200
