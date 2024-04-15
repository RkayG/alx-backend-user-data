#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User
import os


@app_views.route(
    '/auth_session/login', methods=['POST'],
    strict_slashes=False)
def loginWithCookie() -> str:
    """Login in with a set cookie
    Returns:
        str: your details as a user
    """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400
    users = User().search({'email': email})
    if not users or users == []:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            s_id = auth.create_session(user.id)
            key = os.environ.get('SESSION_NAME')
            val = jsonify(user.to_json())
            val.set_cookie(key, s_id)
            return val
    return jsonify({"error": "wrong password"}), 401

@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """Logout
    Returns:
     - (str) an empty dictionary and a success status code
    """
    from api.v1.app import auth
    destroyed = auth.destroy_session(request)
    if not destroyed:
        abort(404)
    return jsonify({}), 200
