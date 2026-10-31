import src.repositories.peliculas as peliculas_repository


def crear_pelicula(datos):

    id_pelicula = peliculas_repository.insertar_pelicula(datos)

    pelicula = datos.copy()
    pelicula["id"] = id_pelicula

    return pelicula