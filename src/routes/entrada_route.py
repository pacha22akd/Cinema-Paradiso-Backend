from flask import Blueprint
from services import entradas_service
from src.utils.errores import devolver_error

entradas_bp = Blueprint("entradas", __name__)


@entradas_bp.route("/entradas/<int:id>", methods=["GET"])
def get_entrada(id):

    try:
        return entradas_service.consultar_entrada(id)

    except Exception as e:
        return devolver_error(str(e), 500)
