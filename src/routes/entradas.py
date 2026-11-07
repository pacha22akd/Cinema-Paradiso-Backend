from flask import Blueprint, request, jsonify, g
from src.services import entradas
from src.utils.errores import devolver_error
from src.utils.auth import requiere_auth, requiere_rol

entradas_bp = Blueprint("entradas", __name__)

@entradas_bp.route("/admin/entradas/validar_qr", methods=["POST"])
@requiere_rol("administrador")
def post_validar_qr():
    try:
        datos = request.get_json(silent=True)

        if not isinstance(datos, dict):
            return devolver_error("No se recibieron los datos de la entrada", 400)
        
        resultado = entradas.validar_qr(
            datos.get("qr_codigo"),
            datos.get("funcion_id"),
        )
        return jsonify(resultado), 200

    except ValueError as e:
        return devolver_error(str(e), 400)

@entradas_bp.route("/entradas/<int:id>", methods=["GET"])
@requiere_auth
def get_entrada(id):

    try:
        return entradas.consultar_entrada(id, g.usuario_id)

    except Exception:
        return devolver_error("No se pudo obtener la entrada", 500)
