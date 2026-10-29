from flask import Blueprint, jsonify
from src.repositories.estadisticas import (
obtener_ocupacion_funciones, 
obtener_ocupacion_peliculas,
obtener_ocupacion_franjas_horarias
)

estadisticas_bp = Blueprint('estadisticas', __name__)

@estadisticas_bp.route('/admin/estadisticas/ocupacion/funciones', methods=['GET'])
def obtener_ocupacion_por_funciones():
    datos = obtener_ocupacion_funciones()

    if datos is None:
        return jsonify({"error": "Error al calcular las estadísticas de ocupación"}), 500

    return jsonify(datos), 200

@estadisticas_bp.route('/admin/estadisticas/ocupacion/peliculas', methods=['GET'])
def obtener_ocupacion_por_peliculas():
    datos = obtener_ocupacion_peliculas()

    if datos is None:
        return jsonify({"error": "Error al calcular las estadísticas de ocupación por película"}), 500

    return jsonify(datos), 200

@estadisticas_bp.route('/admin/estadisticas/franjas_horarias', methods=['GET'])
def obtener_franjas_horarias():
    datos = obtener_ocupacion_franjas_horarias()

    if datos is None:
        return jsonify({"error": "Error al calcular las estadísticas por franja horaria"}), 500

    return jsonify(datos), 200