from flask import Blueprint, jsonify
from src.services.locales import obtener_locales_service
from src.utils.errores import devolver_error
from src.utils.auth import requiere_rol
locales_bp = Blueprint('locales_bp', __name__)

@locales_bp.route('/admin/locales', methods=['GET'])
@requiere_rol("administrador")
def obtener_locales():
    
    locales = obtener_locales_service()
    
    if locales is None:
        return devolver_error("Error al obtener locales", 500)
    
    return jsonify(locales), 200

