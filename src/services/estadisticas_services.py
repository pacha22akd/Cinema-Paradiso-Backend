from repositories import estadisticas_repository

def consultar_cancelaciones():

    motivos = estadisticas_repository.obtener_cancelaciones()

    total = 0
    for fila in motivos:
        total += fila["cantidad"]

    return {"total_canceladas": total, "motivos": motivos}