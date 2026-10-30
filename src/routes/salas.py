from flask import Blueprint, jsonify
from src.repositories.salas import obtener_salas
from src.utils.errores import devolver_error

salas_bp = Blueprint('salas', __name__)

@salas_bp.route('/admin/salas', methods=['GET'])
def listar_salas():
    try:
        salas = obtener_salas()

        if salas is None:
            return devolver_error("Error al obtener el listado de salas", 500)

        return jsonify(salas), 200

    except Exception as e:
        return devolver_error(f"Error inesperado al obtener salas: {str(e)}", 500)