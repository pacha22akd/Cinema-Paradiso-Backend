from src.repositories.funciones import obtener_funciones, obtener_funcion_por_id

def listar_funciones():
    return obtener_funciones()


def buscar_funcion_por_id(id_funcion):
    return obtener_funcion_por_id(id_funcion)
