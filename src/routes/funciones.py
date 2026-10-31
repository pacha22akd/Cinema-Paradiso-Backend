from flask import Blueprint, jsonify
from src.services.funciones import listar_funciones, buscar_funcion_por_id
from src.utils.errores import devolver_error
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