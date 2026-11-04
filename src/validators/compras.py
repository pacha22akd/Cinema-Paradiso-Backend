
def validar_id_compra(id_compra):

    if type(id_compra) is not int or id_compra <= 0:
        return False, "El ID de la compra debe ser un entero positivo"

    return True, None
