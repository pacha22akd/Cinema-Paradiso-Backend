import uuid
from sqlalchemy import text
from src.utils.config import db

def obtener_compra_por_id(id_compra):
    query_compra = """
        SELECT c.id, c.codigo, c.total, c.estado, c.fecha_compra, c.numero_factura,
               f.id AS funcion_id, f.fecha_hora_inicio, f.fecha_hora_fin,
               p.titulo AS pelicula, s.nombre AS sala, l.nombre AS local
        FROM compras c
        JOIN funciones f ON c.funcion_id = f.id
        JOIN peliculas p ON f.pelicula_id = p.id
        JOIN salas s ON f.sala_id = s.id
        JOIN locales l ON s.local_id = l.id
        WHERE c.id = :id
    """
    
    query_entradas = """
        SELECT e.id, e.precio, e.qr_codigo, e.estado,
               b.fila, b.numero, b.tipo AS tipo_butaca
        FROM entradas e
        JOIN butacas b ON e.butaca_id = b.id
        WHERE e.compra_id = :id
    """
    
    query_servicios = """
        SELECT cs.cantidad, cs.precio_unitario, cs.subtotal,
               s.nombre AS servicio
        FROM compra_servicios cs
        JOIN servicios s ON cs.servicio_id = s.id
        WHERE cs.compra_id = :id
    """

    valores = {"id": id_compra}

    conn = db.engine.connect()
    
    resultado_compra = conn.execute(text(query_compra), valores).fetchone()
    if not resultado_compra:
        conn.close()
        return None

    compra = {
        "id": resultado_compra.id,
        "codigo": resultado_compra.codigo,
        "total": float(resultado_compra.total),
        "estado": resultado_compra.estado,
        "fecha_compra": resultado_compra.fecha_compra,
        "numero_factura": resultado_compra.numero_factura,
        "funcion_id": resultado_compra.funcion_id,
        "fecha_hora_inicio": resultado_compra.fecha_hora_inicio,
        "fecha_hora_fin": resultado_compra.fecha_hora_fin,
        "pelicula": resultado_compra.pelicula,
        "sala": resultado_compra.sala,
        "local": resultado_compra.local,
        "entradas": [],
        "servicios": []
    }

    resultado_entradas = conn.execute(text(query_entradas), valores)
    for fila in resultado_entradas:
        compra["entradas"].append({
            "id": fila.id,
            "butaca": f"{fila.fila}{fila.numero}",
            "tipo_butaca": fila.tipo_butaca,
            "precio": float(fila.precio),
            "qr_codigo": fila.qr_codigo,
            "estado": fila.estado
        })

    resultado_servicios = conn.execute(text(query_servicios), valores)
    for fila in resultado_servicios:
        compra["servicios"].append({
            "servicio": fila.servicio,
            "cantidad": fila.cantidad,
            "precio_unitario": float(fila.precio_unitario),
            "subtotal": float(fila.subtotal)
        })

    conn.close()
    return compra