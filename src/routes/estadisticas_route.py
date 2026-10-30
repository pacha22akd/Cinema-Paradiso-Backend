from flask import Blueprint, jsonify
from services import estadisticas_services

estadisticas_bp = Blueprint("estadisticas", __name__)

@estadisticas_bp.route("/admin/estadisticas/cancelaciones", methods=["GET"])
def get_cancelaciones():

    try:
        resultado = estadisticas_service.consultar_cancelaciones()
        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"message": "Error interno", "error": str(e)}), 500