from flask import Blueprint, request, jsonify
from services import entradas_services

entradas_bp = Blueprint("entradas", __name__)

@entradas_bp.route("/admin/entradas/validar_qr", methods=["POST"])
def post_validar_qr():

    datos = request.get_json()

    try:
        resultado = entradas_service.validar_qr(
            datos.get("qr_codigo"),
            datos.get("funcion_id"),
        )
        return jsonify(resultado), 200

    except ValueError as e:
        return jsonify({"message": str(e)}), 400

    except Exception as e:
        return jsonify({"message": "Error interno", "error": str(e)}), 500
