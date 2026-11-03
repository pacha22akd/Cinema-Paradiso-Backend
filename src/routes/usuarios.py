from flask import Blueprint, request, jsonify
from src.services import usuarios 
from src.utils.errores import devolver_error

usuarios_bp = Blueprint('usuarios', __name__)

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