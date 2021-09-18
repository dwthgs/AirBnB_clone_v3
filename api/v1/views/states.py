#!/usr/bin/python3
"""
route for handling State objects and operations
"""
from models.state import State
from flask import jsonify, abort, request
from api.v1.views import app_views, storage


@app_views.route("/states", strict_slashes=False)
def all():
    """ Return of all states """
    states = []
    for state in storage.all("State").values():
        states.append(state.to_dict())

    return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=False)
def get(state_id=None):
    """Get a state"""
    state = storage.get("State", state_id)

    if state is None:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def delete(state_id):
    """ Deletes a state """
    state = storage.get("State", str(state_id))

    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()

    return jsonify({})


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update(state_id):
    """ Updates a state """
    state = storage.get("State", str(state_id))

    if state is None:
        abort(404)

    state_obj = request.get_json(silent=True)

    if state_obj is None:
        abort(400, "Not a json")

    for k, v in state_obj.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict())


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create():
    """ create state """
    newstate = request.get_json(silent=True)
    if newstate is None:
        abort(400, 'Not a JSON')

    if "name" not in newstate:
        abort(400, 'Missing name')

    new_state = State(**newstate)
    new_state.save()

    return jsonify(new_state.to_dict()), 201
