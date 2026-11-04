<<<<<<< HEAD
from flask import Blueprint, request, jsonify
from src.services.compras import realizar_proceso_compra
=======
from flask import Blueprint, jsonify
from src.services import compras
>>>>>>> feature/endpoints-POST-usuarios-GET-compras/id
from src.utils.errores import devolver_error

compras_bp = Blueprint('compras', __name__)

<<<<<<< HEAD
@compras_bp.route('/compras', methods=['POST'])
def crear_compra():
    try:
        datos = request.get_json(silent=True)
        if not isinstance(datos, dict):
            return devolver_error("Debe proporcionar un cuerpo JSON válido", 400)

        usuario_id = datos.get('usuario_id')
        funcion_id = datos.get('funcion_id')
        butaca_ids = datos.get('butaca_ids')

        resultado = realizar_proceso_compra(usuario_id, funcion_id, butaca_ids)

        if "error" in resultado:
            return devolver_error(resultado["error"], resultado["status"])  

        return jsonify({
            "mensaje": "Compra realizada con éxito",
            "compra_id": resultado["compra_id"],
            "codigo": resultado["codigo_compra"],
            "monto_total": resultado["monto_total"]
        }), 201

    except Exception as e:
        return devolver_error(f"Error inesperado al procesar la compra: {str(e)}", 500)
=======
@compras_bp.route("/compras/<int:id>", methods=["GET"])
def get_compra(id):
    try:
        resultado = compras.obtener_compra(id)

        if "error" in resultado:
            return devolver_error(resultado["error"], resultado["status"])

        return jsonify(resultado), 200

    except Exception as e:
        return devolver_error(str(e), 500)
>>>>>>> feature/endpoints-POST-usuarios-GET-compras/id
