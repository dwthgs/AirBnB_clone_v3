#!/usr/bin/python3
"""
route for handling place objects and operations
"""
from models.place import Place
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from os import getenv


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def all_places(city_id):
    """ Return of all places """
    city = storage.get("City", city_id)

    if city is None:
        abort(404)

    places = [place.to_dict() for place in city.places]
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


def check_amenities(place):
    """ helper function """
    place_dict = place.to_dict()
    if "amenities" in place_dict:
        del place_dict["amenities"]
    return place_dict


@app_views.route('/places_search', methods=['POST'])
def create_search():
    """ Route search places based on JSON """
    amenities_l = []
    cities_l = []
    places_l = []
    if request.is_json:
        data = request.get_json()
        if len(data) is 0:
            places_l = storage.all('Place')
        else:
            if 'states' in data and len(data["states"]) is not 0:
                for my_states in data["states"]:
                    cities_l += storage.get('State', my_states).cities
            if 'cities' in data and len(data["cities"]) is not 0:
                cities_l.append(data["cities"])
                for my_cities in cities_l:
                    places_l += list(map(lambda x: x.places,
                                         storage.get('City', my_cities)))
            if 'amenities' in data and len(data["amenities"]) is not 0:
                if getenv("HBNB_TYPE_STORAGE") == 'db':
                    places_l += list(filter(lambda x:
                                            all(elem in
                                                list(map(lambda y: y.id,
                                                         x.amenities))
                                                for elem in data["amenities"]),
                                            storage.all('Place').values()))
                else:
                    places_l += list(filter(lambda x: all(elem in x.amenity_ids
                                            for elem in data["amenities"]),
                                            storage.all('Place').values()))
                if len(places_l) is 0:
                    places_l = storage.all('Place').values()
            print(places_l)
            print("*"*50)
            return jsonify(list(map(check_amenities, places_l))), 200
    else:
        return jsonify(error="Not a JSON"), 400
