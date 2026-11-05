
from src.repositories.funciones import (
    obtener_funciones_por_pelicula,
    obtener_funcion_por_id,
    obtener_butacas_por_funcion,
    obtener_funciones,
    crear_funcion,
    actualizar_funcion
)


def listar_funciones_por_pelicula(pelicula_id):
    return obtener_funciones_por_pelicula(pelicula_id)


def obtener_disponibilidad_butacas(funcion_id):
    funcion = obtener_funcion_por_id(funcion_id)

    if not funcion:
        return None

    return obtener_butacas_por_funcion(funcion_id, funcion["sala_id"])


def listar_funciones():
    return obtener_funciones()


def buscar_funcion_por_id(id_funcion):
    return obtener_funcion_por_id(id_funcion)


def crear_nueva_funcion(datos_funcion):
    return crear_funcion(datos_funcion)


def modificar_funcion(id_funcion, datos_actualizados):
    return actualizar_funcion(id_funcion, datos_actualizados)
