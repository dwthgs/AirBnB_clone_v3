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


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletestate(state_id=None):
    """Deletes a state"""
    s = storage.get("State", state_id)
    if s is None:
        abort(404)
    else:
        storage.delete(s)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def createstate():
    """Create a state"""
    s = request.get_json(silent=True)
    if s is None:
        abort(400, "Not a JSON")
    elif "name" not in s.keys():
        abort(400, "Missing name")
    else:
        new_s = State(**s)
        storage.new(new_s)
        storage.save()
        return jsonify(new_s.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def updatestate(state_id=None):
    """Update a state"""
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)

    s = request.get_json(silent=True)
    if s is None:
        abort(400, "Not a JSON")
    else:
        for k, v in s.items():
            if k in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(obj, k, v)
        storage.save()
        res = obj.to_dict()
        return jsonify(res), 200
