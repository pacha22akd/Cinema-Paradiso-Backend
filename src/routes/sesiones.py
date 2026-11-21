from flask import Blueprint, request, current_app, jsonify

from src.services import sesiones
from src.utils.errores import devolver_error

sesiones_bp = Blueprint('sesiones', __name__)

@sesiones_bp.route('/sesiones', methods=['POST'])
def iniciar_sesion():
    datos = request.get_json(silent=True)

    if not datos:
        return devolver_error("Debe proporcionar un cuerpo JSON válido", 400)

    
    try:
        respuesta = sesiones.iniciar_sesion(
            datos.get("email"),
            datos.get("password"),   
        )

    except ValueError as e:
        return devolver_error(str(e),400)
    except PermissionError as e:
        return devolver_error(str(e),401)
    except Exception:
        current_app.logger.exception("error al iniciar sesion")
        return devolver_error("Ocurrio un error al iniciar sesion",500)

    return jsonify({
            "mensaje": "Sesión iniciada correctamente",
            "data": respuesta
        })