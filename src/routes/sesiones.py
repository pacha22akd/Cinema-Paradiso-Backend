from flask import Blueprint, request

from src.services import sesiones
from src.utils.errores import devolver_error

sesiones_bp = Blueprint('sesiones', __name__)

@sesiones_bp.route('/sesiones', methods=['POST'])
def iniciar_sesion():
    datos = request.get_json(silent=True)

    if not datos:
        return devolver_error("Debe proporcionar un cuerpo JSON válido", 400)

    respuesta, status = sesiones.iniciar_sesion(
        datos.get("email"),
        datos.get("contraseña"),   
    )

    if status == 200:
        respuesta = {
            "mensaje": "Sesión iniciada correctamente",
            **respuesta,
        }

    return respuesta, status