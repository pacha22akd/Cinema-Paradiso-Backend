
from flask import Blueprint, jsonify
from src.validators.compras import validar_id_compra

compras_bp = Blueprint("compras_bp", __name__)


@compras_bp.route("/compras/<int:id_compra>/cancelar", methods=["PATCH"])
def cancelar_compra_por_id(id_compra):

    valido, error = validar_id_compra(id_compra)

    if not valido:
        return jsonify({"error": error}), 400

    return jsonify({
        "error": "Falta integrar la autenticacion del usuario"
    }), 501
