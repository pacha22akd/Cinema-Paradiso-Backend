from flask import Blueprint, request, jsonify
from services import servicios_services
from src.utils.errores import devolver_error

servicios_bp = Blueprint("servicios", __name__)

@servicios_bp.route('/admin/servicios', methods = ['GET'])
def obtener_servicios():

    try:
        servicios = servicios_services.listar_servicios()
        if not servicios:
            return devolver_error("No hay servicios actualmente", 404)

        return jsonify(servicios), 200
    
    except Exception as e:
        return devolver_error(str(e), 500)


@servicios_bp.route('/admin/servicios', methods = ['POST'])
def nuevo_servicio():

    datos = request.get_json()

    try:
        servicio = servicios_services.dar_de_alta_servicio(
            datos.get("nombre"),
            datos.get("descripcion"),
            datos.get("categoria"),
            datos.get("precio"),
            datos.get("stock"),
            datos.get("imagen_url"),
        )
        return jsonify({"message": "Se creó el servicio correspondiente"}), 200

    except ValueError as e:
        return devolver_error(str(e), 400)

    except Exception as e:
        return devolver_error(str(e), 500)

@servicios_bp.route('/admin/servicios/<int:id>', methods = ['PATCH'])
def patch_servicio(id):

    datos = request.get_json()

    try:
        existe = servicios_services.alterar_servicio(
        id,
        datos.get("nombre"),
        datos.get("descripcion"),
        datos.get("categoria"),
        datos.get("precio"),
        datos.get("stock"),
        datos.get("imagen_url"),
        )
    
        if existe == False:
            return devolver_error("No existe el servicio buscado", 404)

        return jsonify({"message": "Servicio modificado con éxito."}), 200
    
    except Exception as e:
        return devolver_error(str(e), 500)


@servicios_bp.route("/admin/servicios/<int:id>", methods=["DELETE"])
def delete_servicio(id):

    try:
        existe = servicios_services.quitar_servicio(id)

        if existe == False:
            return devolver_error("No existe el servicio buscado.", 404)

        return jsonify({"message": "Servicio eliminado con éxito."}), 200

    except Exception as e:
        return devolver_error(str(e), 500)
