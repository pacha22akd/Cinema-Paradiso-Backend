from sqlalchemy import text
from src.utils.config import db

def obtener_ocupacion_funciones():
    """
    Ejecuta la consulta SQL para calcular el porcentaje de ocupación por función.
    """
    try:
        conn = db.connect()
        
        query = """
            SELECT 
                f.id AS funcion_id,
                p.titulo AS pelicula,
                s.nombre AS sala,
                f.fecha_hora,
                s.capacidad,
                COUNT(e.id) AS entradas_vendidas,
                ROUND((COUNT(e.id) * 100.0 / s.capacidad), 2) AS porcentaje_ocupacion
            FROM cine_paradiso_funciones f
            JOIN cine_paradiso_peliculas p 
                ON f.id_pelicula = p.id
            JOIN cine_paradiso_salas s 
                ON f.id_sala = s.id
            LEFT JOIN cine_paradiso_entradas e 
                ON e.id_funcion = f.id
            GROUP BY 
                f.id, 
                p.titulo, 
                s.nombre, 
                f.fecha_hora, 
                s.capacidad
        """
        
        result = conn.execute(text(query))
        rows = result.fetchall()
        
       
        ocupacion = [dict(zip(result.keys(), row)) for row in rows]
        
        conn.close()
        return ocupacion
    except Exception as e:
        print(f"Error al consultar la ocupación de funciones: {e}")
        return None

def obtener_ocupacion_peliculas():
    """
    Ejecuta la consulta SQL para calcular el porcentaje de ocupación promedio por película.
    """
    try:
        conn = db.connect()
        
        query = """
            SELECT 
                p.id AS pelicula_id,
                p.titulo AS pelicula,
                COUNT(f.id) AS total_funciones,
                SUM(s.capacidad) AS capacidad_total,
                COUNT(e.id) AS total_entradas_vendidas,
                ROUND((COUNT(e.id) * 100.0 / SUM(s.capacidad)), 2) AS porcentaje_ocupacion
            FROM cine_paradiso_peliculas p
            JOIN cine_paradiso_funciones f 
                ON f.id_pelicula = p.id
            JOIN cine_paradiso_salas s 
                ON f.id_sala = s.id
            LEFT JOIN cine_paradiso_entradas e 
                ON e.id_funcion = f.id
            GROUP BY 
                p.id, 
                p.titulo
        """
        
        result = conn.execute(text(query))
        rows = result.fetchall()
        
        # Mapeo a lista de diccionarios con zip
        ocupacion = [dict(zip(result.keys(), row)) for row in rows]
        
        conn.close()
        return ocupacion
    except Exception as e:
        print(f"Error al consultar la ocupación por películas: {e}")
        return None

def obtener_ocupacion_franjas_horarias():
    """
    Ejecuta la consulta SQL para agrupar y contar las entradas vendidas por franja horaria.
    """
    try:
        conn = db.connect()
        
        query = """
            SELECT 
                HOUR(f.fecha_hora) AS hora,
                COUNT(e.id) AS entradas_vendidas
            FROM cine_paradiso_funciones f
            LEFT JOIN cine_paradiso_entradas e 
                ON e.id_funcion = f.id
            GROUP BY 
                HOUR(f.fecha_hora)
            ORDER BY 
                hora ASC
        """
        
        result = conn.execute(text(query))
        rows = result.fetchall()
        
        # Mapeo tradicional
        franjas = [dict(zip(result.keys(), row)) for row in rows]
        
        conn.close()
        return franjas
    except Exception as e:
        print(f"Error al consultar las franjas horarias: {e}")
        return None