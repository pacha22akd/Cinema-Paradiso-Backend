
from sqlalchemy import text
from src.utils.config import db


def obtener_funciones_por_pelicula(pelicula_id):
    """
    Obtiene todas las funciones vigentes de una película con datos de sala y local.
    """
    try:
        with db.connect() as conn:
            query = text("""
                SELECT
                    f.id AS funcion_id,
                    f.pelicula_id,
                    f.fecha_hora_inicio,
                    f.fecha_hora_fin,
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
                  AND f.fecha_hora_inicio >= NOW()
                  AND f.estado = 'programada'
                ORDER BY f.fecha_hora_inicio ASC
            """)

            resultado = conn.execute(query, {"pelicula_id": pelicula_id})
            funciones = [dict(fila) for fila in resultado.mappings()]

            for funcion in funciones:
                funcion["fecha_hora_inicio"] = funcion["fecha_hora_inicio"].isoformat()
                funcion["fecha_hora_fin"] = funcion["fecha_hora_fin"].isoformat()

            return funciones

    except Exception as e:
        print(f"Error al consultar funciones de la película: {e}")
        return None


def obtener_funcion_por_id(id_funcion):
    """
    Obtiene una función por ID, incluyendo si ya comenzó.
    """
    try:
        with db.connect() as conn:
            query = text("""
                SELECT *, fecha_hora_inicio <= NOW() AS ya_empezo
                FROM funciones
                WHERE id = :id_funcion
            """)

            resultado = conn.execute(query, {"id_funcion": id_funcion})
            fila = resultado.mappings().first()

            if fila is None:
                return None

            return dict(fila)

    except Exception as e:
        print(f"Error al obtener función por ID: {e}")
        return None


def obtener_butacas_por_funcion(funcion_id, sala_id):
    """
    Obtiene las butacas y su disponibilidad para una función.
    """
    try:
        with db.connect() as conn:
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

            resultado = conn.execute(
                query,
                {"funcion_id": funcion_id, "sala_id": sala_id}
            )

            return [dict(fila) for fila in resultado.mappings()]

    except Exception as e:
        print(f"Error al consultar disponibilidad de butacas: {e}")
        return None


def obtener_funciones():
    try:
        with db.connect() as conn:
            query = text("SELECT * FROM funciones")
            resultado = conn.execute(query)

            return [dict(fila) for fila in resultado.mappings()]

    except Exception as e:
        print(f"Error al obtener funciones: {e}")
        return None


def crear_funcion(datos_funcion):
    try:
        with db.connect() as conn:
            query = text("""
                INSERT INTO funciones (
                    pelicula_id,
                    sala_id,
                    fecha_hora_inicio,
                    fecha_hora_fin,
                    precio_base
                )
                VALUES (
                    :pelicula_id,
                    :sala_id,
                    :fecha_hora_inicio,
                    :fecha_hora_fin,
                    :precio_base
                )
            """)

            conn.execute(query, datos_funcion)
            conn.commit()

            return True

    except Exception as e:
        print(f"Error al crear función: {e}")
        return False


def actualizar_funcion(id_funcion, datos_actualizados):
    campos_permitidos = (
        "pelicula_id",
        "sala_id",
        "fecha_hora_inicio",
        "fecha_hora_fin",
        "precio_base"
    )

    condiciones = []
    parametros = {"id_funcion": id_funcion}

    for campo, valor in datos_actualizados.items():
        if campo not in campos_permitidos:
            raise ValueError("Campo no permitido")

        condiciones.append(f"{campo} = :{campo}")
        parametros[campo] = valor

    if not condiciones:
        raise ValueError("No se recibieron campos para actualizar")

    query = "UPDATE funciones SET " + ", ".join(condiciones)
    query += " WHERE id = :id_funcion"

    conn = db.connect()

    try:
        consulta = text("""
            SELECT id
            FROM funciones
            WHERE id = :id_funcion
        """)

        resultado = conn.execute(
            consulta,
            {"id_funcion": id_funcion}
        )

        if resultado.fetchone() is None:
            return None

        conn.execute(text(query), parametros)

        consulta = text("""
            SELECT *
            FROM funciones
            WHERE id = :id_funcion
        """)

        resultado = conn.execute(
            consulta,
            {"id_funcion": id_funcion}
        )

        fila = resultado.mappings().first()

        conn.commit()

        return dict(fila)

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()
