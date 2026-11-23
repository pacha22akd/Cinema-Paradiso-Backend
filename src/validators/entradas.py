def validar_datos_qr(codigo):

    if not codigo:
        raise ValueError("El código QR es obligatorio.")