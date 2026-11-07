from flask import Blueprint
from services import entradas
from src.utils.errores import devolver_error
from src.utils.auth import requiere_auth

entradas_bp = Blueprint("entradas", __name__)


@entradas_bp.route("/entradas/<int:id>", methods=["GET"])
@requiere_auth
def get_entrada(id):

    try:
        return entradas.consultar_entrada(id)

    except Exception as e:
        return devolver_error(str(e), 500)
