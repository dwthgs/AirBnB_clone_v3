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

    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def find_city(city_id=None):
    """Get a city"""
    city = storage.get("City", str(city_id))

    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route(
    '/cities/<city_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_city(city_id):
    """Deletes a city given the id"""
    city = storage.get('City', city_id)
    if city:
        city.delete()
        storage.save()
        return (jsonify({}), 200)
    abort(404)


@app_views.route(
    '/states/<state_id>/cities',
    methods=['POST'],
    strict_slashes=False)
def post_city(state_id):
    """Creates a city in a given state"""
    state = storage.get('State', state_id)
    city_dict = request.get_json()
    if not city_dict:
        return (jsonify({'error': 'Not a JSON'}), 400)
    elif 'name' not in city_dict:
        return (jsonify({'error': 'Missing name'}), 400)
    if state:
        city_dict['state_id'] = state.id
        city = City(**city_dict)
        city.save()
        return (jsonify(city.to_dict()), 201)
    abort(404)


@app_views.route(
    '/cities/<city_id>',
    methods=['PUT'],
    strict_slashes=False)
def put_city(city_id):
    """Updates an existing city"""
    city_dict = request.get_json()
    if not city_dict:
        return (jsonify({'error': 'Not a JSON'}), 400)
    city = storage.get('City', city_id)
    if city:
        city.name = city_dict['name']
        city.save()
        return (jsonify(city.to_dict()), 200)
    abort(404)
