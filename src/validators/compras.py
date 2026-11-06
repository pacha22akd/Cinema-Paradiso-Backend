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

def validar_id_compra(id_compra):

    if type(id_compra) is not int or id_compra <= 0:
        return False, "El ID de la compra debe ser un entero positivo"

    return True, None

def convertir_a_entero(valor, mensaje_error):

    try:
        numero = float(valor)

        if numero != int(numero):
            raise ValueError

        return int(numero)

    except (TypeError, ValueError, OverflowError):
        raise ValueError(mensaje_error)


def validar_servicio_en_compra(servicio_id, cantidad):

    servicio_id = convertir_a_entero(servicio_id, "El id del servicio debe ser un número entero")
    cantidad = convertir_a_entero(cantidad, "La cantidad debe ser un número entero")

    if servicio_id <= 0:
        raise ValueError("El id del servicio debe ser mayor a 0")

    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor a 0")

    return servicio_id, cantidad
