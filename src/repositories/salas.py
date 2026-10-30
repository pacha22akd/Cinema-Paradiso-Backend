from sqlalchemy import text
from src.utils.config import engine

def obtener_salas():
    """
    Ejecuta la consulta SQL para traer la lista completa de salas desde la BD.
    """
    try:
        with engine.connect() as conn:
            query = "SELECT * FROM salas"
            result = conn.execute(text(query))
            rows = result.fetchall()
            
            salas = [dict(zip(result.keys(), row)) for row in rows]
            return salas
    except Exception as e:
        print(f"Error al consultar las salas en la base de datos: {e}")
        return None