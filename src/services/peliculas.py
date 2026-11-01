import src.repositories.peliculas as peliculas_repository


def modificar_pelicula(id_pelicula, datos):

    pelicula = peliculas_repository.actualizar_pelicula(
        id_pelicula, datos
    )

    return pelicula