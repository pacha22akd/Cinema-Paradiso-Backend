from flask import Blueprint, jsonify
from services import estadisticas_services
from src.utils.errores import devolver_error

estadisticas_bp = Blueprint("estadisticas", __name__)

@estadisticas_bp.route("/admin/estadisticas/cancelaciones", methods=["GET"])
def get_cancelaciones():

    try:
        resultado = estadisticas_service.consultar_cancelaciones()
        return jsonify(resultado), 200

    except Exception as e:
        return devolver_error(str(e), 500)