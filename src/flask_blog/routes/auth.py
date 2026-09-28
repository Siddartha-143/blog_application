"""Authentication routes: user registration and login."""

from uuid import uuid4

from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

from flask_blog.repositories import create_user, find_user_by_email

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/user")
def add_user():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return {"message": "Name, email and password are required"}, 400

    if find_user_by_email(email):
        return {"message": "Please enter a different mail ID"}, 400

    create_user(
        name=name,
        email=email,
        hashed_password=generate_password_hash(password),
        user_id=str(uuid4()),
    )
    return {"message": "User is added successfully"}, 200


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"message": "Email and password are required"}, 400

    user = find_user_by_email(email)
    if user is None:
        return {"message": "Signup required"}, 401

    if not check_password_hash(user["hashed_password"], password):
        return {"message": "Invalid password"}, 401

    token = create_access_token(identity=email)
    return {"message": "Logged in successfully", "token": token}, 200
