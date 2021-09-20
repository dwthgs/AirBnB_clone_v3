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
                 methods=["POST"],
                 strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """ links a amenity with a place """

    place_obj = storage.get("Place", place_id)
    amenity_obj = storage.get("Amenity", amenity_id)
    amenity = None

    if not place_obj or not amenity_obj:
        abort(404)

    for obj in place_obj.amenities:
        if str(obj.id) == amenity_id:
            amenity = obj
            break

    if amenity is not None:
        return jsonify(amenity.to_json())

    if getenv("HBNB_TYPE_STORAGE") == "db":
        place_obj.amenities.append(amenity_obj)
    else:
        place_obj.amenities = amenity_obj

    place_obj.save()

    return jsonify(amenity_obj.to_json())
