from flask import Blueprint, jsonify, request, g
from src.services import compras
from src.utils.errores import devolver_error
from src.utils.auth import requiere_auth
from src.validators.compras import validar_id_compra

compras_bp = Blueprint('compras', __name__)

@compras_bp.route('/compras', methods=['POST'])
@requiere_auth
def crear_compra():
    try:
        datos = request.get_json(silent=True)

        if not isinstance(datos, dict):
            return devolver_error("No se recibieron los datos de la compra", 400)

        usuario_id = g.usuario_id
        funcion_id = datos.get('funcion_id')
        butaca_ids = datos.get('butaca_ids')

        resultado = compras.realizar_proceso_compra(usuario_id, funcion_id, butaca_ids)

        if "error" in resultado:
            return devolver_error(resultado["error"], resultado["status"])

        return jsonify({
            "mensaje": "Compra realizada con éxito",
            "compra_id": resultado["compra_id"],
            "codigo": resultado["codigo_compra"],
            "monto_total": resultado["monto_total"]
        }), 201

    except Exception:
        return devolver_error("No se pudo procesar la compra", 500)
    
    
@compras_bp.route("/compras/<int:id>", methods=["GET"])
@requiere_auth
def get_compra(id):
    try:
        resultado = compras.obtener_compra(id, g.usuario_id)

        if "error" in resultado:
            return devolver_error(resultado["error"], resultado["status"])

        return jsonify(resultado), 200

    except Exception:
        return devolver_error("No se pudo obtener la compra", 500)


@compras_bp.route('/compras', methods=['GET'])
@requiere_auth
def listar_compras():
    try:
        resultado = compras.listar_compras_usuario(
            usuario_id  = g.usuario_id,  
            estado      = request.args.get("estado"),
            fecha_desde = request.args.get("fecha_desde"),
            fecha_hasta = request.args.get("fecha_hasta"),
            page        = request.args.get("page"),
            per_page    = request.args.get("per_page"),
        )

        return jsonify({
            "mensaje": "Historial de compras obtenido exitosamente",
            **resultado,
        }), 200

    except ValueError as e:
        return devolver_error(str(e), 400)

    except PermissionError as e:
        return devolver_error(str(e), 401)

    except Exception:
        return devolver_error("No se pudo obtener el historial de compras", 500)

@compras_bp.route("/compras/<int:id_compra>/cancelar", methods=["PATCH"])
@requiere_auth
def cancelar_compra_por_id(id_compra):
    valido, error = validar_id_compra(id_compra)
    if not valido:
        return jsonify({"error": error}), 400
    datos = request.get_json(silent=True) or {}
    motivo = datos.get("motivo")
    respuesta, codigo = compras.cancelar_compra(id_compra, g.usuario_id, motivo)
    return jsonify(respuesta), codigo

@compras_bp.route("/compras/<int:id>/servicios", methods=["POST"])
@requiere_auth
def post_servicio_a_compra(id):
    try:
        datos = request.get_json(silent=True)

        if not isinstance(datos, dict):
            return devolver_error("No se recibieron los datos del servicio", 400)

        return compras.agregar_servicio_a_compra(
            id,
            datos.get("servicio_id"),
            datos.get("cantidad"),
            g.usuario_id
        )

    except ValueError as e:
        return devolver_error(str(e), 400)

    except Exception:
        return devolver_error("Error interno al agregar el servicio", 500)

@compras_bp.route("/compras/<int:id>/pagar", methods=["POST"])
@requiere_auth
def post_pagar_compra(id):

    try:
        return compras.pagar_compra(id, g.usuario_id)

    except Exception as e:
        return devolver_error(str(e), 500)

@compras_bp.route("/compras/<int:id>/reenviar_mail", methods=["POST"])
@requiere_auth
def post_reenviar_mail(id):
    try:
        return compras.reenviar_mail_compra(id, g.usuario_id)

    except Exception as e:
        return devolver_error(str(e), 500)