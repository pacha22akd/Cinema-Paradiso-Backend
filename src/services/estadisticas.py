from repositories import estadisticas

def consultar_cancelaciones():

    motivos = estadisticas.obtener_cancelaciones()

    total = 0
    for fila in motivos:
        total += fila["cantidad"]

    return {"total_canceladas": total, "motivos": motivos}
