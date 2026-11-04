import re


def validar_modificacion_perfil(datos):

    if not isinstance(datos, dict):
        return False, None, "El cuerpo debe ser un objeto JSON"

    if len(datos) == 0:
        return False, None, "Debe enviar al menos un campo para modificar"

    campos_texto = {
        "nombre": 100,
        "apellido": 100,
        "email": 150,
        "telefono": 30
    }

    perfil = {}

    for campo, valor in datos.items():

        if campo not in campos_texto:
            return False, None, f"El campo {campo} no se puede modificar"

        if campo == "telefono" and valor is None:
            perfil[campo] = None

        else:
            if not isinstance(valor, str):
                return False, None, f"El campo {campo} debe ser texto"

            valor = valor.strip()

            if valor == "":
                if campo == "telefono":
                    valor = None
                else:
                    return False, None, f"El campo {campo} no puede estar vacio"

            if valor is not None and len(valor) > campos_texto[campo]:
                return False, None, f"El campo {campo} supera la longitud permitida"

            if campo == "email":
                if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor) is None:
                    return False, None, "El email no tiene un formato valido"

                valor = valor.lower()

            perfil[campo] = valor

    return True, perfil, None