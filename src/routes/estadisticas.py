from flask import Blueprint, request, jsonify

import src.validators.estadisticas as estadisticas_validator
import src.services.estadisticas as estadisticas_service
import src.utils.errores as errores


estadisticas_bp = Blueprint("admin_estadisticas", __name__)


@estadisticas_bp.route("/admin/estadisticas/ventas_genero", methods=["GET"])
def obtener_ventas_genero():

    fecha_desde = request.args.get("fecha_desde")
    fecha_hasta = request.args.get("fecha_hasta")

    es_valido, fecha_desde, fecha_hasta, descripcion_error = estadisticas_validator.validar_fechas_ventas(fecha_desde, fecha_hasta, request.args)

    if not es_valido:
        return errores.devolver_error(descripcion_error, 400)

    try:
        estadisticas = estadisticas_service.consultar_ventas_genero(
            fecha_desde, fecha_hasta
        )

        return jsonify(estadisticas), 200

    except Exception:
        return errores.devolver_error("No se pudieron obtener las ventas por genero", 500)