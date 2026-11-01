from sqlalchemy import text
from src.utils.config import db


def eliminar_pelicula(id_pelicula):

    conn = db.connect()

    try:
        parametros = {"id_pelicula": id_pelicula}

        query = """SELECT id FROM peliculas
                   WHERE id = :id_pelicula"""

        resultado = conn.execute(text(query), parametros)

        if resultado.fetchone() is None:
            return "no_existe"

        query = """SELECT id FROM funciones
                   WHERE pelicula_id = :id_pelicula
                   LIMIT 1"""

        resultado = conn.execute(text(query), parametros)

        if resultado.fetchone() is not None:
            return "con_funciones_asociadas"

        query = """DELETE FROM peliculas
                   WHERE id = :id_pelicula"""

        resultado = conn.execute(text(query), parametros)

        conn.commit()

        if resultado.rowcount == 0:
            return "no_existe"

        return "eliminada"

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()