
from src.repositories.compras import cancelar_compra_en_bd


def cancelar_compra(id_compra, id_usuario):

    resultado = cancelar_compra_en_bd(id_compra, id_usuario)

    if resultado == "no_existe":
        return {"error": "Compra no encontrada"}, 404

    if resultado == "no_cancelable":
        return {"error": "La compra no se puede cancelar"}, 409

    return {"mensaje": "Compra cancelada correctamente"}, 200

