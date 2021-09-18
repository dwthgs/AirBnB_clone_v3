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
def city_create(state_id):
    """
    create city route
    param: state_id - state id
    :return: newly created city obj
    """
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')

    if not storage.get("State", str(state_id)):
        abort(404)

    if "name" not in city_json:
        abort(400, 'Missing name')

    city_json["state_id"] = state_id

    new_city = City(**city_json)
    new_city.save()
    resp = jsonify(new_city.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
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
