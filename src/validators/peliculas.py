def validar_busqueda_externa(titulo=None, anio=None):

    if titulo is None:
        return False, None, None, "El titulo es obligatorio"

    titulo = titulo.strip()

    if titulo == "":
        return False, None, None, "El titulo no puede estar vacio"

    if anio is not None:
        anio = anio.strip()

        if len(anio) != 4 or not anio.isdigit():
            return False, None, None, "El anio debe contener cuatro digitos numericos"

    return True, titulo, anio, None