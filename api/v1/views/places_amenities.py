#!/usr/bin/python3
"""
route for handling place and amenities linking
"""
from flask import jsonify, abort
from os import getenv
from api.v1.views import app_views, storage


@app_views.route("/places/<place_id>/amenities",
                 strict_slashes=False)
def amenity_by_place(place_id):
    """ get all amenities related with place """
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def unlink_amenity_from_place(place_id, amenity_id):
    """ delete an amenity in a place """

    if not storage.get("Place", place_id):
        abort(404)
    if not storage.get("Amenity", amenity_id):
        abort(404)

    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    found = 0

    for obj in place.amenities:
        if str(obj.id) == amenity_id:
            if getenv("HBNB_TYPE_STORAGE") == "db":
                place.amenities.remove(obj)
            else:
                place.amenity_ids.remove(obj.id)
            place.save()
            found = 1
            break

    if found == 0:
        abort(404)

    return jsonify({})


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=["POST"])
def link_place_amenity(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    required_place = storage.get("Place", place_id)
    if (not required_place):
        abort(404)

    required_amenity = storage.get("Amenity", amenity_id)
    if (not required_amenity):
        abort(404)

    if (getenv("HBNB_TYPE_STORAGE") != "db"):
        if amenity_id in required_place.amenities:
            return jsonify(required_amenity.to_dict()), 200
    else:
        if required_amenity in required_place.amenities:
            return jsonify(required_amenity.to_dict()), 200

    if (getenv("HBNB_TYPE_STORAGE") != "db"):
        required_place.amenities = required_amenity
        required_place.save()
        return jsonify(required_amenity.to_dict()), 201
    else:
        required_place.amenities.append(required_amenity)
        required_place.save()
        return jsonify(required_amenity.to_dict()), 201
