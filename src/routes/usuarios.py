from flask import Blueprint, request, jsonify, g

import src.validators.usuarios as usuarios_validator
import src.services.usuarios as usuarios_service
import src.utils.errores as errores
import src.utils.auth as auth
from src.services import usuarios 
from src.utils.errores import devolver_error


usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/usuarios/perfil", methods=["PATCH"])
@auth.requiere_auth
def modificar_perfil():

    id_usuario = g.usuario_actual["id"]

    datos = request.get_json(silent=True)

    es_valido, perfil, descripcion_error = usuarios_validator.validar_modificacion_perfil(datos)

    if not es_valido:
        return errores.devolver_error(descripcion_error, 400)

    try:
        perfil_actualizado = usuarios_service.modificar_perfil(
            id_usuario, perfil
        )

        if perfil_actualizado is None:
            return errores.devolver_error("El usuario no existe", 404)

        if perfil_actualizado == "email_duplicado":
            return errores.devolver_error("El email ya se encuentra registrado", 409)

        return jsonify(perfil_actualizado), 200

    except Exception:
        return errores.devolver_error("No se pudo modificar el perfil", 500)


@usuarios_bp.route("/usuarios", methods=["POST"])
def post_usuario():
    datos = request.get_json()

    if not datos:
        return devolver_error("No se enviaron datos", 400)

    try:
        resultado = usuarios.registrar_usuario(datos)

        if "error" in resultado:
            return devolver_error(resultado["error"], resultado["status"])

        return jsonify({
            'mensaje': 'Usuario registrado exitosamente',
            'usuario': resultado
        }), 201

    except Exception as e:
        return devolver_error(f"Error inesperado: {str(e)}", 500)

#-----------------------------------

@usuarios_bp.route('/usuarios/perfil', methods=['GET'])
@auth.requiere_auth
def get_perfil():
    try:
        resultado = usuarios_service.obtener_perfil_usuario(g.usuario_id)

        return jsonify({
            "mensaje": "Perfil obtenido exitosamente",
            **resultado
        }), 200

    except PermissionError as e:
        return errores.devolver_error(str(e), 401)
    except LookupError as e:
        return errores.devolver_error(str(e), 404)
    except Exception:
        current_app.logger.exception("Error al obtener el perfil del usuario")
        return errores.devolver_error(
            "Ocurrió un error inesperado al obtener el perfil",
            500
        )

