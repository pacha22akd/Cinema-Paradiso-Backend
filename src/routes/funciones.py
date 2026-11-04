from flask import Blueprint, jsonify
from src.services.funciones import obtener_disponibilidad_butacas
from src.utils.errores import devolver_error

funciones_bp = Blueprint('funciones', __name__)

@funciones_bp.route('/funciones/<int:funcion_id>/butacas', methods=['GET'])
def get_butacas_funcion(funcion_id):
    try:
        butacas = obtener_disponibilidad_butacas(funcion_id)

        if butacas is None:
            return devolver_error("La función solicitada no existe o no se pudieron obtener las butacas", 404)

        return jsonify(butacas), 200

    except Exception as e:
        return devolver_error(f"Error al obtener las butacas de la función: {str(e)}", 500)