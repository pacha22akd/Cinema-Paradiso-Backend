from datetime import date
from repositories import entradas_repository

def validar_qr(codigo, funcion_id):

    if not codigo:
        raise ValueError("El código QR es obligatorio.")

    if funcion_id is None or funcion_id <= 0:
        raise ValueError("El id de la función debe ser mayor a 0.")

    entrada = entradas_repository.buscar_entrada_por_qr(codigo)

    if entrada is None:
        return {"valida": False, "motivo": "El código QR no existe", "estado_entrada": None}

    estado = entrada["estado"]

    if entrada["funcion_id"] != funcion_id:
        return {"valida": False, "motivo": "La entrada no corresponde a ésta función", "estado_entrada": estado}

    if estado == "usada":
        return {"valida": False, "motivo": "La entrada ya fue utilizada", "estado_entrada": estado}

    if estado == "cancelada":
        return {"valida": False, "motivo": "La entrada fue cancelada", "estado_entrada": estado}

    if entrada["estado_funcion"] == "cancelada":
        return {"valida": False, "motivo": "La función está cancelada.", "estado_entrada": estado}

    if entrada["estado_funcion"] == "finalizada":
        return {"valida": False, "motivo": "La función está finalizada.", "estado_entrada": estado}

    if entrada["fecha"] != date.today():
        return {"valida": False, "motivo": "La entrada no es para el día de hoy", "estado_entrada": estado}

    marcada = entradas_repository.marcar_entrada_usada(entrada["id"])

    if not marcada:
        return {"valida": False, "motivo": "La entrada ya fue utilizada", "estado_entrada": "usada"}

    return {"valida": True, "motivo": "Entrada válida", "estado_entrada": "usada"}

