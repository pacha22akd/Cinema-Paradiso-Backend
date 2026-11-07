from flask import Blueprint
from flask import jsonify
from flask import request
from services import servicios
from src.utils.errores import devolver_error


servicios_bp = Blueprint("servicios", __name__)

@servicios_bp.route("/servicios", methods=["GET"])

def get_servicios_adicionales():

    categoria = request.args.get("categoria")

    try:
        servicios = servicios.listar_servicios_adicionales(categoria)
        return jsonify(servicios), 200

    except Exception as e:
        return devolver_error(str(e), 500)
