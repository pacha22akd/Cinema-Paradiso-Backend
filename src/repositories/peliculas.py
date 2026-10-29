from sqlalchemy import text
from src.utils.config import db

def obtener_pelicula_por_id(id_pelicula):
    """
    Ejecuta la consulta SQL para traer los datos de una película por ID.
    """
    try: 
        conn = db.connect()
        query = "SELECT * FROM cine_paradiso_peliculas WHERE id = :id"
        result = conn.execute(text(query), {"id": id_pelicula})
        row = result.fetchone()
        pelicula = dict(zip(result.keys(), row)) if row else None
        conn.close()
        return pelicula
    except Exception as e:
        print(f"Error al consultar la base de datos: {e}")
        return None

    