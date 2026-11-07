from repositories import servicios

def listar_servicios_adicionales(categoria):
    return servicios.obtener_servicios_adicionales(categoria)
