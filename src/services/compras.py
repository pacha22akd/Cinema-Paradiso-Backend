from src.repositories import funciones
from src.repositories import compras

def obtener_compra(id_compra):
    compra = compras.obtener_compra_por_id(id_compra)

    if compra is None:
        return {"error": "No existe la compra buscada", "status": 404}

    compra["fecha_compra"] = str(compra["fecha_compra"]) if compra["fecha_compra"] else None
    compra["fecha_hora_inicio"] = str(compra["fecha_hora_inicio"]) if compra["fecha_hora_inicio"] else None
    compra["fecha_hora_fin"] = str(compra["fecha_hora_fin"]) if compra["fecha_hora_fin"] else None

    return compra