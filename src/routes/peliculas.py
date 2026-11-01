from flask import Blueprint, jsonify

import src.validators.peliculas as peliculas_validator
import src.services.peliculas as peliculas_service
import src.utils.errores as errores


peliculas_bp = Blueprint("admin_peliculas", __name__)


@peliculas_bp.route("/admin/peliculas/<int:id_pelicula>", methods=["DELETE"])
def eliminar_pelicula(id_pelicula):

    id_valido, descripcion_error = peliculas_validator.validar_id_pelicula(id_pelicula)

    if not id_valido:
        return errores.devolver_error(descripcion_error, 400)

    try:
        resultado = peliculas_service.borrar_pelicula(id_pelicula)

        if resultado == "no_existe":
            return errores.devolver_error("La pelicula no existe", 404)

        if resultado == "con_funciones_asociadas":
            return errores.devolver_error("La pelicula tiene funciones asociadas y no puede eliminarse", 409)

        return jsonify({"mensaje": "La pelicula fue eliminada correctamente"}), 200

    except Exception:
        return errores.devolver_error("No se pudo eliminar la pelicula", 500)