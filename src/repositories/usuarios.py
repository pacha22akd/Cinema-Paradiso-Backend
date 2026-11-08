from sqlalchemy import text
from src.utils.config import db


def actualizar_perfil(id_usuario, datos):
    columnas_permitidas = ("nombre", "apellido", "email", "telefono", "password_hash")
    condiciones = []
    parametros = {"id_usuario": id_usuario}

    for campo, valor in datos.items():

        if campo not in columnas_permitidas:
            return "campo_no_permitido"

        condiciones.append(f"{campo} = :{campo}")
        parametros[campo] = valor

    if len(condiciones) == 0:
        return "campo_no_permitido"

    query = "UPDATE usuarios SET " + ", ".join(condiciones)
    query += " WHERE id = :id_usuario"

    conn = db.connect()

    try:
        consulta = "SELECT id FROM usuarios WHERE id = :id_usuario"

        resultado = conn.execute(
            text(consulta),
            {"id_usuario": id_usuario}
        )

        if resultado.fetchone() is None:
            return None

        if "email" in datos:

            consulta = """SELECT id FROM usuarios
                          WHERE email = :email
                          AND id != :id_usuario"""

            resultado = conn.execute(
                text(consulta),
                {
                    "email": datos["email"],
                    "id_usuario": id_usuario
                }
            )

            if resultado.fetchone() is not None:
                return "email_duplicado"

        conn.execute(text(query), parametros)

        consulta = """SELECT id, nombre, apellido, email, telefono
                      FROM usuarios
                      WHERE id = :id_usuario"""

        resultado = conn.execute(
            text(consulta),
            {"id_usuario": id_usuario}
        )

        fila = resultado.fetchone()

        conn.commit()

        return dict(fila._mapping)

    except Exception:
        conn.rollback()
        return "error_bd"

    finally:
        conn.close()

        
def crear_usuario(nombre, apellido, email, password_hash, telefono, rol_id):
    query = """
        INSERT INTO usuarios (nombre, apellido, email, password_hash, telefono, rol_id)
        VALUES (:nombre, :apellido, :email, :password_hash, :telefono, :rol_id)
    """
    valores = {
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "password_hash": password_hash,
        "telefono": telefono,
        "rol_id": rol_id
    }
    
    conn = db.connect()
    resultado = conn.execute(text(query), valores)
    conn.commit() 
    nuevo_id = resultado.lastrowid
    conn.close()
    
    return nuevo_id

#-----------------------------------------------
def obtener_perfil_usuario(usuario_id):
    sql = text("""
        SELECT u.id, u.nombre, u.apellido, u.email, 
                u.telefono, u.fecha_registro, r.nombre AS rol
        FROM usuarios u
        JOIN roles r ON u.rol_id = r.id
        WHERE u.id = :usuario_id
    """)
    with db.connect() as conn:
        return conn.execute(sql, {"usuario_id": usuario_id}).fetchone()


def obtener_usuario_por_email(email):
    sql = text("""
        SELECT u.id, u.nombre, u.apellido, u.email, u.password_hash,
               u.telefono r.nombre AS rol
        FROM usuarios u
        JOIN roles r ON u.rol_id = r.id
        WHERE u.email = :email
    """)
    with db.connect() as conn:
        return conn.execute(sql, {"email": email}).fetchone()


def obtener_resumen_consumos(usuario_id):
    sql = text("""
        SELECT COUNT(id) AS total_compras,
               COALESCE(SUM(total), 0) AS total_gastado
        FROM compras
        WHERE usuario_id = :usuario_id
          AND estado != 'cancelada'
    """)
    with db.connect() as conn:
        return conn.execute(sql, {"usuario_id": usuario_id}).fetchone()


def obtener_historial_peliculas(usuario_id):
    sql = text("""
        SELECT p.titulo, p.poster_url, f.fecha_hora_inicio,
               c.estado AS estado_compra, c.codigo
        FROM compras c
        JOIN funciones f ON c.funcion_id = f.id
        JOIN peliculas p ON f.pelicula_id = p.id
        WHERE c.usuario_id = :usuario_id
          AND c.estado IN ('pagada', 'usada')
        ORDER BY f.fecha_hora_inicio DESC
    """)
    with db.connect() as conn:
        return conn.execute(sql, {"usuario_id": usuario_id}).fetchall()

def obtener_rol_id_por_nombre(nombre_rol):
    sql = text("""
        SELECT id 
        FROM roles 
        WHERE nombre = :nombre
    """)
    with db.connect() as conn:
        resultado = conn.execute(sql, {"nombre": nombre_rol}).fetchone()
        return resultado.id if resultado else None