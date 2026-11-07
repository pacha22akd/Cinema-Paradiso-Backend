from sqlalchemy import text
from src.utils.config import db

def obtener_servicios_adicionales(categoria):

    conn = db.connect()

    if categoria is None:
        query = """ SELECT * FROM servicios """
        resultado = conn.execute(text(query))

    else: 
        query = """ SELECT * FROM servicios WHERE categoria = :categoria """
        valores = {"categoria": categoria}
        resultado = conn.execute(text(query), valores)

    servicios = []
    for fila in resultado:
        servicio = {
            "id": fila.id,
            "nombre": fila.nombre,
            "descripcion": fila.descripcion,
            "categoria": fila.categoria,
            "precio": fila.precio,
            "stock": fila.stock,
            "imagen_url": fila.imagen_url,
        }
        servicios.append(servicio)

    conn.close()

    return servicios
