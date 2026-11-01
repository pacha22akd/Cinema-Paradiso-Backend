from sqlalchemy import text
from src.utils.config import db


def obtener_ventas_genero(fecha_desde=None, fecha_hasta=None):

    query = """SELECT
                   p.genero AS genero,
                   COUNT(e.id) AS cantidad_entradas,
                   ROUND(SUM(e.precio), 2) AS total_recaudado
               FROM entradas e
               INNER JOIN compras c ON e.compra_id = c.id
               INNER JOIN funciones f ON e.funcion_id = f.id
               INNER JOIN peliculas p ON f.pelicula_id = p.id
               WHERE c.estado IN ('pagada', 'usada')
               AND e.estado IN ('valida', 'usada')"""

    parametros = {}

    if fecha_desde is not None:
        query += " AND DATE(c.fecha_compra) >= :fecha_desde"
        parametros["fecha_desde"] = fecha_desde

    if fecha_hasta is not None:
        query += " AND DATE(c.fecha_compra) <= :fecha_hasta"
        parametros["fecha_hasta"] = fecha_hasta

    query += " GROUP BY p.genero"
    query += " ORDER BY total_recaudado DESC"

    conn = db.connect()

    try:
        resultado = conn.execute(text(query), parametros)

        filas = resultado.fetchall()

        estadisticas = []

        for fila in filas:
            estadistica = dict(fila._mapping)
            estadistica["total_recaudado"] = float(estadistica["total_recaudado"])
            estadisticas.append(estadistica)

        return estadisticas

    finally:
        conn.close()