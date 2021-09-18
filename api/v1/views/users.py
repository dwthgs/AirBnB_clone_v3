#!/usr/bin/python3
"""
route for handling User objects and operations
"""
from models.user import User
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
import hashlib


@app_views.route("/users", strict_slashes=False)
def all_users():
    """ Return of all users """
    users = []
    for user in storage.all("User").values():
        users.append(user.to_dict())

    return jsonify(users)


@app_views.route('/users/<user_id>', strict_slashes=False)
def find_user(user_id=None):
    """Get User"""
    user = storage.get("User", str(user_id))

    if user is None:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes User """
    user = storage.get("User", str(user_id))

    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()

    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """ create User """
    newuser = request.get_json(silent=True)
    if newuser is None:
        abort(400, 'Not a JSON')

    if "email" not in newuser:
        abort(400, "Missing email")

    if "password" not in newuser:
        abort(400, "Missing password")

    newuser["password"] = hashlib.md5(
        newuser["password"].encode("utf8")).hexdigest()
    new_user = User(**newuser)
    new_user.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """ Updates User """
    user = storage.get("User", str(user_id))

    if user is None:
        abort(404)

    user_obj = request.get_json(silent=True)

    if user_obj is None:
        abort(400, "Not a json")

    user_obj["password"] = hashlib.md5(
        user_obj["password"].encode("utf8")).hexdigest()

    for k, v in user_obj.items():
        if k not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, k, v)
    user.save()
    return jsonify(user.to_dict()), 200
