from sqlalchemy import text
from src.utils.config import db

def obtener_locales():
    try:
        with db.connect() as conn:
            query = text("SELECT * FROM locales")
            resultado = conn.execute(query)
            locales = [dict(fila) for fila in resultado.mappings()]
            
        return locales
    
    except Exception as e:
        print(f"Error al obtener locales: {e}")
        return None