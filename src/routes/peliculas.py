from flask import Blueprint, jsonify
from src.repositories.peliculas import obtener_pelicula_por_id

peliculas_bp = Blueprint('peliculas', __name__)

@peliculas_bp.route('/admin/peliculas/<int:id_pelicula>', methods=['GET'])
def obtener_pelicula(id_pelicula):
    pelicula = obtener_pelicula_por_id(id_pelicula)

    if not pelicula:
        return jsonify({"error": "Película no encontrada"}), 404

    return jsonify(pelicula), 200