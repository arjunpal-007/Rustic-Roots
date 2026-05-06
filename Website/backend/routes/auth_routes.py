from flask import Blueprint, request, jsonify, session
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

auth_routes = Blueprint("auth_routes", __name__)

# SIGNUP
@auth_routes.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    user = User(
        name=data["name"],
        email=data["email"],
        password=data["password"]
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Signup successful"})


# LOGIN
@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if user and user.password == password:
        return jsonify({
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        })

    return jsonify({"error": "Invalid credentials"}), 401
