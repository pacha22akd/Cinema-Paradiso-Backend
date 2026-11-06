from flask import Blueprint, jsonify
from services import estadisticas
from src.utils.errores import devolver_error
from src.utils.auth import requiere_rol

estadisticas_bp = Blueprint("estadisticas", __name__)

@estadisticas_bp.route("/admin/estadisticas/cancelaciones", methods=["GET"])
@requiere_rol("admin")
def get_cancelaciones():

    try:
        resultado = estadisticas.consultar_cancelaciones()
        return jsonify(resultado), 200

    except Exception as e:
        return devolver_error(str(e), 500)
