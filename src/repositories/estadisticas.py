from sqlalchemy import text
from src.utils.config import engine

def obtener_ocupacion_funciones():
    """
    Ejecuta la consulta SQL para calcular el porcentaje de ocupación por función.
    """
    try:
        with engine.connect() as conn:
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
            """

            result = conn.execute(text(query))
            rows = result.fetchall()

            ocupacion = [dict(zip(result.keys(), row)) for row in rows]

            # Como MySQL devuelve hora_inicio como timedelta y jsonify no lo puede convertir hago:
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
        with engine.connect() as conn:
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
        with engine.connect() as conn:
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