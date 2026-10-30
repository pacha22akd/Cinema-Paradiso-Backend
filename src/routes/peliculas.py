from flask import Blueprint, jsonify
from src.repositories.peliculas import obtener_pelicula_por_id
from src.utils.errores import devolver_error

peliculas_bp = Blueprint('peliculas', __name__)

@peliculas_bp.route('/admin/peliculas/<int:id_pelicula>', methods=['GET'])
def obtener_pelicula(id_pelicula):
    try:
        pelicula = obtener_pelicula_por_id(id_pelicula)

        if pelicula is None:
            return devolver_error("La película solicitada no existe", 404)

        return jsonify(pelicula), 200

    except Exception as e:
        return devolver_error(f"Error al obtener la película: {str(e)}", 500)