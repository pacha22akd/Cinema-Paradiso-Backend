from sqlalchemy import text
from src.utils.config import db

def crear_usuario(nombre, apellido, email, password_hash, telefono, rol_id):
    query = """
        INSERT INTO usuarios (nombre, apellido, email, password_hash, telefono, rol_id)
        VALUES (:nombre, :apellido, :email, :password_hash, :telefono, :rol_id)
    """
    valores = {
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "password_hash": password_hash,
        "telefono": telefono,
        "rol_id": rol_id
    }
    
    conn = db.engine.connect()
    resultado = conn.execute(text(query), valores)
    conn.commit() 
    nuevo_id = resultado.lastrowid
    conn.close()
    
    return nuevo_id