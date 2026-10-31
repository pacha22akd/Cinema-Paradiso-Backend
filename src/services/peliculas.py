import os
import requests
from dotenv import load_dotenv

load_dotenv()


def buscar_pelicula_externa(titulo, anio=None):

    api_key = os.getenv("OMDB_API_KEY")

    if not api_key:
        raise RuntimeError("No se configuro la API Key de OMDb")

    url = "https://www.omdbapi.com/"

    parametros = {
        "apikey": api_key,
        "t": titulo,
        "type": "movie",
        "plot": "full"
    }

    if anio is not None:
        parametros["y"] = anio

    respuesta = requests.get(url, params=parametros, timeout=10)

    respuesta.raise_for_status()

    datos = respuesta.json()

    if datos.get("Response") == "False":

        error = datos.get("Error", "")

        if "not found" in error.lower():
            return None

        raise RuntimeError("Error al consultar OMDb")

    if datos.get("Response") != "True":
        raise RuntimeError("Respuesta inesperada de OMDb")

    duracion = datos.get("Runtime")
    anio_estreno = datos.get("Year")

    pelicula = {
        "api_id": datos.get("imdbID"),
        "titulo": datos.get("Title"),
        "sinopsis": datos.get("Plot"),
        "poster_url": datos.get("Poster"),
        "duracion_min": None,
        "clasificacion": datos.get("Rated"),
        "genero": datos.get("Genre"),
        "anio_estreno": None
    }

    if duracion and duracion != "N/A":
        minutos = duracion.split()[0]

        if minutos.isdigit():
            pelicula["duracion_min"] = int(minutos)

    if anio_estreno and anio_estreno.isdigit():
        pelicula["anio_estreno"] = int(anio_estreno)

    for campo, valor in pelicula.items():
        if valor == "N/A":
            pelicula[campo] = None

    return pelicula