from sqlalchemy import text
from src.utils.config import db

def obtener_servicios():

    query = """SELECT * from servicios """
    result = conn.execute(text(query))
    conn.close()
    
    return result

    
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
    query = """UPDATE servicios SET nombre = :nombre, descripcion = :descripcion, categoria = :categoria, precio = :precio, stock = :stock, imagen_url = :imagen_url WHERE id == :id"""

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

    query = f"DELETE FROM servicios WHERE id = {id}"

    conn = db.connect()
    resultado = conn.execute(text(query))
    conn.commit()
    filas = resultado.rowcount
    conn.close()

    return filas > 0