def validar_busqueda_externa(titulo, anio, parametros):

    filtros_permitidos = ("titulo", "anio")

    for parametro in parametros:

        if parametro not in filtros_permitidos:
            return False, None, None, f"El filtro {parametro} no es valido"

        if len(parametros.getlist(parametro)) > 1:
            return False, None, None, f"El filtro {parametro} no puede enviarse mas de una vez"

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