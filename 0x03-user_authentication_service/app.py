#!/usr/bin/env python3
"""A minimalist app"""
from flask import Flask, jsonify, abort, request, redirect
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=['GET'])
def greet():
    """Gives a greeting"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def signup():
    """Signs up a user"""
    em = request.form.get('email')
    pwd = request.form.get('password')
    try:
        user = AUTH.register_user(em, pwd)
        return jsonify({"email": em, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login():
    """"Logs in a user"""
    em = request.form.get('email')
    pwd = request.form.get('password')
    valid = AUTH.valid_login(em, pwd)
    if not valid:
        abort(401)
    s_id = AUTH.create_session(em)
    res = jsonify({'email': em, 'message': 'logged in'})
    res.set_cookie('session_id', s_id)
    return res


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """Logs out a user"""
    s_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(s_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route("/profile", methods=['GET'])
def profile():
    """Gets the user profile"""
    s_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(s_id)
    if not user:
        abort(403)
    return jsonify({'email': user.email}), 200


@app.route("/reset_password", methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    em = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(em)
        return jsonify({'email': em, 'reset_token': token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=['PUT'], strict_slashes=False)
def update_password():
    """Updates a user password using the reset token"""
    em = request.form.get('email')
    pwd = request.form.get('new_password')
    r_token = request.form.get('reset_token')
    if not (em or pwd or r_token):
        abort(400)
    try:
        AUTH.update_password(r_token, pwd)
    except ValueError:
        abort(403)
    return jsonify({"email": em, "message": 'Password updated'})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
