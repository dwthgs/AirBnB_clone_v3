#!/usr/bin/python3
"""
route for handling city objects and operations
"""
from models.city import City
from flask import jsonify, abort, request
from api.v1.views import app_views, storage


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def all_cities(state_id):
    """ Return of all cities """
    cities = []
    for city in storage.all("City").values():
        if city.state_id == state_id:
            cities.append(city.to_dict())
        # print(city.state_id)

    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def find_city(city_id=None):
    """Get a city"""
    city = storage.get("City", str(city_id))

    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """ Deletes a city """
    city = storage.get("City", str(city_id))

    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()

    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """ create city """
    newcity = request.get_json(silent=True)
    if newcity is None:
        abort(400, 'Not a JSON')

    if "name" not in newcity:
        abort(400, 'Missing name')

    if not storage.get("State", str(state_id)):
        abort(404)

    newcity["state_id"] = state_id
    new_city = City(**newcity)
    new_city.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route("cities/<city_id>",  methods=["PUT"], strict_slashes=False)
def city_put(city_id):
    """
    updates specific City object by ID
    :param city_id: city object ID
    :return: city object and 200 on success, or 400 or 404 on failure
    """
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get("City", str(city_id))
    if fetched_obj is None:
        abort(404)
    for key, val in city_json.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_json())
