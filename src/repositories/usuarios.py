from sqlalchemy import text
from src.utils.config import db


def actualizar_perfil(id_usuario, datos):

    columnas_permitidas = ("nombre", "apellido", "email", "telefono")

    condiciones = []
    parametros = {"id_usuario": id_usuario}

    for campo, valor in datos.items():

        if campo not in columnas_permitidas:
            raise ValueError("Campo no permitido")

        condiciones.append(f"{campo} = :{campo}")
        parametros[campo] = valor

    query = "UPDATE usuarios SET " + ", ".join(condiciones)
    query += " WHERE id = :id_usuario"

    conn = db.connect()

    try:
        consulta = "SELECT id FROM usuarios WHERE id = :id_usuario"

        resultado = conn.execute(text(consulta), {"id_usuario": id_usuario})

        if resultado.fetchone() is None:
            return None

        if "email" in datos:

            consulta = """SELECT id FROM usuarios
                          WHERE email = :email
                          AND id != :id_usuario"""

            resultado = conn.execute(text(consulta), {"email": datos["email"], "id_usuario": id_usuario})

            if resultado.fetchone() is not None:
                return "email_duplicado"

        conn.execute(text(query), parametros)

        consulta = """SELECT id, nombre, apellido, email, telefono
                      FROM usuarios
                      WHERE id = :id_usuario"""

        resultado = conn.execute(text(consulta), {"id_usuario": id_usuario})

        fila = resultado.fetchone()

        conn.commit()

        return dict(fila._mapping)

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()