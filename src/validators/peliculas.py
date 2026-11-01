def validar_id_pelicula(id_pelicula):

    if id_pelicula <= 0:
        return False, "El id de la pelicula debe ser mayor a 0"

    return True, None