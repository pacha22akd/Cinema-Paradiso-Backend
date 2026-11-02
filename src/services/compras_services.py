from repositories import compras_repositories
from errores import devolver_error

def agregar_servicio_a_compra(compra_id, servicio_id, cantidad):

    if servicio_id is None or servicio_id <= 0:
        raise ValueError("El id del servicio debe ser mayor a 0")

    if cantidad is None or cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor a 0")

    compra = compras_repositories.buscar_compra(compra_id)

    if compra is None:
        return devolver_error("No existe la compra", 404)

    if compra["estado"] != "pendiente":
        return devolver_error("Solo se pueden agregar servicios a una compra pendiente", 409)

    resultado = compras_repositories.agregar_servicio_a_compra(compra_id, servicio_id, cantidad)

    if resultado == "no_existe":
        return devolver_error("No existe el servicio", 404)

    if resultado == "sin_stock":
        return devolver_error("Stock insuficiente", 409)

    return {
        "compra_id": compra_id,
        "servicio_id": servicio_id,
        "cantidad": cantidad,
        "precio_unitario": resultado["precio_unitario"],
        "subtotal": resultado["subtotal"],
    }


def pagar_compra(id):

    compra = compras_repositories.buscar_compra(id)

    if compra is None:
        return devolver_error("No existe la compra", 404)

    if compra["estado"] != "pendiente":
        return devolver_error("La compra no está pendiente de pago", 409)

    numero_factura = "FAC-" + str(id).zfill(6)  #.zfill llena con ceros a la izquierda. "FAC-" se inserta adelante.

    compras_repositories.pagar_compra(id, numero_factura)

    return {"compra_id": id, "estado": "pagada", "numero_factura": numero_factura}