from sqlalchemy import text
from src.utils.config import engine

def obtener_funciones_por_pelicula(pelicula_id):
    """
    Obtiene todas las funciones vigentes de una película con datos de la sala y local.
    """
    try:
        conn = engine.connect()
        query = text("""
            SELECT 
                f.id AS funcion_id,
                f.pelicula_id,
                f.fecha,
                f.hora_inicio,
                f.hora_fin,
                f.precio_base,
                f.estado,
                s.id AS sala_id,
                s.nombre AS sala_nombre,
                s.tipo AS sala_tipo,
                l.id AS local_id,
                l.nombre AS local_nombre,
                l.direccion AS local_direccion,
                l.ciudad AS local_ciudad
            FROM funciones f
            INNER JOIN salas s ON f.sala_id = s.id
            INNER JOIN locales l ON s.local_id = l.id
            WHERE f.pelicula_id = :pelicula_id
              AND TIMESTAMP(f.fecha, f.hora_inicio) >= NOW()
              AND f.estado = 'programada'
            ORDER BY f.fecha ASC, f.hora_inicio ASC
        """)
        
        result = conn.execute(query, {"pelicula_id": pelicula_id})
        columnas = result.keys()
        funciones = [dict(zip(columnas, row)) for row in result]
        
        conn.close()
        return funciones
    except Exception as e:
        print(f"Error al consultar funciones de la película: {e}")
        return None

def obtener_funcion_por_id(funcion_id):
    """
    Obtiene los detalles de una función por su ID.
    """
    try:
        conn = engine.connect()
        query = text("SELECT * FROM funciones WHERE id = :id")
        result = conn.execute(query, {"id": funcion_id})
        row = result.fetchone()
        funcion = dict(zip(result.keys(), row)) if row else None
        conn.close()
        return funcion
    except Exception as e:
        print(f"Error al consultar la función: {e}")
        return None

def obtener_butacas_por_funcion(funcion_id, sala_id):
    """
    Obtiene el mapa de butacas de la sala indicando si están ocupadas o disponibles para la función.
    """
    try:
        conn = engine.connect()
        query = text("""
            SELECT 
                b.id AS butaca_id,
                b.fila,
                b.numero,
                b.tipo,
                CASE 
                    WHEN e.id IS NOT NULL THEN 'ocupada'
                    ELSE 'disponible'
                END AS estado_disponibilidad
            FROM butacas b
            LEFT JOIN entradas e 
                   ON b.id = e.butaca_id 
                  AND e.funcion_id = :funcion_id 
                  AND e.estado != 'cancelada'
            WHERE b.sala_id = :sala_id
            ORDER BY b.fila ASC, b.numero ASC
        """)
        
        result = conn.execute(query, {"funcion_id": funcion_id, "sala_id": sala_id})
        columnas = result.keys()
        butacas = [dict(zip(columnas, row)) for row in result]
        
        conn.close()
        return butacas
    except Exception as e:
        print(f"Error al consultar disponibilidad de butacas: {e}")
        return None