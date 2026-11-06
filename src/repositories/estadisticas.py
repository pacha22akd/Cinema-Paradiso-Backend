from sqlalchemy import text
from src.utils.config import db

def obtener_cancelaciones():

    query = """ SELECT motivo_cancelacion AS motivo, COUNT(*) AS cantidad FROM compras WHERE estado = 'cancelada' GROUP BY motivo_cancelacion """

    conn = db.connect()
    resultado = conn.execute(text(query))

    motivos = []
    for row in resultado:
        motivos.append(dict(row._mapping))
    conn.close()

    return motivos
