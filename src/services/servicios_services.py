from repositories import servicios_repository
def listar_servicios():
    return servicios_repository.obtener_servicios()


def dar_de_alta_servicio(nombre, descripcion, categoria, precio, stock, imagen_url):

    if precio is not None and precio <= 0:
        raise ValueError("El precio debe ser mayor a 0.")

    if stock is not None and stock <= 0:
        raise ValueError("El stock debe ser mayor a 0.")

    return servicios_repository.agregar_servicio(nombre, descripcion, categoria, precio, stock, imagen_url)

def alterar_servicio(id, nombre, descripcion, categoria, precio, stock, imagen_url):
    if id is not None and id <= 0:
        raise ValueError("El id debe ser mayor a 0.")

    if nombre is None:
        raise ValueError("El nombre no puede estar vacío.")

    if precio is not None and precio <= 0:
        raise ValueError("El precio debe ser mayor a 0.")
    
    if stock is not None and stock <= 0:
        raise ValueError("El stock debe ser mayor a 0.")

    return servicios_repository.modificar_servicio(id, nombre, descripcion, categoria, precio, stock, imagen_url)

def quitar_servicio(id):
    return servicios_repository.eliminar_servicio(id)