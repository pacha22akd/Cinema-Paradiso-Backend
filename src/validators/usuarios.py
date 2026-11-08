import re

def validar_modificacion_perfil(datos):
    if not isinstance(datos, dict):
        return False, None, "El cuerpo debe ser un objeto JSON"

    if len(datos) == 0:
        return False, None, "Debe enviar al menos un campo para modificar"

    campos_texto = {"nombre": 100, "apellido": 100, "email": 150, "telefono": 30}

    perfil = {}

    for campo, valor in datos.items():

        if campo == "password":
            if not isinstance(valor, str):
                return False, None, "La contraseña debe ser texto"

            if valor != "":

                if len(valor) < 6 or valor.strip() == "":
                    return False, None, "La contraseña debe tener al menos 6 caracteres validos"

                perfil[campo] = valor

        else:

            if campo not in campos_texto:
                return False, None, f"El campo {campo} no se puede modificar"

            if campo == "telefono" and valor is None:
                perfil[campo] = None

            else:
                if not isinstance(valor, str):
                    return False, None, f"El campo {campo} debe ser texto"

                valor = valor.strip()

                if valor == "":
                    if campo == "telefono":
                        valor = None
                    else:
                        return False, None, f"El campo {campo} no puede estar vacio"

                if valor is not None and len(valor) > campos_texto[campo]:
                    return False, None, f"El campo {campo} supera la longitud permitida"

                if campo == "email":
                    if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor) is None:
                        return False, None, "El email no tiene un formato valido"

                    valor = valor.lower()

                perfil[campo] = valor

    if len(perfil) == 0:
        return False, None, "Debe enviar al menos un campo para modificar"

    return True, perfil, None

def validar_email(email: str):
    if not email:
        raise ValueError("El email es obligatorio")
    
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(patron, email):
        raise ValueError("El formato del email no es válido")

def validar_telefono(telefono: str):
    if not telefono:
            raise ValueError("El telefono es obligatoria")
    if telefono: 
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
