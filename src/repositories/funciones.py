from sqlalchemy import text
from src.utils.config import db

def obtener_funciones():
    try:
        with db.connect() as conn:
            query = text("SELECT * FROM funciones")
            resultado = conn.execute(query)
            funciones = [dict(fila) for fila in resultado.mappings()]
            
            return funciones
    except Exception as e:
        print(f"Error al obtener funciones: {e}")
        return None

def obtener_funcion_por_id(id_funcion):
    try:
        with db.connect() as conn:
            query = text("SELECT * FROM funciones WHERE id = :id_funcion")
            
            resultado = conn.execute(query, {"id_funcion": id_funcion})
            
            fila = resultado.mappings().first()
            
            if fila is None:
                return None
            return dict(fila)
    
    except Exception as e:
        print(f"Error al obtener función por ID: {e}")
        return None