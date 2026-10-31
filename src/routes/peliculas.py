from flask import Blueprint, request, jsonify

import src.validators.peliculas as peliculas_validator
import src.services.peliculas as peliculas_service
import src.utils.errores as errores


peliculas_bp = Blueprint("admin_peliculas", __name__)


@peliculas_bp.route("/admin/peliculas", methods=["GET"])
def consultar_peliculas():

    titulo = request.args.get("titulo")
    genero = request.args.get("genero")

    es_valido, titulo, genero, descripcion_error = peliculas_validator.validar_filtros_peliculas(
        titulo, genero
    )

    if not es_valido:
        return errores.devolver_error(descripcion_error, 400)

    try:
        peliculas = peliculas_service.listar_peliculas(titulo, genero)

        return jsonify(peliculas), 200

    except Exception:
        return errores.devolver_error("No se pudieron consultar las peliculas", 500)