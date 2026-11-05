from flask import Blueprint, request, jsonify
from src.services.peliculas import buscar_pelicula_por_id, listar_peliculas_cartelera
from src.services.funciones import listar_funciones_por_pelicula
from src.utils.errores import devolver_error
import src.validators.peliculas as peliculas_validator
import src.services.peliculas as peliculas_service
import src.utils.errores as errores 
from src.utils.auth import requiere_rol

peliculas_bp = Blueprint('peliculas', __name__)

@peliculas_bp.route('/peliculas', methods=['GET'])
def get_peliculas():
    try:                                                    
        genero = request.args.get('genero')
        titulo = request.args.get('titulo')

        peliculas = listar_peliculas_cartelera(genero, titulo)

        if peliculas is None:
            return devolver_error("Error al obtener la cartelera de películas de la base de datos", 500)

        return jsonify(peliculas), 200

    except Exception as e:                                  
        return devolver_error(f"Error inesperado al obtener la cartelera: {str(e)}", 500)  

@peliculas_bp.route('/admin/peliculas/<int:pelicula_id>', methods=['GET'])
@requiere_rol("administrador")
def obtener_pelicula(pelicula_id):
    try:
        pelicula = buscar_pelicula_por_id(pelicula_id)

        if pelicula is None:
            return devolver_error("La película solicitada no existe", 404)

        return jsonify(pelicula), 200

    except Exception as e:
        return devolver_error(f"Error al obtener la película: {str(e)}", 500)

@peliculas_bp.route('/peliculas/<int:pelicula_id>/funciones', methods=['GET'])
def get_funciones_pelicula(pelicula_id):
    try:                                                    
        pelicula = buscar_pelicula_por_id(pelicula_id)
        if pelicula is None:
            return devolver_error("La película solicitada no existe", 404)

        funciones = listar_funciones_por_pelicula(pelicula_id)
        if funciones is None:
            return devolver_error("Error al obtener las funciones de la película", 500)

        return jsonify(funciones), 200

    except Exception as e:                                  
        return devolver_error(f"Error inesperado al obtener las funciones: {str(e)}", 500) 


@peliculas_bp.route("/admin/peliculas", methods=["GET"])
@requiere_rol("administrador")
def consultar_peliculas():

    titulo = request.args.get("titulo")
    genero = request.args.get("genero")

    es_valido, titulo, genero, descripcion_error = peliculas_validator.validar_filtros_peliculas(titulo, genero, request.args)
    if not es_valido:
            return errores.devolver_error(descripcion_error, 400)
    
    try:
        peliculas = peliculas_service.listar_peliculas(titulo, genero)
    
        return jsonify(peliculas), 200
    except Exception:
            return errores.devolver_error("No se pudieron consultar las peliculas", 500)


    
@peliculas_bp.route("/admin/peliculas/externas", methods=["GET"])
@requiere_rol("administrador")
def consultar_pelicula_externa():

    titulo = request.args.get("titulo")
    anio = request.args.get("anio")

    es_valido, titulo, anio, descripcion_error = peliculas_validator.validar_busqueda_externa(titulo, anio, request.args)
    if not es_valido:
            return errores.devolver_error(descripcion_error, 400)
    
    try:
        pelicula = peliculas_service.buscar_pelicula_externa(titulo, anio)

        if pelicula is None:
            return errores.devolver_error("No se encontro la pelicula en OMDb", 404)

        return jsonify(pelicula), 200

    except Exception:
        return errores.devolver_error("No se pudo consultar OMDb", 500)

          
@peliculas_bp.route("/admin/peliculas/<int:id_pelicula>", methods=["PATCH"])
@requiere_rol("administrador")
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
    
    
@peliculas_bp.route("/admin/peliculas", methods=["POST"])
@requiere_rol("administrador")
def registrar_pelicula():

    datos = request.get_json(silent=True)

    es_valido, pelicula, descripcion_error = peliculas_validator.validar_alta_pelicula(datos)

    if not es_valido:
        return errores.devolver_error(descripcion_error, 400)

    try:
        pelicula_creada = peliculas_service.crear_pelicula(pelicula)

        return jsonify(pelicula_creada), 201

    except Exception:
        return errores.devolver_error("No se pudo registrar la pelicula", 500)


    
@peliculas_bp.route("/admin/peliculas/<int:id_pelicula>", methods=["DELETE"])
@requiere_rol("administrador")
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
