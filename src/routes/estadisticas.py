from flask import Blueprint, request, jsonify, current_app
from src.repositories.estadisticas import consultar_estadisticas_relevantes_resumen
from src.utils.errores import devolver_error
from src.utils.auth import requiere_rol
from src.services.estadisticas import (
    listar_ocupacion_funciones,
    listar_ocupacion_peliculas,
    listar_franjas_horarias,
    consultar_ventas_genero,
    consultar_cancelaciones
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
    parametros = request.args.to_dict(flat=False)
    try:
        estadisticas = consultar_ventas_genero(parametros)

        return jsonify(estadisticas), 200

    except ValueError as e:
        return devolver_error(str(e), 400)

    except Exception:
        return devolver_error("No se pudieron obtener las ventas por genero", 500)


@estadisticas_bp.route("/admin/estadisticas/cancelaciones", methods=["GET"])
@requiere_rol("administrador")
def get_cancelaciones():

    try:
        resultado = consultar_cancelaciones()
        return jsonify(resultado), 200

    except Exception as e:
        return devolver_error(str(e), 500)


@estadisticas_bp.route('/admin/estadisticas/estadisticas_relevantes', methods=['GET'])
@requiere_rol("administrador")
def obtener_estadisticas_relevantes():
    try:
        datos = consultar_estadisticas_relevantes_resumen()
        
        return jsonify(datos), 200
    except Exception:
        current_app.logger.exception("Error al obetener las estadisticas relevantes")
        return devolver_error("Error inesperado al obtener las estadísticas relevantes", 500)
