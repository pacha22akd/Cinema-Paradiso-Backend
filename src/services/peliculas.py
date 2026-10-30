from src.repositories.peliculas import obtener_pelicula_por_id, obtener_peliculas_cartelera

def buscar_pelicula_por_id(pelicula_id):
    return obtener_pelicula_por_id(pelicula_id)

def listar_peliculas(genero=None, titulo=None):
    return obtener_peliculas_cartelera(genero, titulo)