from datetime import datetime, timedelta, timezone
import jwt
from flask import current_app
from werkzeug.security import check_password_hash
from src.repositories.usuarios import obtener_usuario_por_email


def iniciar_sesion(email, password):
    if not email or not password:
        raise ValueError("Email y contraseña son obligatorios")

    usuario = obtener_usuario_por_email(email)
    if not usuario:
        raise PermissionError("Credenciales inválidas")

    if not check_password_hash(usuario.password_hash, password):
        raise PermissionError("Credenciales inválidas")

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
    }


