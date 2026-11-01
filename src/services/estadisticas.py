import src.repositories.estadisticas as estadisticas_repository


def consultar_ventas_genero(fecha_desde=None, fecha_hasta=None):

    estadisticas = estadisticas_repository.obtener_ventas_genero(
        fecha_desde, fecha_hasta
    )

    return estadisticas