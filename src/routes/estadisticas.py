from flask import Blueprint, request, jsonify
from src.repositories.estadisticas import consultar_kpis_resumen
from src.utils.errores import devolver_error
import src.validators.estadisticas as estadisticas_validator
import src.services.estadisticas as estadisticas_service
import src.utils.errores as errores
from src.utils.auth import requiere_rol
from src.services.estadisticas import (
    listar_ocupacion_funciones,
    listar_ocupacion_peliculas,
    listar_franjas_horarias
)

estadisticas_bp = Blueprint('estadisticas', __name__)

@estadisticas_bp.route('/admin/estadisticas/ocupacion/funciones', methods=['GET'])
@requiere_rol("administrador")
def obtener_ocupacion_por_funciones():
    try:
        datos = listar_ocupacion_funciones()

        if datos is None:
            return devolver_error("Error al calcular las estadísticas de ocupación por funciones", 500)

        return jsonify(datos), 200
    except Exception as e:
        return devolver_error(f"Error inesperado al obtener estadísticas de funciones: {str(e)}", 500)

@estadisticas_bp.route('/admin/estadisticas/ocupacion/peliculas', methods=['GET'])
@requiere_rol("administrador")
def obtener_ocupacion_por_peliculas():
    try:
        datos = listar_ocupacion_peliculas()

        if datos is None:
            return devolver_error("Error al calcular las estadísticas de ocupación por película", 500)

        return jsonify(datos), 200
    except Exception as e:
        return devolver_error(f"Error inesperado al obtener estadísticas por película: {str(e)}", 500)

@estadisticas_bp.route('/admin/estadisticas/franjas_horarias', methods=['GET'])
@requiere_rol("administrador")
def obtener_franjas_horarias():
    try:
        datos = listar_franjas_horarias()

        if datos is None:
            return devolver_error("Error al calcular las estadísticas por franja horaria", 500)

        return jsonify(datos), 200
    except Exception as e:
        return devolver_error(f"Error inesperado al obtener estadísticas por franja horaria: {str(e)}", 500)


@estadisticas_bp.route("/admin/estadisticas/ventas_genero", methods=["GET"])
@requiere_rol("administrador")
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


@estadisticas_bp.route("/admin/estadisticas/cancelaciones", methods=["GET"])
@requiere_rol("administrador")
def get_cancelaciones():

    try:
        resultado = estadisticas_service.consultar_cancelaciones()
        return jsonify(resultado), 200

    except Exception as e:
        return devolver_error(str(e), 500)


@estadisticas_bp.route('/admin/estadisticas/kpis', methods=['GET'])
@requiere_rol("administrador")
def obtener_kpis():
    try:
        datos = consultar_kpis_resumen()
        if datos is None:
            return devolver_error("Error al calcular los KPIs", 500)
        return jsonify(datos), 200
    except Exception as e:
        return devolver_error(f"Error inesperado al obtener KPIs: {str(e)}", 500)
