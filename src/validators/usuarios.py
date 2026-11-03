import re

def validar_email(email: str):
    if not email:
        raise ValueError("El email es obligatorio")
    
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(patron, email):
        raise ValueError("El formato del email no es válido")

def validar_telefono(telefono: str):
    if not telefono:
            raise ValueError("El telefono es obligatoria")
    if telefono: # El teléfono puede ser opcional
        telefono_limpio = re.sub(r'[\s\-\(\)]', '', telefono) # Limpia guiones/espacios
        patron = r'^(11|15)[0-9]{8}$'
        if not re.match(patron, telefono_limpio):
            raise ValueError("El teléfono debe empezar con 11 o 15 y tener exactamente 10 números")

def validar_password(password: str):
    if not password:
        raise ValueError("La contraseña es obligatoria")
    if len(password) < 6:
        raise ValueError("La contraseña debe tener al menos 6 caracteres")
    
def validar_registro_usuario(datos: dict):
    """Agrupa todas las validaciones para el registro."""
    validar_email(datos.get('email'))
    validar_telefono(datos.get('telefono'))
    validar_password(datos.get('password'))
    
    if not datos.get('nombre') or not datos.get('apellido'):
        raise ValueError("El nombre y el apellido son obligatorios")