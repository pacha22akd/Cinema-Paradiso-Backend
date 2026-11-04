from sqlalchemy import text
from src.utils.config import db


def obtener_peliculas(titulo=None, genero=None)->list:

    conn = db.connect()

    try:
        query = "SELECT * FROM peliculas"
        condiciones = []
        parametros = {}

        if (titulo is not None):
            condiciones.append("titulo LIKE :titulo")
            parametros["titulo"] = f"%{titulo}%"

        if (genero is not None):
            condiciones.append("genero LIKE :genero")
            parametros["genero"] = f"%{genero}%"

        if (len(condiciones) > 0):
            query += " WHERE " + " AND ".join(condiciones)

        resultado = conn.execute(text(query), parametros)

        filas = resultado.fetchall()

        peliculas = [dict(fila._mapping) for fila in filas]

        return peliculas

    finally:
        conn.close()