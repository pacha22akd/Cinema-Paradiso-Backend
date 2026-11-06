from flask import Blueprint, jsonify
from src.services.locales import obtener_locales_service
from src.utils.errores import devolver_error
locales_bp = Blueprint('locales_bp', __name__)

@locales_bp.route('/locales', methods=['GET'])
def obtener_locales():
    
    locales = obtener_locales_service()
    
    if locales is None:
        return devolver_error("Error al obtener locales", 500)
    
    return jsonify(locales), 200