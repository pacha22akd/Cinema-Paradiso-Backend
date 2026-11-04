import src.repositories.estadisticas as estadisticas_repository
from src.repositories.estadisticas import (
    obtener_ocupacion_funciones,
    obtener_ocupacion_peliculas,
    obtener_ocupacion_franjas_horarias
)

def listar_ocupacion_funciones():
    return obtener_ocupacion_funciones()

def listar_ocupacion_peliculas():
    return obtener_ocupacion_peliculas()

def listar_franjas_horarias():
    return obtener_ocupacion_franjas_horarias()



def consultar_ventas_genero(fecha_desde=None, fecha_hasta=None):

    estadisticas = estadisticas_repository.obtener_ventas_genero(
        fecha_desde, fecha_hasta
    )

    return estadisticas
