from src.repositories import usuarios
from src.validators.usuarios import validar_registro_usuario
from werkzeug.security import generate_password_hash

def registrar_usuario(datos):
    try:
        validar_registro_usuario(datos)
    except ValueError as e:
        return {"error": str(e), "status": 400}

    email = datos.get('email')
    if usuarios.obtener_por_email(email):
        return {"error": "El email ya está registrado en el sistema", "status": 400}

    rol_id = usuarios.obtener_rol_id_por_nombre('cliente')
    if not rol_id:
        return {"error": "Error interno: El rol 'cliente' no está configurado", "status": 500}

    password = datos.get('password')
    password_hash = generate_password_hash(password)

    nombre = datos.get('nombre', '').strip()
    apellido = datos.get('apellido', '').strip()
    email_limpio = email.strip().lower()
    telefono = datos.get('telefono')

    try:
        nuevo_usuario_id = usuarios.crear_usuario(
            nombre=nombre, 
            apellido=apellido, 
            email=email_limpio,
            password_hash=password_hash, 
            telefono=telefono, 
            rol_id=rol_id
        )
    except Exception as e:
        return {"error": f"Error al guardar en base de datos: {str(e)}", "status": 500}

    return {
        'id': nuevo_usuario_id,
        'nombre': nombre,
        'apellido': apellido,
        'email': email_limpio,
        'telefono': telefono,
        'rol_id': rol_id
    }