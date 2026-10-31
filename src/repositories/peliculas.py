from sqlalchemy import text
from src.utils.config import engine

def obtener_pelicula_por_id(pelicula_id):
    """
    Ejecuta la consulta SQL para traer los datos de una película por ID.
    """
    try: 
        with engine.connect() as conn:
            query = "SELECT * FROM peliculas WHERE id = :id"
            result = conn.execute(text(query), {"id": pelicula_id})
            row = result.fetchone()
            pelicula = dict(zip(result.keys(), row)) if row else None
            return pelicula
    except Exception as e:
        print(f"Error al consultar la base de datos: {e}")
        return None

def obtener_peliculas_cartelera(genero=None, titulo=None):
    try:
        with engine.connect() as conn:
            query_str = """
                SELECT id, api_id, titulo, sinopsis, poster_url, duracion_min, clasificacion, genero, anio_estreno
                FROM peliculas
                WHERE id IN (
                    SELECT pelicula_id 
                    FROM funciones 
                    WHERE fecha_hora_inicio >= NOW() AND estado = 'programada'
                )
            """
            params = {}

            if genero:
                query_str += " AND genero LIKE :genero"
                params["genero"] = f"%{genero}%"

            if titulo:
                query_str += " AND titulo LIKE :titulo"
                params["titulo"] = f"%{titulo}%"

            query = text(query_str)
            result = conn.execute(query, params)

            columnas = result.keys()
            peliculas = [dict(zip(columnas, row)) for row in result]

            return peliculas
    except Exception as e:
        print(f"Error al consultar cartelera de peliculas: {e}")
        return None