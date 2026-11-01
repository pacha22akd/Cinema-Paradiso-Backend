from flask import Blueprint
from flask import jsonify
from flask import request
from services import servicios_adicionales_service
from src.utils.errores import devolver_error

servicios_adicionales_bp = Blueprint("servicios_adicionales", __name__)

@servicios_adicionales_bp.route("/servicios", methods=["GET"])
def get_servicios_adicionales():

    categoria = request.args.get("categoria")

    try:
        servicios = servicios_adicionales_service.listar_servicios_adicionales(categoria)
        return jsonify(servicios), 200

    except Exception as e:
        return devolver_error(str(e), 500)
