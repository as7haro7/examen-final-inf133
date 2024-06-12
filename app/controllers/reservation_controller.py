# reservation_controller.py

from flask import Blueprint, jsonify, request
from app.models.reservation_model import Reservation
from app.utils.decorators import jwt_required, roles_required
from app.views.reservation_view import render_reservation_detail, render_reservation_list

# Crear un blueprint para el controlador de reservas
reservation_bp = Blueprint("reservation", __name__)

# Ruta para obtener la lista de reservas
@reservation_bp.route("/reservations", methods=["GET"])
@jwt_required
@roles_required(roles=["admin"])
def get_reservations():
    reservations = Reservation.get_all()
    return jsonify(render_reservation_list(reservations))

# Ruta para obtener una reserva específica por su ID
@reservation_bp.route("/reservations/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "customer"])
def get_reservation(id):
    reservation = Reservation.get_by_id(id)
    if reservation:
        return jsonify(render_reservation_detail(reservation))
    return jsonify({"error": "Reserva no encontrada"}), 404

# Ruta para crear una nueva reserva
@reservation_bp.route("/reservations", methods=["POST"])
@jwt_required
@roles_required(roles=["admin", "customer"])
def create_reservation():
    data = request.json
    user_id = data.get("user_id")
    restaurant_id = data.get("restaurant_id")
    reservation_date = data.get("reservation_date")
    num_guests = data.get("num_guests")
    special_requests = data.get("special_requests")
    status = data.get("status")

    # Validación simple de datos de entrada
    if not all([user_id, restaurant_id, reservation_date, num_guests, status]):
        return jsonify({"error": "Faltan datos requeridos"}), 400

    # Crear una nueva reserva y guardarla en la base de datos
    reservation = Reservation(user_id=user_id, restaurant_id=restaurant_id, reservation_date=reservation_date, num_guests=num_guests, special_requests=special_requests, status=status)
    reservation.save()

    return jsonify(render_reservation_detail(reservation)), 201

# Ruta para actualizar una reserva existente
@reservation_bp.route("/reservations/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin", "customer"])
def update_reservation(id):
    reservation = Reservation.get_by_id(id)

    if not reservation:
        return jsonify({"error": "Reserva no encontrada"}), 404

    data = request.json
    user_id = data.get("user_id")
    restaurant_id = data.get("restaurant_id")
    reservation_date = data.get("reservation_date")
    num_guests = data.get("num_guests")
    special_requests = data.get("special_requests")
    status = data.get("status")

    # Actualizar los datos de la reserva
    reservation.update(user_id=user_id, restaurant_id=restaurant_id, reservation_date=reservation_date, num_guests=num_guests, special_requests=special_requests, status=status)

    return jsonify(render_reservation_detail(reservation))

# Ruta para eliminar una reserva existente
@reservation_bp.route("/reservations/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin", "customer"])
def delete_reservation(id):
    reservation = Reservation.get_by_id(id)

    if not reservation:
        return jsonify({"error": "Reserva no encontrada"}), 404

    # Eliminar la reserva de la base de datos
    reservation.delete()

    # Respuesta vacía con código de estado 204 (sin contenido)
    return "", 204
