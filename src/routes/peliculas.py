from flask import Blueprint, request, jsonify

import src.validators.peliculas as peliculas_validator
import src.services.peliculas as peliculas_service
import src.utils.errores as errores


peliculas_bp = Blueprint("admin_peliculas", __name__)


@peliculas_bp.route("/admin/peliculas/externas", methods=["GET"])
def consultar_pelicula_externa():

    titulo = request.args.get("titulo")
    anio = request.args.get("anio")

    es_valido, titulo, anio, descripcion_error = peliculas_validator.validar_busqueda_externa(
        titulo, anio
    )

    if not es_valido:
        return errores.devolver_error(descripcion_error, 400)

    try:
        pelicula = peliculas_service.buscar_pelicula_externa(titulo, anio)

        if pelicula is None:
            return errores.devolver_error("No se encontro la pelicula en OMDb", 404)

        return jsonify(pelicula), 200

    except Exception:
        return errores.devolver_error("No se pudo consultar OMDb", 500)