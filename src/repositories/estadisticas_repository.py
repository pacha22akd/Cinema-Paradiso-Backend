from sqlalchemy import text
from src.utils.config import db

def obtener_cancelaciones():

    query = """ SELECT motivo_cancelacion FROM compras WHERE estado = 'cancelada' """

    conn = db.connect()
    resultado = conn.execute(text(query))
    motivos = []
    for row in result:
        motivos.append(dict(row._mapping))
    conn.close()