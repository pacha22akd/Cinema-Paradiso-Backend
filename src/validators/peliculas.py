def validar_filtros_peliculas(titulo, genero, parametros):

    filtros_permitidos = ("titulo", "genero")

    for parametro in parametros:

        if parametro not in filtros_permitidos:
            return False, None, None, f"El filtro {parametro} no es valido"

        if len(parametros.getlist(parametro)) > 1:
            return False, None, None, f"El filtro {parametro} no puede enviarse mas de una vez"

    if titulo is not None:
        titulo = titulo.strip()

        if titulo == "":
            return False, None, None, "El titulo no puede estar vacio"

    if genero is not None:
        genero = genero.strip()

        if genero == "":
            return False, None, None, "El genero no puede estar vacio"

    return True, titulo, genero, None