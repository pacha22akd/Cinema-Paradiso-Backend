def validar_datos_compra(usuario_id, funcion_id, butaca_ids):
    """
    Valida el formato de los datos de la compra (sin consultar la base).
    Devuelve un diccionario de error si algo está mal, o None si está todo bien.
    """
    if not usuario_id or not funcion_id or not butaca_ids:
        return {"error": "Faltan datos: usuario_id, funcion_id y butaca_ids son obligatorios", "status": 400}

    if not isinstance(butaca_ids, list) or len(butaca_ids) == 0:
        return {"error": "butaca_ids debe ser una lista con al menos una butaca", "status": 400}

    butacas_vistas = []
    for b_id in butaca_ids:
        if b_id in butacas_vistas:
            return {"error": "Hay butacas repetidas en la solicitud", "status": 400}
        butacas_vistas.append(b_id)

    return None