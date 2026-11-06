from datetime import datetime


def validar_fechas_ventas(fecha_desde, fecha_hasta, parametros):

    filtros_permitidos = ("fecha_desde", "fecha_hasta")

    for parametro in parametros:

        if parametro not in filtros_permitidos:
            return False, None, None, f"El filtro {parametro} no es valido"

        if len(parametros.getlist(parametro)) > 1:
            return False, None, None, f"El filtro {parametro} no puede enviarse mas de una vez"

    for fecha in (fecha_desde, fecha_hasta):

        if fecha is not None:

            if len(fecha) != 10:
                return False, None, None, "Las fechas deben tener el formato AAAA-MM-DD"

            try:
                datetime.strptime(fecha, "%Y-%m-%d")

            except ValueError:
                return False, None, None, "Se ingreso una fecha invalida"

    if fecha_desde is not None and fecha_hasta is not None and fecha_desde > fecha_hasta:
        return False, None, None, "La fecha inicial no puede ser posterior a la fecha final"

    return True, fecha_desde, fecha_hasta, None