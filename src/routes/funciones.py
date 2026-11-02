from flask import Blueprint, jsonify
from src.services.funciones import listar_funciones, buscar_funcion_por_id, crear_nueva_funcion, actualizar_funcion, modificar_funcion
from src.validators.funciones import validar_datos_funcion, validar_modificacion_funcion
from src.utils.errores import devolver_error
from flask import request
funciones_bp = Blueprint('funciones_bp', __name__)

@funciones_bp.route('/admin/funciones', methods=['GET'])
def obtener_funciones():
    funciones = listar_funciones()
    
    if funciones is None:
        return devolver_error("Error al obtener funciones", 500)
    
    return jsonify(funciones), 200

@funciones_bp.route('/admin/funciones/<int:id_funcion>', methods=['GET'])
def obtener_funcion(id_funcion):
    funcion = buscar_funcion_por_id(id_funcion)
    
    if funcion is None:
        return devolver_error(f"No se encontró la función con ID {id_funcion}", 404)
    
    return jsonify(funcion), 200

@funciones_bp.route('/admin/funciones', methods=['POST'])
def crear_funcion():
    datos_funcion = request.get_json()
    
    valido, error = validar_datos_funcion(datos_funcion)
    if not valido:
        return devolver_error(error, 400)
    nueva_funcion = crear_nueva_funcion(datos_funcion)
    
    if not nueva_funcion:
        return devolver_error("Error al crear función", 500)
    
    return jsonify({"mensaje": "Función creada correctamente"}), 201

@funciones_bp.route('/admin/funciones/<int:id_funcion>', methods=['PATCH'])
def actualizar_funcion_por_id(id_funcion):
    datos_actualizados = request.get_json()
    
    valido, datos_actualizados, error = validar_modificacion_funcion(datos_actualizados)
    
    if not valido:
        return devolver_error(error, 400)
    
    funcion_actualizada = modificar_funcion(id_funcion, datos_actualizados)
    
    if funcion_actualizada is None:
        return devolver_error(f"No se encontró la función con ID {id_funcion}", 404)
    
    return jsonify({"mensaje": "Función actualizada correctamente"}), 200