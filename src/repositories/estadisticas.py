from sqlalchemy import text
from src.utils.config import db

def obtener_ocupacion_funciones():
    """
    Ejecuta la consulta SQL para calcular el porcentaje de ocupación por función.
    """
    try:
        with db.connect() as conn:
            query = """
                SELECT 
                    f.id AS funcion_id,
                    p.titulo AS pelicula,
                    s.nombre AS sala,
                    f.fecha_hora_inicio,
                    s.capacidad,
                    COUNT(e.id) AS entradas_vendidas,
                    ROUND((COUNT(e.id) * 100.0 / s.capacidad), 2) AS porcentaje_ocupacion
                FROM funciones f
                JOIN peliculas p 
                    ON f.pelicula_id = p.id
                JOIN salas s 
                    ON f.sala_id = s.id
                LEFT JOIN entradas e 
                    ON e.funcion_id = f.id
                    AND e.estado <> 'cancelada'
                GROUP BY 
                    f.id, 
                    p.titulo, 
                    s.nombre, 
                    f.fecha_hora_inicio,
                    s.capacidad
                ORDER BY f.fecha_hora_inicio
            """

            result = conn.execute(text(query))
            rows = result.fetchall()

            ocupacion = [dict(zip(result.keys(), row)) for row in rows]

            # Paso la fecha a texto en formato estándar (ej: "2026-12-10T18:00:00") para el JSON
            for fila in ocupacion:
                fila["fecha_hora_inicio"] = fila["fecha_hora_inicio"].isoformat()

            return ocupacion
    except Exception as e:
        print(f"Error al consultar la ocupación de funciones: {e}")
        return None

def obtener_ocupacion_peliculas():
    """
    Ejecuta la consulta SQL para calcular el porcentaje de ocupación por película.
    Primero agrupa por función (subconsulta) para no inflar los totales.
    """
    try:
        with db.connect() as conn:
            query = """
                SELECT 
                    p.id AS pelicula_id,
                    p.titulo AS pelicula,
                    COUNT(o.funcion_id) AS total_funciones,
                    SUM(o.capacidad) AS capacidad_total,
                    SUM(o.vendidas) AS total_entradas_vendidas,
                    ROUND((SUM(o.vendidas) * 100.0 / SUM(o.capacidad)), 2) AS porcentaje_ocupacion
                FROM peliculas p
                JOIN (
                    SELECT 
                        f.id AS funcion_id,
                        f.pelicula_id,
                        s.capacidad,
                        COUNT(e.id) AS vendidas
                    FROM funciones f
                    JOIN salas s 
                        ON f.sala_id = s.id
                    LEFT JOIN entradas e 
                        ON e.funcion_id = f.id
                        AND e.estado <> 'cancelada'
                    GROUP BY 
                        f.id, 
                        f.pelicula_id, 
                        s.capacidad
                ) o 
                    ON o.pelicula_id = p.id
                GROUP BY 
                    p.id, 
                    p.titulo
            """

            result = conn.execute(text(query))
            rows = result.fetchall()

            # Mapeo a lista de diccionarios con zip
            ocupacion = [dict(zip(result.keys(), row)) for row in rows]

            return ocupacion
    except Exception as e:
        print(f"Error al consultar la ocupación por películas: {e}")
        return None


def obtener_ocupacion_franjas_horarias():
    """
    Ejecuta la consulta SQL para agrupar y contar las entradas vendidas por franja horaria.
    """
    try:
        with db.connect() as conn:
            query = """
                SELECT 
                    HOUR(f.fecha_hora_inicio) AS hora,
                    COUNT(e.id) AS entradas_vendidas
                FROM funciones f
                LEFT JOIN entradas e 
                    ON e.funcion_id = f.id
                    AND e.estado <> 'cancelada'
                GROUP BY 
                    HOUR(f.fecha_hora_inicio)
                ORDER BY 
                    hora ASC
            """

            result = conn.execute(text(query))
            rows = result.fetchall()

            # Mapeo tradicional
            franjas = [dict(zip(result.keys(), row)) for row in rows]

            return franjas
    except Exception as e:
        print(f"Error al consultar las franjas horarias: {e}")
        return None

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

        
def obtener_cancelaciones():

    query = """ SELECT motivo_cancelacion AS motivo, COUNT(*) AS cantidad FROM compras WHERE estado = 'cancelada' GROUP BY motivo_cancelacion """

    conn = db.connect()
    resultado = conn.execute(text(query))

    motivos = []
    for fila in resultado:
        motivo = {"motivo": fila.motivo, "cantidad": fila.cantidad}
        motivos.append(motivo)

    conn.close()

    return motivos

def consultar_kpis_resumen():
   
    try:
        with db.connect() as conn:
            # Entradas vendidas
            query_entradas = """
                SELECT COUNT(id) AS total 
                FROM entradas 
                WHERE estado IN ('valida', 'usada')
            """
            res_entradas = conn.execute(text(query_entradas))
            entradas = res_entradas.scalar() or 0

            # Ingresos totales
            query_ingresos = """
                SELECT SUM(total) AS total 
                FROM compras 
                WHERE estado IN ('pagada', 'usada')
            """
            res_ingresos = conn.execute(text(query_ingresos))
            ingresos = res_ingresos.scalar() or 0.0

            # Ocupación media
            query_ocupacion = """
                SELECT ROUND(AVG(porcentaje), 1) AS media
                FROM (
                    SELECT (COUNT(e.id) * 100.0 / s.capacidad) AS porcentaje
                    FROM funciones f
                    JOIN salas s ON f.sala_id = s.id
                    LEFT JOIN entradas e ON f.id = e.funcion_id AND e.estado <> 'cancelada'
                    GROUP BY f.id, s.capacidad
                ) AS subquery
            """
            res_ocupacion = conn.execute(text(query_ocupacion))
            ocupacion = res_ocupacion.scalar() or 0.0

            # Cancelaciones totales
            query_cancelaciones = """
                SELECT COUNT(id) AS total 
                FROM compras 
                WHERE estado = 'cancelada'
            """
            res_cancelaciones = conn.execute(text(query_cancelaciones))
            cancelaciones = res_cancelaciones.scalar() or 0

            # diccionario con los resultados
            kpis = {
                "entradas_vendidas": int(entradas),
                "ingresos": float(ingresos),
                "ocupacion_media": float(ocupacion),
                "total_cancelaciones": int(cancelaciones)
            }

            return kpis

    except Exception as e:
        print(f"Error al consultar los KPIs: {e}")
        return None