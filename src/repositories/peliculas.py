from sqlalchemy import text
from src.utils.config import db


def insertar_pelicula(datos):

    query = """INSERT INTO peliculas (
                   api_id,
                   titulo,
                   sinopsis,
                   poster_url,
                   duracion_min,
                   clasificacion,
                   genero,
                   anio_estreno
               )
               VALUES (
                   :api_id,
                   :titulo,
                   :sinopsis,
                   :poster_url,
                   :duracion_min,
                   :clasificacion,
                   :genero,
                   :anio_estreno
               )"""

    conn = db.connect()

    try:
        resultado = conn.execute(text(query), datos)

        id_pelicula = resultado.lastrowid

        conn.commit()

        return id_pelicula

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()