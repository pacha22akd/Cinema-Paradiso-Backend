from src.repositories import servicios
from src.validators.servicios import validar_alta_servicio, validar_modificacion_servicio

def listar_servicios():
    return servicios.obtener_servicios()


def dar_de_alta_servicio(nombre, descripcion, categoria, precio, stock, imagen_url):

    validar_alta_servicio(nombre, precio, stock)
    servicios.agregar_servicio(nombre, descripcion, categoria, precio, stock, imagen_url)

def alterar_servicio(id, nombre, descripcion, categoria, precio, stock, imagen_url):

    validar_modificacion_servicio(id, nombre, precio, stock)

    actual = servicios.obtener_servicio(id)

    if actual is None:
        return False
    
    if nombre is None:
        nombre = actual["nombre"]
    if descripcion is None:
        descripcion = actual["descripcion"]
    if categoria is None:
        categoria = actual["categoria"]
    if precio is None:
        precio = actual["precio"]
    if stock is None:
        stock = actual["stock"]
    if imagen_url is None:
        imagen_url = actual["imagen_url"]

    servicios.modificar_servicio(id, nombre, descripcion, categoria, precio, stock, imagen_url)
    return True

def quitar_servicio(id):
    return servicios.eliminar_servicio(id)

def listar_servicios_adicionales(categoria):
    return servicios.obtener_servicios_adicionales(categoria)