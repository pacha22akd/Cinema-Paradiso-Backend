from src.repositories.funciones import obtener_funciones, obtener_funcion_por_id, crear_funcion

def listar_funciones():
    return obtener_funciones()


def buscar_funcion_por_id(id_funcion):
    return obtener_funcion_por_id(id_funcion)

def crear_nueva_funcion(datos_funcion):
    return crear_funcion(datos_funcion)