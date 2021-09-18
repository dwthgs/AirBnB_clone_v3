#!/usr/bin/python3
"""
route for handling Amenity objects and operations
"""
from models.amenity import Amenity
from flask import jsonify, abort, request
from api.v1.views import app_views, storage


@app_views.route("/amenities", strict_slashes=False)
def all_amenities():
    """ Return of all amenities """
    amenities = [obj.to_dict() for obj in storage.all("Amenity").values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def find_amenity(amenity_id=None):
    """Get Amenity"""
    amenity = storage.get("Amenity", str(amenity_id))

    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes Amenity """
    amenity = storage.get("Amenity", str(amenity_id))

    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """ create Amenity """
    newamenity = request.get_json(silent=True)
    if newamenity is None:
        abort(400, 'Not a JSON')

    if "name" not in newamenity:
        abort(400, 'Missing name')

    new_amenity = Amenity(**newamenity)
    new_amenity.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates Amenity """
    amenity = storage.get("Amenity", str(amenity_id))

    if amenity is None:
        abort(404)

    amenity_obj = request.get_json(silent=True)

    if amenity_obj is None:
        abort(400, "Not a json")

    for k, v in amenity_obj.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
