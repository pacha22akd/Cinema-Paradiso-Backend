def crear_respuesta_error(codigo: str, mensaje: str, descripcion: str)->dict:
    """Devuelve la respuesta estándar de un error"""
    return {
        "errors": [{
            "code": codigo,
            "message": mensaje,
            "level": "error",
            "description": descripcion
        }]
    }

def devolver_error(descripcion: str, status_code: int)->dict:
    """Devuelve la respuesta del error (con la descripción recibida), la cual depende del status_code enviado"""
    if (status_code == 400):
        return crear_respuesta_error("ERROR_VALIDACION", "El cuerpo de la solicitud es inválido", descripcion), status_code
    elif (status_code == 401):
        return crear_respuesta_error("NO_AUTENTICADO", "Autenticación requerida", descripcion), status_code
    elif (status_code == 403):
        return crear_respuesta_error("ACCESO_DENEGADO", "Acceso denegado", descripcion), status_code
    elif (status_code == 404):
        return crear_respuesta_error("NO_ENCONTRADO", "Recurso no encontrado", descripcion), status_code
    elif (status_code == 409):
        return crear_respuesta_error("CONFLICTO", "Conflicto de negocio", descripcion), status_code
    elif (status_code == 500):
        return crear_respuesta_error("ERROR_INTERNO", "Error interno del servidor", descripcion), status_code
