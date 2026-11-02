from sqlalchemy import text
from src.utils.config import db

def buscar_compra(id):

    query = "SELECT id, estado FROM compras WHERE id = :id"

    valores = {"id": id}

    conn = db.connect()
    resultado = conn.execute(text(query), valores)

    compras = []
    for fila in resultado:
        compra = {"id": fila.id, "estado": fila.estado}
        compras.append(compra)

    conn.close()

    if len(compras) == 0:
        return None

    return compras[0]


def agregar_servicio_a_compra(compra_id, servicio_id, cantidad):

    select_query = """ SELECT precio, stock FROM servicios WHERE id = :servicio_id """
    insert_query = """ INSERT INTO compra_servicios (compra_id, servicio_id, cantidad, precio_unitario, subtotal)
    VALUES (:compra_id, :servicio_id, :cantidad, :precio_unitario, :subtotal) """
    stock_query = "UPDATE servicios SET stock = stock - :cantidad WHERE id = :servicio_id"
    total_query = "UPDATE compras SET total = total + :subtotal WHERE id = :compra_id"

    conn = db.connect()

    valor = {"servicio_id": servicio_id}

    resultado = conn.execute(text(select_query), valor)

    servicios = []
    for fila in resultado:
        servicio = {"precio": fila.precio, "stock": fila.stock}
        servicios.append(servicio)

    if len(servicios) == 0:
        conn.close()
        return "no_existe"

    precio = servicios[0]["precio"]
    stock = servicios[0]["stock"]

    if stock is not None and stock < cantidad:
        conn.close()
        return "sin_stock"

    subtotal = precio * cantidad

    valores = {
        "compra_id": compra_id,
        "servicio_id": servicio_id,
        "cantidad": cantidad,
        "precio_unitario": precio,
        "subtotal": subtotal,
    }

    conn.execute(text(insert_query), valores)
    conn.execute(text(stock_query), valores)
    conn.execute(text(total_query), valores)
    conn.commit()
    conn.close()

    return {"precio_unitario": precio, "subtotal": subtotal}


def pagar_compra(id, numero_factura):

    compra_query = "UPDATE compras SET estado = 'pagada', numero_factura = :numero_factura WHERE id = :id"
    entradas_query = "UPDATE entradas SET estado = 'valida' WHERE compra_id = :id AND estado = 'pendiente'"

    valores = {"id": id, "numero_factura": numero_factura}

    conn = db.connect()
    conn.execute(text(compra_query), valores)
    conn.execute(text(entradas_query), valores)
    conn.commit()
    conn.close()
