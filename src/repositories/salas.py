from sqlalchemy import text
from src.utils.config import db

def obtener_salas():
    """
    Ejecuta la consulta SQL para traer la lista completa de salas.
    """
    try:
        conn = db.connect()
        query = "SELECT * FROM cine_paradiso_salas"
        result = conn.execute(text(query))
        rows = result.fetchall()
        
        # Convierte cada fila a un diccionario usando zip
        salas = [dict(zip(result.keys(), row)) for row in rows]
        
        conn.close()
        return salas
    except Exception as e:
        print(f"Error al consultar las salas en la base de datos: {e}")
        return None