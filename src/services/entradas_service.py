from repositories import entradas_repository
from src.utils.errores import devolver_error

def consultar_entrada(id):

    entrada = entradas_repository.obtener_entrada(id)

    if entrada is None:
        return devolver_error("No existe la entrada buscada", 404)

    entrada["fecha_hora_inicio"] = str(entrada["fecha_hora_inicio"])

    return entrada, 200
