#!/usr/bin/python3
"""
route for handling city objects and operations
"""
from models.city import City
from flask import jsonify, abort, request
from api.v1.views import app_views, storage


@app_views.route("/cities", strict_slashes=False)
def all():
    """ Return of all cities """
    cities = []
    for city in storage.all("City").values():
        cities.append(city.to_dict())

    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get(city_id=None):
    """Get a city"""
    city = storage.get("City", str(city_id))

    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete(city_id):
    """ Deletes a city """
    city = storage.get("City", str(city_id))

    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()

    return jsonify({}), 200


@app_views.route("/cities", methods=["POST"], strict_slashes=False)
def create():
    """ create city """
    newcity = request.get_json(silent=True)
    if newcity is None:
        abort(400, 'Not a JSON')

    if "name" not in newcity:
        abort(400, 'Missing name')

    new_city = City(**newcity)
    new_city.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update(city_id):
    """ Updates a city """
    city = storage.get("City", str(city_id))

    if city is None:
        abort(404)

    city_obj = request.get_json(silent=True)

    if city_obj is None:
        abort(400, "Not a json")

    for k, v in city_obj.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict()), 200
