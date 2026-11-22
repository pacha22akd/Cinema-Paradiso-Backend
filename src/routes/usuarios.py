from flask import Blueprint, request, jsonify, g, current_app
import src.validators.usuarios as usuarios_validator
import src.services.usuarios as usuarios_service
import src.utils.auth as auth
from src.utils.errores import devolver_error

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/usuarios/perfil", methods=["PATCH"])
@auth.requiere_auth
def modificar_perfil():

    id_usuario = g.usuario_id

    datos = request.get_json(silent=True)

    es_valido, perfil, descripcion_error = usuarios_validator.validar_modificacion_perfil(datos)

    if not es_valido:
        return devolver_error(descripcion_error, 400)

    try:
        perfil_actualizado = usuarios_service.modificar_perfil(
            id_usuario, perfil
        )

        if perfil_actualizado is None:
            return devolver_error("El usuario no existe", 404)

        if perfil_actualizado == "email_duplicado":
            return devolver_error("El email ya se encuentra registrado", 409)

        if perfil_actualizado == "campo_no_permitido":
            return devolver_error("Campo no permitido", 400)

        if perfil_actualizado == "error_bd":
            return devolver_error("No se pudo modificar el perfil", 500)

        return jsonify(perfil_actualizado), 200

    except Exception:
        return devolver_error("No se pudo modificar el perfil", 500)


@usuarios_bp.route("/usuarios", methods=["POST"])
def post_usuario():
    datos = request.get_json()
    try:
        resultado = usuarios_service.registrar_usuario(datos)

        return jsonify({'mensaje': 'Usuario registrado exitosamente','usuario': resultado}), 201

    except ValueError as e:
        mensaje = str(e)
        status = 409 if "email ya está registrado" in mensaje else 400
        return devolver_error(mensaje, status)

    except Exception as e:
        return devolver_error(f"Error inesperado: {str(e)}", 500)


@usuarios_bp.route('/usuarios/perfil', methods=['GET'])
@auth.requiere_auth
def get_perfil():
    try:
        resultado = usuarios_service.obtener_perfil_usuario(g.usuario_id)

        return jsonify({"mensaje": "Perfil obtenido exitosamente", "data": resultado}), 200

    except PermissionError as e:
        return devolver_error(str(e), 401)
    except LookupError as e:
        return devolver_error(str(e), 404)
    except Exception:
        current_app.logger.exception("Error al obtener el perfil del usuario")
        return devolver_error("Ocurrió un error inesperado al obtener el perfil", 500)

