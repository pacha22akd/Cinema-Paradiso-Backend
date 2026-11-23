from functools import wraps
from flask import request, g, current_app
import jwt

from src.utils.errores import devolver_error
from src.repositories.usuarios import obtener_perfil_usuario


def requiere_auth(f):

    @wraps(f)
    def wrapper(*args, **kwargs):

        auth_header = request.headers.get("Authorization", "")

        tipo, espacio, token = auth_header.partition(" ")

        if tipo.lower() != "bearer" or not token.strip():
            return devolver_error("Token no proporcionado", 401)

        try:
            payload = jwt.decode(
                token.strip(),
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"],
                options={"require": ["usuario_id", "rol", "exp"]}
            )

            usuario_id = payload["usuario_id"]
            rol_token = payload["rol"]

            if type(usuario_id) is not int or usuario_id <= 0:
                return devolver_error("Token inválido", 401)

            if not isinstance(rol_token, str) or rol_token.strip() == "":
                return devolver_error("Token inválido", 401)

        except jwt.ExpiredSignatureError:
            return devolver_error("Token expirado", 401)

        except (jwt.InvalidTokenError, ValueError, TypeError):
            return devolver_error("Token inválido", 401)

        try:
            usuario = obtener_perfil_usuario(usuario_id)

        except Exception:
            return devolver_error("No se pudo verificar el usuario", 500)

        if usuario is None:
            return devolver_error("El usuario del token no existe", 401)

        g.usuario_id = usuario.id
        g.rol = usuario.rol

        return f(*args, **kwargs)

    return wrapper


def requiere_rol(rol_requerido):

    def decorar(f):

        @wraps(f)
        def wrapper(*args, **kwargs):

            if g.rol != rol_requerido:
                return devolver_error("No tiene permisos para acceder", 403)

            return f(*args, **kwargs)

        return requiere_auth(wrapper)

    return decorar