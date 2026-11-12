from datetime import date
from src.repositories.entradas import buscar_entrada_por_qr, marcar_entrada_usada, obtener_entrada
from src.validators.entradas import validar_datos_qr
from src.utils.errores import devolver_error

def validar_qr(codigo):

    validar_datos_qr(codigo)

    entrada = buscar_entrada_por_qr(codigo)

    if entrada is None:
        return {"valida": False, "motivo": "El código QR no existe", "estado_entrada": None}

    estado = entrada["estado"]
    

    if estado == "pendiente":
        return {"valida": False, "motivo": "La compra todavía no fue pagada", "estado_entrada": estado}

    if estado == "usada":
        return {"valida": False, "motivo": "La entrada ya fue utilizada", "estado_entrada": estado}

    if estado == "cancelada":
        return {"valida": False, "motivo": "La entrada fue cancelada", "estado_entrada": estado}

    if entrada["estado_funcion"] == "cancelada":
        return {"valida": False, "motivo": "La función está cancelada.", "estado_entrada": estado}

    if entrada["estado_funcion"] == "finalizada":
        return {"valida": False, "motivo": "La función está finalizada.", "estado_entrada": estado}

    if entrada["fecha_hora_inicio"].date() != date.today():
        return {"valida": False, "motivo": "La entrada no es para el día de hoy", "estado_entrada": estado}

    if entrada["fecha_hora_fin"].date() < date.today():
        return {"valida": False, "motivo": "La función ya finalizó", "estado_entrada": estado}
    
    marcada = marcar_entrada_usada(entrada["id"])

    if not marcada:
        return {"valida": False, "motivo": "La entrada ya fue utilizada", "estado_entrada": "usada"}

    hora_formateada = entrada["fecha_hora_inicio"].strftime("%H:%M") if entrada["fecha_hora_inicio"] else ""
    
    return {
        "valida": True, 
        "motivo": "Entrada válida", 
        "estado_entrada": "usada",
        "detalles": {
            "pelicula": entrada["pelicula"],
            "sala": entrada["sala"],
            "hora": hora_formateada,
            "butaca": f"{entrada['fila']}{entrada['numero']}"
        }
    }


def consultar_entrada(id, usuario_id):

    entrada = obtener_entrada(id, usuario_id)

    if entrada is None:
        return devolver_error("No existe la entrada buscada", 404)

    entrada["fecha_hora_inicio"] = str(entrada["fecha_hora_inicio"])

    return entrada, 200
