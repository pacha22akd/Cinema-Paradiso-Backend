from sqlalchemy import text
from src.utils.config import db

def buscar_entrada_por_qr(codigo):

    query = """ SELECT e.id, e.funcion_id, e.estado, f.fecha, f.estado AS estado_funcion 
    FROM entradas e 
    JOIN compras c on e.compra_id = c.id
    JOIN funciones f ON e.funcion_id = f.id
    WHERE e.qr_codigo = :codigo """

    valores = {"qr_codigo": codigo}

    conn = db.connect()
    resultado = conn.execute(text(query), valores)
    filas = [dict(row.mapping) for row in resultado]
    conn.close

    if len(filas) == 0:
        return None

    return filas[0]

def marcar_entrada_usada(id):

    query = """ UPDATE entradas SET estado = 'usada', fecha_uso = NOW() WHERE id = :id AND estado = 'valida' """

    valores {"id": id}

    conn = db.connect()
    resultado = conn.execute(text(query), valores)
    conn.commit()
    filas = resultado.rowcount
    conn.close()

    return filas > 0