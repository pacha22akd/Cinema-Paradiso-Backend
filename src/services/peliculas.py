import src.repositories.peliculas as peliculas_repository


def borrar_pelicula(id_pelicula):

    resultado = peliculas_repository.eliminar_pelicula(id_pelicula)

    return resultado