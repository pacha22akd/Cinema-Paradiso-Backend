import src.repositories.compras as compras_repositories
import src.validators.compras as compras_validator
from src.utils.errores import devolver_error

def agregar_servicio_a_compra(compra_id, servicio_id, cantidad, usuario_id):

    servicio_id, cantidad = compras_validator.validar_servicio_en_compra(servicio_id, cantidad)

    compra = compras_repositories.buscar_compra(compra_id)

    if compra is None:
        return devolver_error("No existe la compra", 404)
    
    if compra["usuario_id"] != usuario_id:
        return devolver_error("La compra no pertenece al usuario", 403)

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
    }, 201


def pagar_compra(id, usuario_id):

    compra = compras_repositories.buscar_compra(id)

    if compra is None:
        return devolver_error("No existe la compra", 404)

    if compra["usuario_id"] != usuario_id:
        return devolver_error("La compra no pertenece al usuario", 403)

    if compra["estado"] != "pendiente":
        return devolver_error("La compra no está pendiente de pago", 409)

    numero_factura = "FAC-" + str(id).zfill(6)  #.zfill llena con ceros a la izquierda. "FAC-" se inserta adelante.

    compras_repositories.pagar_compra(id, numero_factura)

    return {"compra_id": id, "estado": "pagada", "numero_factura": numero_factura}
