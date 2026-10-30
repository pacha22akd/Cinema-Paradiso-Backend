from src.repositories.funciones import obtener_funcion_por_id
from src.repositories.compras import registrar_compra_transaccion

def realizar_proceso_compra(usuario_id, funcion_id, butaca_ids):
    # 1. Validaciones de presencia y formato de datos
    if not usuario_id or not funcion_id or not butaca_ids:
        return None

    if not isinstance(butaca_ids, list) or len(butaca_ids) == 0:
        return None

    # 2. Validar que la función solicitada exista
    funcion = obtener_funcion_por_id(funcion_id)
    if not funcion:
        return None

    # 3. Obtener el precio unitario y ejecutar la transacción
    precio_unitario = funcion["precio_base"]
    resultado = registrar_compra_transaccion(usuario_id, funcion_id, butaca_ids, precio_unitario)

    return resultado