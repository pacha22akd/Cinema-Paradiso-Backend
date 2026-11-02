
from datetime import datetime


def validar_datos_funcion(datos):
    if not isinstance(datos, dict):
        return False, "El cuerpo debe ser un objeto JSON"

    campos_obligatorios = [
        "pelicula_id",
        "sala_id",
        "fecha_hora_inicio",
        "fecha_hora_fin",
        "precio_base"
    ]

    for campo in campos_obligatorios:
        if campo not in datos:
            return False, f"Falta el campo obligatorio: {campo}"

    if not isinstance(datos["pelicula_id"], int) or datos["pelicula_id"] <= 0:
        return False, "pelicula_id debe ser un entero positivo"

    if not isinstance(datos["sala_id"], int) or datos["sala_id"] <= 0:
        return False, "sala_id debe ser un entero positivo"

    try:
        inicio = datetime.fromisoformat(datos["fecha_hora_inicio"])
        fin = datetime.fromisoformat(datos["fecha_hora_fin"])
    except (ValueError, TypeError):
        return False, "Las fechas deben tener un formato válido, por ejemplo 2026-11-02T18:00:00"

    if fin <= inicio:
        return False, "La fecha de fin debe ser posterior a la fecha de inicio"

    if (
        isinstance(datos["precio_base"], bool)
        or not isinstance(datos["precio_base"], (int, float))
        or datos["precio_base"] < 0
    ):
        return False, "precio_base debe ser un número mayor o igual a cero"

    estados_validos = ["programada", "en_curso", "finalizada", "cancelada"]

    if "estado" in datos and datos["estado"] not in estados_validos:
        return False, "El estado no es válido"

    return True, None
