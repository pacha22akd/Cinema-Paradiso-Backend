from src.repositories.funciones import obtener_funcion_por_id, obtener_butacas_por_funcion
from src.repositories.compras import registrar_compra_transaccion
from src.validators.compras import validar_datos_compra

def realizar_proceso_compra(usuario_id, funcion_id, butaca_ids):
    # 1. Validaciones de formato
    error = validar_datos_compra(usuario_id, funcion_id, butaca_ids)
    if error:
        return error

    # 2. Validar que la función solicitada exista
    funcion = obtener_funcion_por_id(funcion_id)
    if not funcion:
        return {"error": "La función solicitada no existe", "status": 404}  

    if funcion["estado"] != "programada":
        return {"error": "La función no está disponible para la venta", "status": 409}
    
    if funcion["ya_empezo"]:
        return {"error": "La función ya comenzó o finalizó", "status": 409}
    
    butacas_sala = obtener_butacas_por_funcion(funcion_id, funcion["sala_id"])
    if butacas_sala is None:
        return {"error": "No se pudo verificar la disponibilidad de las butacas", "status": 500}

    for b_id in butaca_ids:
        butaca_encontrada = None
        for butaca in butacas_sala:
            if butaca["butaca_id"] == b_id:
                butaca_encontrada = butaca

        if butaca_encontrada is None:
            return {"error": f"La butaca {b_id} no pertenece a la sala de esta función", "status": 400}

        if butaca_encontrada["estado_disponibilidad"] == "ocupada":
            return {"error": f"La butaca {b_id} ya está ocupada", "status": 409}

    # 3. Obtener el precio unitario y ejecutar la transacción
    precio_unitario = funcion["precio_base"]
    resultado = registrar_compra_transaccion(usuario_id, funcion_id, butaca_ids, precio_unitario)

    if resultado is None:
        return {"error": "No se pudo registrar la compra", "status": 500}

    return resultado