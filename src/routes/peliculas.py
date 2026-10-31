from flask import Blueprint, request, jsonify
from src.services.peliculas import buscar_pelicula_por_id, listar_peliculas
from src.services.funciones import listar_funciones_por_pelicula
from src.utils.errores import devolver_error

peliculas_bp = Blueprint('peliculas', __name__)

@peliculas_bp.route('/peliculas', methods=['GET'])
def get_peliculas():
    try:                                                    
        genero = request.args.get('genero')
        titulo = request.args.get('titulo')

        peliculas = listar_peliculas(genero, titulo)

        if peliculas is None:
            return devolver_error("Error al obtener la cartelera de películas de la base de datos", 500)

        return jsonify(peliculas), 200

    except Exception as e:                                  
        return devolver_error(f"Error inesperado al obtener la cartelera: {str(e)}", 500)  

@peliculas_bp.route('/admin/peliculas/<int:pelicula_id>', methods=['GET'])
def obtener_pelicula(pelicula_id):
    try:
        pelicula = buscar_pelicula_por_id(pelicula_id)

        if pelicula is None:
            return devolver_error("La película solicitada no existe", 404)

        return jsonify(pelicula), 200

    except Exception as e:
        return devolver_error(f"Error al obtener la película: {str(e)}", 500)

@peliculas_bp.route('/peliculas/<int:pelicula_id>/funciones', methods=['GET'])
def get_funciones_pelicula(pelicula_id):
    try:                                                    
        pelicula = buscar_pelicula_por_id(pelicula_id)
        if pelicula is None:
            return devolver_error("La película solicitada no existe", 404)

        funciones = listar_funciones_por_pelicula(pelicula_id)
        if funciones is None:
            return devolver_error("Error al obtener las funciones de la película", 500)

        return jsonify(funciones), 200

    except Exception as e:                                  
        return devolver_error(f"Error inesperado al obtener las funciones: {str(e)}", 500) 