from sqlalchemy import text
from src.utils.config import db

def obtener_entrada(id):

    query = """ SELECT e.id, e.qr_codigo, e.estado, e.precio, b.fila AS butaca_fila, b.numero AS butaca_numero,
    s.nombre AS sala, f.fecha_hora_inicio, p.titulo AS pelicula
    FROM entradas e
    JOIN butacas b ON e.butaca_id = b.id
    JOIN salas s ON b.sala_id = s.id
    JOIN funciones f ON e.funcion_id = f.id
    JOIN peliculas p ON f.pelicula_id = p.id
    WHERE e.id = :id """

    valores = {"id": id}

    conn = db.connect()
    resultado = conn.execute(text(query), valores)

    entradas = []
    for fila in resultado:
        entrada = {
            "id": fila.id,
            "qr_codigo": fila.qr_codigo,
            "estado": fila.estado,
            "precio": fila.precio,
            "butaca_fila": fila.butaca_fila,
            "butaca_numero": fila.butaca_numero,
            "sala": fila.sala,
            "fecha_hora_inicio": fila.fecha_hora_inicio,
            "pelicula": fila.pelicula,
        }
        entradas.append(entrada)

    conn.close()

    if len(entradas) == 0:
        return None

    return entradas[0]
