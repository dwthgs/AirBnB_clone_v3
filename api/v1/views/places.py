#!/usr/bin/python3
"""
route for handling place objects and operations
"""
from models.place import Place
from flask import jsonify, abort, request
from api.v1.views import app_views, storage


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def all_places(city_id):
    """ Return of all places """
    if city_id is None:
        abort(404)

    city = storage.get("Place", city_id)

    places = [place.to_dict() for place in city.values()]
    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False)
def find_place(place_id=None):
    """Get a place"""
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a place """
    if place_id is None:
        abort(404)

    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()

    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """ create place """
    newplace = request.get_json(silent=True)
    if newplace is None:
        abort(400, 'Not a JSON')

    if "name" not in newplace:
        abort(400, 'Missing name')

    if "user_id" not in newplace:
        abort(400, 'Missing user_id')

    if not storage.get("City", str(city_id)):
        abort(404)

    if not storage.get("User", str(newplace["user_id"])):
        abort(404)

    newplace["city_id"] = city_id
    new_place = Place(**newplace)
    new_place.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """ Updates a place """
    place = storage.get("Place", str(place_id))

    if place is None:
        abort(404)

    city_obj = request.get_json(silent=True)

    if city_obj is None:
        abort(400, "Not a json")

    for k, v in city_obj.items():
        if k not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict()), 200
