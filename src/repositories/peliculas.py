from sqlalchemy import text
from src.utils.config import db


def actualizar_pelicula(id_pelicula, datos):

    columnas_permitidas = (
        "api_id",
        "titulo",
        "sinopsis",
        "poster_url",
        "duracion_min",
        "clasificacion",
        "genero",
        "anio_estreno"
    )

    condiciones = []
    parametros = {"id_pelicula": id_pelicula}

    for campo, valor in datos.items():

        if campo not in columnas_permitidas:
            raise ValueError("Campo no permitido")

        condiciones.append(f"{campo} = :{campo}")
        parametros[campo] = valor

    query = "UPDATE peliculas SET " + ", ".join(condiciones)
    query += " WHERE id = :id_pelicula"

    conn = db.connect()

    try:
        consulta = "SELECT id FROM peliculas WHERE id = :id_pelicula"

        resultado = conn.execute(
            text(consulta),
            {"id_pelicula": id_pelicula}
        )

        if resultado.fetchone() is None:
            return None

        conn.execute(text(query), parametros)

        consulta = "SELECT * FROM peliculas WHERE id = :id_pelicula"

        resultado = conn.execute(
            text(consulta),
            {"id_pelicula": id_pelicula}
        )

        fila = resultado.fetchone()

        conn.commit()

        return dict(fila._mapping)

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()