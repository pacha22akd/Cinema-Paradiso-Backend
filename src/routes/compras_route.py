from flask import Blueprint, request
from services import compras_services
from src.utils.errores import devolver_error

compras_bp = Blueprint("compras", __name__)


@compras_bp.route("/compras/<int:id>/servicios", methods=["POST"])
def post_servicio_a_compra(id):

    try:
        datos = request.get_json()

        return compras_services.agregar_servicio_a_compra(
            id,
            datos.get("servicio_id"),
            datos.get("cantidad"),
        )

    except ValueError as e:
        return devolver_error(str(e), 400)

    except Exception as e:
        return devolver_error(str(e), 500)


@compras_bp.route("/compras/<int:id>/pagar", methods=["POST"])
def post_pagar_compra(id):

    try:
        return compras_services.pagar_compra(id)

    except Exception as e:
        return devolver_error(str(e), 500)
