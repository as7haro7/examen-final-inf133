from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from app.models.user_model import User
import json

user_bp = Blueprint("user", __name__)

@user_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")
    roles = data.get("role")

    if not email or not password:
        return jsonify({"error": "Se requieren correo electrónico y contraseña"}), 400

    existing_user = User.find_by_email(email)
    if existing_user:
        return jsonify({"error": "El correo electrónico ya está en uso"}), 400

    # Aseguramos que roles sea una lista
    if isinstance(roles, str):
        roles = [roles]

    new_user = User(username=username, password=password, email=email, phone=phone, roles=roles)
    new_user.save()

    return jsonify({"message": "Usuario creado exitosamente"}), 201

@user_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = User.find_by_email(email)
    if user and user.check_password(password):
        # Decodificamos roles y nos aseguramos de que sean una lista
        roles = json.loads(user.roles)
        access_token = create_access_token(identity={"email": email, "roles": roles})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401
