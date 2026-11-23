from src.repositories.estadisticas import (
    obtener_ocupacion_funciones,
    obtener_ocupacion_peliculas,
    obtener_ocupacion_franjas_horarias,
    obtener_ventas_genero,
    obtener_cancelaciones
)
from src.validators.estadisticas import validar_fechas_ventas

def listar_ocupacion_funciones():
    return obtener_ocupacion_funciones()

def listar_ocupacion_peliculas():
    return obtener_ocupacion_peliculas()

def listar_franjas_horarias():
    return obtener_ocupacion_franjas_horarias()


def consultar_ventas_genero(parametros):
    fecha_desde = parametros.get("fecha_desde", [None])[0]
    fecha_hasta = parametros.get("fecha_hasta", [None])[0]

    es_valido, fecha_desde, fecha_hasta, descripcion_error = validar_fechas_ventas(fecha_desde, fecha_hasta, parametros)

    if not es_valido:
        raise ValueError(descripcion_error)

    estadisticas = obtener_ventas_genero(fecha_desde, fecha_hasta)

    return estadisticas


def consultar_cancelaciones():

    motivos = obtener_cancelaciones()

    total = 0
    for fila in motivos:
        total += fila["cantidad"]

    return {"total_canceladas": total, "motivos": motivos}
