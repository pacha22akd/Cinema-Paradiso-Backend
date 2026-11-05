
from flask import Blueprint, jsonify, request
from src.validators.funciones import validar_datos_funcion, validar_modificacion_funcion
from src.utils.errores import devolver_error
from src.utils.auth import requiere_rol
from src.services.funciones import (
    obtener_disponibilidad_butacas,
    listar_funciones,
    buscar_funcion_por_id,
    crear_nueva_funcion,
    modificar_funcion
)

funciones_bp = Blueprint('funciones', __name__)


# Obtener disponibilidad de butacas
@funciones_bp.route('/funciones/<int:funcion_id>/butacas', methods=['GET'])
def get_butacas_funcion(funcion_id):
    try:
        butacas = obtener_disponibilidad_butacas(funcion_id)

        if butacas is None:
            return devolver_error(
                "La función solicitada no existe o no se pudieron obtener las butacas", 404
            )

        return jsonify(butacas), 200

    except Exception as e:
        return devolver_error(f"Error al obtener las butacas de la función: {str(e)}", 500)


# Listar funciones (admin)
@funciones_bp.route('/admin/funciones', methods=['GET'])
@requiere_rol("administrador")
def obtener_funciones():
    funciones = listar_funciones()

    if funciones is None:
        return devolver_error("Error al obtener funciones", 500)

    return jsonify(funciones), 200


# Obtener una función por ID (admin)
@funciones_bp.route('/admin/funciones/<int:id_funcion>', methods=['GET'])
@requiere_rol("administrador")
def obtener_funcion(id_funcion):
    funcion = buscar_funcion_por_id(id_funcion)

    if funcion is None:
        return devolver_error(f"No se encontró la función con ID {id_funcion}", 404)

    return jsonify(funcion), 200


# Crear una función (admin)
@funciones_bp.route('/admin/funciones', methods=['POST'])
@requiere_rol("administrador")
def crear_funcion():
    datos_funcion = request.get_json()

    valido, error = validar_datos_funcion(datos_funcion)
    if not valido:
        return devolver_error(error, 400)

    nueva_funcion = crear_nueva_funcion(datos_funcion)

    if not nueva_funcion:
        return devolver_error("Error al crear función", 500)

    return jsonify({"mensaje": "Función creada correctamente"}), 201


# Modificar una función (admin)
@funciones_bp.route('/admin/funciones/<int:id_funcion>', methods=['PATCH'])
@requiere_rol("administrador")
def actualizar_funcion_por_id(id_funcion):
    datos_actualizados = request.get_json()

    valido, datos_actualizados, error = validar_modificacion_funcion(datos_actualizados)

    if not valido:
        return devolver_error(error, 400)

    funcion_actualizada = modificar_funcion(id_funcion, datos_actualizados)

    if funcion_actualizada is None:
        return devolver_error(f"No se encontró la función con ID {id_funcion}", 404)

    return jsonify({"mensaje": "Función actualizada correctamente"}), 200
