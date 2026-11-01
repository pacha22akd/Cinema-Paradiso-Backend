from flask import Blueprint, request, jsonify

import src.validators.peliculas as peliculas_validator
import src.services.peliculas as peliculas_service
import src.utils.errores as errores


peliculas_bp = Blueprint("admin_peliculas", __name__)


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