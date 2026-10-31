def validar_alta_pelicula(datos):

    if not isinstance(datos, dict):
        return False, None, "El cuerpo debe ser un objeto JSON"

    titulo = datos.get("titulo")

    if not isinstance(titulo, str) or titulo.strip() == "":
        return False, None, "El titulo es obligatorio y no puede estar vacio"

    campos_texto = {
        "api_id": 50,
        "titulo": 200,
        "sinopsis": None,
        "poster_url": 500,
        "clasificacion": 20,
        "genero": 100
    }

    pelicula = {}

    for campo, longitud_maxima in campos_texto.items():

        valor = datos.get(campo)

        if valor is not None:

            if not isinstance(valor, str):
                return False, None, f"El campo {campo} debe ser texto"

            valor = valor.strip()

            if valor == "":
                valor = None

            if longitud_maxima is not None and valor is not None:
                if len(valor) > longitud_maxima:
                    return False, None, f"El campo {campo} supera la longitud permitida"

        pelicula[campo] = valor

    for campo in ("duracion_min", "anio_estreno"):

        valor = datos.get(campo)

        if valor is not None:
            if type(valor) is not int or valor <= 0:
                return False, None, f"El campo {campo} debe ser un entero positivo"

        pelicula[campo] = valor

    return True, pelicula, None