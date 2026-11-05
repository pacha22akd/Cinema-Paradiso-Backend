def validar_datos_qr(codigo, funcion_id):

    if not codigo:
        raise ValueError("El código QR es obligatorio.")

    if funcion_id is None or funcion_id <= 0:
        raise ValueError("El id de la función debe ser mayor a 0.")