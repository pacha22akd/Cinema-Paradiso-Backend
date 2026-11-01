def validar_id_pelicula(id_pelicula):

    if id_pelicula <= 0:
        return False, "El id de la pelicula debe ser mayor a 0"

    return True, None

def validar_modificacion_pelicula(datos):

    if not isinstance(datos, dict):
        return False, None, "El cuerpo debe ser un objeto JSON"

    if len(datos) == 0:
        return False, None, "Debe enviar al menos un campo para modificar"

    campos_texto = {
        "api_id": 50,
        "titulo": 200,
        "sinopsis": None,
        "poster_url": 500,
        "clasificacion": 20,
        "genero": 100
    }

    campos_numericos = ("duracion_min", "anio_estreno")

    pelicula = {}

    for campo, valor in datos.items():

        if campo in campos_texto:

            if campo == "titulo" and (not isinstance(valor, str) or valor.strip() == ""):
                return False, None, "El titulo no puede estar vacio"

            if valor is not None:

                if not isinstance(valor, str):
                    return False, None, f"El campo {campo} debe ser texto"

                valor = valor.strip()

                if valor == "":
                    valor = None

                longitud_maxima = campos_texto[campo]

                if longitud_maxima is not None and valor is not None and len(valor) > longitud_maxima:
                    return False, None, f"El campo {campo} supera la longitud permitida"

            pelicula[campo] = valor

        elif campo in campos_numericos:

            if valor is not None and (type(valor) is not int or valor <= 0):
                return False, None, f"El campo {campo} debe ser un entero positivo"

            pelicula[campo] = valor

        else:
            return False, None, f"El campo {campo} no existe o no se puede modificar"

    return True, pelicula, None