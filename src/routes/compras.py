from flask import Blueprint, jsonify
from src.services import compras
from src.utils.errores import devolver_error

compras_bp = Blueprint('compras', __name__)

@compras_bp.route("/compras/<int:id>", methods=["GET"])
def get_compra(id):
    try:
        resultado = compras.obtener_compra(id)

        if "error" in resultado:
            return devolver_error(resultado["error"], resultado["status"])

        return jsonify(resultado), 200

    except Exception as e:
        return devolver_error(str(e), 500)