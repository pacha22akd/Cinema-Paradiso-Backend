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