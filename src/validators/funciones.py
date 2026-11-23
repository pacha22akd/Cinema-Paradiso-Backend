
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


def validar_modificacion_funcion(datos):

    if not isinstance(datos, dict):
        return False, None, "El cuerpo debe ser un objeto JSON"

    if len(datos) == 0:
        return False, None, "Debe enviar al menos un campo para modificar"

    campos_permitidos = (
        "pelicula_id",
        "sala_id",
        "fecha_hora_inicio",
        "fecha_hora_fin",
        "precio_base"
    )

    funcion = {}

    for campo, valor in datos.items():

        if campo not in campos_permitidos:
            return False, None, f"El campo {campo} no existe o no se puede modificar"

        if campo in ("pelicula_id", "sala_id"):

            if type(valor) is not int or valor <= 0:
                return False, None, f"El campo {campo} debe ser un entero positivo"

            funcion[campo] = valor

        elif campo in ("fecha_hora_inicio", "fecha_hora_fin"):

            try:
                datetime.fromisoformat(valor)
            except (ValueError, TypeError):
                return False, None, f"El campo {campo} debe tener un formato de fecha válido"

            funcion[campo] = valor

        elif campo == "precio_base":

            if (
                isinstance(valor, bool)
                or not isinstance(valor, (int, float))
                or valor < 0
            ):
                return False, None, "El precio debe ser un número mayor o igual a cero"

            funcion[campo] = valor

    return True, funcion, None
