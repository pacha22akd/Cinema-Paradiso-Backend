from datetime import datetime
from src.repositories.compras import cancelar_compra_en_bd
from src.repositories.funciones import obtener_funcion_por_id, obtener_butacas_por_funcion
from src.repositories.compras import registrar_compra_transaccion
from src.validators.compras import validar_datos_compra, validar_servicio_en_compra
from src.repositories import compras
from src.utils.errores import devolver_error

def realizar_proceso_compra(usuario_id, funcion_id, butaca_ids):
   
    error = validar_datos_compra(usuario_id, funcion_id, butaca_ids)
    if error:
        return error

    funcion = obtener_funcion_por_id(funcion_id)
    if not funcion:
        return {"error": "La función solicitada no existe", "status": 404}  

    if funcion["estado"] != "programada":
        return {"error": "La función no está disponible para la venta", "status": 409}
    
    if funcion["ya_empezo"]:
        return {"error": "La función ya comenzó o finalizó", "status": 409}
    
    butacas_sala = obtener_butacas_por_funcion(funcion_id, funcion["sala_id"])
    if butacas_sala is None:
        return {"error": "No se pudo verificar la disponibilidad de las butacas", "status": 500}

    for b_id in butaca_ids:
        butaca_encontrada = None
        for butaca in butacas_sala:
            if butaca["butaca_id"] == b_id:
                butaca_encontrada = butaca

        if butaca_encontrada is None:
            return {"error": f"La butaca {b_id} no pertenece a la sala de esta función", "status": 400}

        if butaca_encontrada["estado_disponibilidad"] == "ocupada":
            return {"error": f"La butaca {b_id} ya está ocupada", "status": 409}

    precio_unitario = funcion["precio_base"]
    resultado = registrar_compra_transaccion(usuario_id, funcion_id, butaca_ids, precio_unitario)

    if resultado == "butaca_ocupada":
        return{"error": "Una de las butacas ya fue ocupada por otra compra", "status": 409}

    if resultado is None:
        return {"error": "No se pudo registrar la compra", "status": 500}

    return resultado

def obtener_compra(id_compra, usuario_id):
    compra = compras.obtener_compra_por_id(id_compra, usuario_id)

    if compra is None:
        return {"error": "No existe la compra buscada", "status": 404}

    compra["fecha_compra"] = str(compra["fecha_compra"]) if compra["fecha_compra"] else None
    compra["fecha_hora_inicio"] = str(compra["fecha_hora_inicio"]) if compra["fecha_hora_inicio"] else None
    compra["fecha_hora_fin"] = str(compra["fecha_hora_fin"]) if compra["fecha_hora_fin"] else None

    return compra

ESTADOS_VALIDOS = {"pendiente", "pagada", "cancelada", "usada"}

def _parse_int(valor, campo, default=None):
    if valor is None or valor == "":
        return default
    try:
        return int(valor)
    except (TypeError, ValueError):
        raise ValueError(f"El parámetro '{campo}' debe ser un número entero")


def _parse_datetime(valor, campo):
    if not valor:
        return None
    try:
        return datetime.fromisoformat(valor)
    except ValueError:
        raise ValueError(
            f"El parámetro '{campo}' debe tener formato ISO 8601 "
            f"(YYYY-MM-DD o YYYY-MM-DDTHH:MM:SS)"
        )

def listar_compras_usuario(usuario_id, estado=None, fecha_desde=None,
                           fecha_hasta=None, page=None, per_page=None):
    
    if not usuario_id:
        raise PermissionError("Usuario no autenticado")

    # Parsear
    page        = _parse_int(page, "page", default=1)
    per_page    = _parse_int(per_page, "per_page", default=10)
    fecha_desde = _parse_datetime(fecha_desde, "fecha_desde")
    fecha_hasta = _parse_datetime(fecha_hasta, "fecha_hasta")

    if page < 1:
        raise ValueError("'page' debe ser mayor a 0")
    if per_page < 1 or per_page > 100:
        raise ValueError("'per_page' debe estar entre 1 y 100")
    if estado and estado not in ESTADOS_VALIDOS:
        raise ValueError(
            f"'estado' inválido. Permitidos: {', '.join(sorted(ESTADOS_VALIDOS))}"
        )
    if fecha_desde and fecha_hasta and fecha_desde > fecha_hasta:
        raise ValueError("'fecha_desde' no puede ser mayor que 'fecha_hasta'")

    filtros = {
        "estado":      estado,
        "fecha_desde": fecha_desde,
        "fecha_hasta": fecha_hasta,
    }
    offset = (page - 1) * per_page
    filas, total = compras.obtener_compras_usuario(usuario_id, filtros, offset, per_page)

    #Formatear respuesta
    data = []
    for c in filas:
        fecha_f = c.fecha_hora_inicio.strftime("%Y-%m-%d") if c.fecha_hora_inicio else None
        hora_f  = c.fecha_hora_inicio.strftime("%H:%M")    if c.fecha_hora_inicio else None
        fecha_c = c.fecha_compra.strftime("%Y-%m-%d %H:%M") if c.fecha_compra else None

        data.append({
            "id": c.id,
            "codigo": c.codigo,
            "total": float(c.total),
            "estado": c.estado,
            "fecha_compra": fecha_c,
            "funcion": {
                "fecha": fecha_f,
                "hora_inicio": hora_f,
                "pelicula": c.pelicula_titulo,
                "poster": c.poster_url,
                "sala": c.sala_nombre,
                "local": c.local_nombre,
            },
            "cantidad_entradas": c.cantidad_entradas,
            "cantidad_servicios": c.cantidad_servicios,
        })

    return {
        "data": data,
        "meta": {
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page if per_page else 0,
        },
    }

def cancelar_compra(id_compra, id_usuario, id_motivo):
    
    resultado = cancelar_compra_en_bd(id_compra, id_usuario, id_motivo)

    if resultado == "no_existe":
        return {"error": "Compra no encontrada"}, 404

    if resultado == "no_cancelable":
        return {"error": "La compra no se puede cancelar"}, 409

    if resultado == "fuera_de_plazo":
        return {"error": "Solo se puede cancelar hasta 2 horas antes de la función"}, 409

    return {"mensaje": "Compra cancelada correctamente"}, 200


def agregar_servicio_a_compra(compra_id, servicio_id, cantidad, usuario_id):

    servicio_id, cantidad = validar_servicio_en_compra(servicio_id, cantidad)

    compra = compras.buscar_compra(compra_id)

    if compra is None:
        return devolver_error("No existe la compra", 404)
    
    if compra["usuario_id"] != usuario_id:
        return devolver_error("La compra no pertenece al usuario", 403)

    if compra["estado"] != "pendiente":
        return devolver_error("Solo se pueden agregar servicios a una compra pendiente", 409)

    resultado = compras.agregar_servicio_a_compra(compra_id, servicio_id, cantidad)

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

    compra = compras.buscar_compra(id)

    if compra is None:
        return devolver_error("No existe la compra", 404)

    if compra["usuario_id"] != usuario_id:
        return devolver_error("La compra no pertenece al usuario", 403)

    if compra["estado"] != "pendiente":
        return devolver_error("La compra no está pendiente de pago", 409)

    numero_factura = "FAC-" + str(id).zfill(6)  #.zfill llena con ceros a la izquierda. "FAC-" se inserta adelante.

    compras.pagar_compra(id, numero_factura)

    return {"compra_id": id, "estado": "pagada", "numero_factura": numero_factura}

