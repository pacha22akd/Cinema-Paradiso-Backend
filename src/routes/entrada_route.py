from flask import Blueprint, request, jsonify
from services import entrada_services
from src.utils.errores import devolver_error

entradas_bp = Blueprint("entradas", __name__)

@entradas_bp.route("/admin/entradas/validar_qr", methods=["POST"])
def post_validar_qr():

    datos = request.get_json()

    try:
        resultado = entrada_services.validar_qr(
            datos.get("qr_codigo"),
            datos.get("funcion_id"),
        )
        return jsonify(resultado), 200

    except ValueError as e:
        return devolver_error(str(e), 400)

    except Exception as e:
        return devolver_error(str(e), 500)
