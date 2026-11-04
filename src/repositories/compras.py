
from sqlalchemy import text
from src.utils.config import db


def cancelar_compra_en_bd(id_compra, id_usuario):

    conn = db.connect()

    try:
        query = """
            SELECT usuario_id, estado
            FROM compras
            WHERE id = :id_compra
            FOR UPDATE
        """

        valores = {"id_compra": id_compra}

        resultado = conn.execute(text(query), valores)
        compra = resultado.fetchone()

        if compra is None:
            conn.rollback()
            return "no_existe"

        if compra.usuario_id != id_usuario:
            conn.rollback()
            return "no_existe"

        if compra.estado != "pendiente":
            conn.rollback()
            return "no_cancelable"

        query = """
            UPDATE compras
            SET estado = 'cancelada',
                fecha_cancelacion = NOW()
            WHERE id = :id_compra
        """

        conn.execute(text(query), valores)

        query = """
            UPDATE entradas
            SET estado = 'cancelada',
                fecha_cancelacion = NOW()
            WHERE compra_id = :id_compra
        """

        conn.execute(text(query), valores)

        conn.commit()

        return "cancelada"

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()
