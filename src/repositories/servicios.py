from sqlalchemy import text
from src.utils.config import db

def obtener_servicios():

    query = """SELECT * FROM servicios """
   
    conn = db.connect()
    resultado = conn.execute(text(query))

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

    
def agregar_servicio(nombre, descripcion, categoria, precio, stock, imagen_url):

    query = """INSERT INTO servicios (nombre, descripcion, categoria, precio, stock, imagen_url) VALUES (:nombre, :descripcion, :categoria, :precio, :stock, :imagen_url);"""

    valores = {
        "nombre": nombre, "descripcion": descripcion, "categoria": categoria,
        "precio": precio, "stock": stock, "imagen_url": imagen_url
    }
    conn = db.connect()
    resultado = conn.execute(text(query), valores)
    conn.commit()
    conn.close()
    

def modificar_servicio(id, nombre, descripcion, categoria, precio, stock, imagen_url):

    conn = db.connect()
    query = """UPDATE servicios SET nombre = :nombre, descripcion = :descripcion, categoria = :categoria, precio = :precio, stock = :stock, imagen_url = :imagen_url WHERE id = :id"""

    valores = {
        "id": id, "nombre": nombre, "descripcion": descripcion, "categoria": categoria,
        "precio": precio, "stock": stock, "imagen_url": imagen_url
    }
    conn = db.connect()
    resultado = conn.execute(text(query), valores)
    conn.commit()
    filas = resultado.rowcount
    conn.close()

    return filas > 0

def eliminar_servicio(id):

    query = """ DELETE FROM servicios WHERE id = :id """

    valores = {"id": id}

    conn = db.connect()
    resultado = conn.execute(text(query), valores)
    conn.commit()
    filas = resultado.rowcount
    conn.close()

    return filas > 0
