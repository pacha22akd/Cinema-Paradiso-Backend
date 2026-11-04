from flask import Blueprint, request, jsonify

import src.validators.peliculas as peliculas_validator
import src.services.peliculas as peliculas_service
import src.utils.errores as errores


peliculas_bp = Blueprint("admin_peliculas", __name__)


@peliculas_bp.route("/admin/peliculas", methods=["GET"])
def consultar_peliculas():

    titulo = request.args.get("titulo")
    genero = request.args.get("genero")

    es_valido, titulo, genero, descripcion_error = peliculas_validator.validar_filtros_peliculas(titulo, genero, request.args)
    if not es_valido:
            return errores.devolver_error(descripcion_error, 400)
    
    try:
        peliculas = peliculas_service.listar_peliculas(titulo, genero)
    
        return jsonify(peliculas), 200
    except Exception:
            return errores.devolver_error("No se pudieron consultar las peliculas", 500)


    
@peliculas_bp.route("/admin/peliculas/externas", methods=["GET"])
def consultar_pelicula_externa():

    titulo = request.args.get("titulo")
    anio = request.args.get("anio")

    es_valido, titulo, anio, descripcion_error = peliculas_validator.validar_busqueda_externa(titulo, anio, request.args)
    if not es_valido:
            return errores.devolver_error(descripcion_error, 400)
    
    try:
        pelicula = peliculas_service.buscar_pelicula_externa(titulo, anio)

        if pelicula is None:
            return errores.devolver_error("No se encontro la pelicula en OMDb", 404)

        return jsonify(pelicula), 200

    except Exception:
        return errores.devolver_error("No se pudo consultar OMDb", 500)

          
@peliculas_bp.route("/admin/peliculas/<int:id_pelicula>", methods=["PATCH"])
def modificar_pelicula(id_pelicula):

    id_valido, descripcion_error = peliculas_validator.validar_id_pelicula(id_pelicula)

    if not id_valido:
        return errores.devolver_error(descripcion_error, 400)

    datos = request.get_json(silent=True)

    es_valido, pelicula, descripcion_error = peliculas_validator.validar_modificacion_pelicula(datos)

    if not es_valido:
        return errores.devolver_error(descripcion_error, 400)

    try:
        
        pelicula_actualizada = peliculas_service.modificar_pelicula(
            id_pelicula, pelicula
        )

        if pelicula_actualizada is None:
            return errores.devolver_error("La pelicula no existe", 404)

        return jsonify(pelicula_actualizada), 200

    except Exception:
        return errores.devolver_error("No se pudo modificar la pelicula", 500)
