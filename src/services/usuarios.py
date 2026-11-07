from src.repositories import usuarios
from src.validators.usuarios import validar_registro_usuario
from werkzeug.security import generate_password_hash


def modificar_perfil(id_usuario, datos):

    perfil = usuarios.actualizar_perfil(id_usuario, datos)

    return perfil


def registrar_usuario(datos):
    try:
        validar_registro_usuario(datos)
    except ValueError as e:
        return {"error": str(e), "status": 400}

    email = datos.get('email')
    if usuarios.obtener_usuario_por_email(email):
        return {"error": "El email ya está registrado en el sistema", "status": 409}

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

#--------------------------------------
def obtener_perfil_usuario(usuario_id):
    if not usuario_id:
        raise PermissionError("Usuario no autenticado")

    perfil_db = usuarios.obtener_perfil_usuario(usuario_id)
    if not perfil_db:
        raise LookupError("Usuario no encontrado")

    consumos_db = usuarios.obtener_resumen_consumos(usuario_id)
    historial_db = usuarios.obtener_historial_peliculas(usuario_id)

    fecha_reg = (
        perfil_db.fecha_registro.strftime("%Y-%m-%d")
        if perfil_db.fecha_registro else None
    )

    historial = []
    for h in historial_db:
        fecha_f = (
            h.fecha_hora_inicio.strftime("%Y-%m-%d %H:%M")
            if h.fecha_hora_inicio else None
        )
        historial.append({
            "codigo_compra": h.codigo,
            "pelicula": h.titulo,
            "poster": h.poster_url,
            "fecha_funcion": fecha_f,
            "estado": h.estado_compra
        })

    return {
        "datos_personales": {
            "id": perfil_db.id,
            "nombre": perfil_db.nombre,
            "apellido": perfil_db.apellido,
            "email": perfil_db.email,
            "telefono": perfil_db.telefono,
            "rol": perfil_db.rol,
            "fecha_registro": fecha_reg
        },
        "consumos": {
            "total_compras": consumos_db.total_compras,
            "total_gastado": float(consumos_db.total_gastado)
        },
        "historial_peliculas": historial
    }
