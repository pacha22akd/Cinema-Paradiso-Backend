from flask import Blueprint, request, jsonify

import src.validators.peliculas as peliculas_validator
import src.services.peliculas as peliculas_service
import src.utils.errores as errores


peliculas_bp = Blueprint("admin_peliculas", __name__)


@peliculas_bp.route("/admin/peliculas", methods=["POST"])
def registrar_pelicula():

    datos = request.get_json(silent=True)

    es_valido, pelicula, descripcion_error = peliculas_validator.validar_alta_pelicula(datos)

    if not es_valido:
        return errores.devolver_error(descripcion_error, 400)

    try:
        pelicula_creada = peliculas_service.crear_pelicula(pelicula)

        return jsonify(pelicula_creada), 201

    except Exception:
        return errores.devolver_error("No se pudo registrar la pelicula", 500)