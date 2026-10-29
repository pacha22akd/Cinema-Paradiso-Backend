from flask import Blueprint, jsonify
from src.repositories.salas import obtener_salas

salas_bp = Blueprint('salas', __name__)

@salas_bp.route('/admin/salas', methods=['GET'])
def listar_salas():
    salas = obtener_salas()

    if salas is None:
        return jsonify({"error": "Error al obtener el listado de salas"}), 500

    return jsonify(salas), 200