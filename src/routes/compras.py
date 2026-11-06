from flask import Blueprint, request
from src.utils.auth import requiere_auth
from src.utils.errores import devolver_error
import src.services.compras as compras_service

compras_bp = Blueprint("compras", __name__)

@compras_bp.route("/compras/<int:id>/servicios", methods=["POST"])
@requiere_auth
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
@requiere_auth
def post_pagar_compra(id):

    try:
        return compras_services.pagar_compra(id)

    except Exception as e:
        return devolver_error(str(e), 500)
