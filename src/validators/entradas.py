def validar_datos_qr(codigo, funcion_id):

    if not codigo:
        raise ValueError("El código QR es obligatorio.")

    if not isinstance(funcion_id, int) or isinstance(funcion_id, bool) or funcion_id <= 0:
        raise ValueError("El id de la función debe ser un número entero mayor a 0.")