def validar_precio(precio):

    if precio is not None and precio <= 0:
        raise ValueError("El precio debe ser mayor a 0")


def validar_stock(stock):

    if stock is not None and stock < 0:
        raise ValueError("El stock no puede ser negativo")


def validar_alta_servicio(nombre, precio, stock):

    if not nombre or not nombre.strip():
        raise ValueError("El nombre es obligatorio")

    if precio is None:
        raise ValueError("El precio es obligatorio")

    validar_precio(precio)
    validar_stock(stock)


def validar_modificacion_servicio(id, nombre, precio, stock):

    if id is None or id <= 0:
        raise ValueError("El id debe ser mayor a 0")

    if nombre is not None and not nombre.strip():
        raise ValueError("El nombre no puede estar vacío")

    validar_precio(precio)
    validar_stock(stock)