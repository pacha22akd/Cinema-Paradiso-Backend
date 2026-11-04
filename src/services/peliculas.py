from src.repositories import peliculas as periculas_rep


def listar_peliculas(titulo=None, genero=None) -> list:

    peliculas = periculas_rep.obtener_peliculas(titulo, genero)

    return peliculas