from sqlalchemy import text
from src.utils.config import db

def buscar_entrada_por_qr(codigo):


    #busco la sala, la butaca, la hora de la funcion y que funcion es
    query = """ 
    SELECT e.id, e.funcion_id, e.estado, f.fecha_hora_inicio, f.estado AS estado_funcion,
           p.titulo AS pelicula, s.nombre AS sala, b.fila, b.numero
    FROM entradas e 
    JOIN compras c on e.compra_id = c.id
    JOIN funciones f ON e.funcion_id = f.id
    JOIN peliculas p ON f.pelicula_id = p.id
    JOIN salas s ON f.sala_id = s.id
    JOIN butacas b ON e.butaca_id = b.id
    WHERE e.qr_codigo = :codigo """

    valores = {"codigo": codigo}

    conn = db.connect()
    resultado = conn.execute(text(query), valores)
    filas = [dict(row._mapping) for row in resultado]
    conn.close()

    if len(filas) == 0:
        return None

    return filas[0]

def marcar_entrada_usada(id):

    query = """ UPDATE entradas SET estado = 'usada', fecha_uso = NOW() WHERE id = :id AND estado = 'valida' """

    valores = {"id": id}

    conn = db.connect()
    resultado = conn.execute(text(query), valores)
    conn.commit()
    filas = resultado.rowcount
    conn.close()

    return filas > 0

def obtener_entrada(id, usuario_id):

    query = """ SELECT e.id, e.estado, e.precio, b.fila AS butaca_fila, b.numero AS butaca_numero,
    s.nombre AS sala, f.fecha_hora_inicio, p.titulo AS pelicula
    FROM entradas e
    JOIN butacas b ON e.butaca_id = b.id
    JOIN salas s ON b.sala_id = s.id
    JOIN funciones f ON e.funcion_id = f.id
    JOIN peliculas p ON f.pelicula_id = p.id
    JOIN compras c ON e.compra_id = c.id
    WHERE e.id = :id AND c.usuario_id = :usuario_id """
    
    conn = db.connect()
    resultado = conn.execute(text(query), {"id": id, "usuario_id": usuario_id})

    entradas = []
    for fila in resultado:
        entrada = {
            "id": fila.id,
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
