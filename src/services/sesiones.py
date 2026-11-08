from datetime import datetime, timedelta, timezone

import jwt
from flask import current_app
from werkzeug.security import check_password_hash

from src.repositories import usuarios
from src.utils.errores import devolver_error


def iniciar_sesion(email, password):
    if not email or not password:
        return devolver_error("Email y contraseña son obligatorios", 400)

    usuario = usuarios.obtener_usuario_por_email(email)
    if not usuario:
        return devolver_error("Credenciales inválidas", 401)

    if not check_password_hash(usuario.password_hash, password):
        return devolver_error("Credenciales inválidas", 401)

    token = jwt.encode(
        {
            "usuario_id": usuario.id,
            "rol": usuario.rol,
            "exp": datetime.now(timezone.utc) + timedelta(hours=8),
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256",
    )

    return {
        "usuario": {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "email": usuario.email,
            "rol": usuario.rol,
        },
        "token": token,
    }, 200


