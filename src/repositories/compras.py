import uuid
from sqlalchemy import text
from src.utils.config import db

def registrar_compra_transaccion(usuario_id, funcion_id, butaca_ids, precio_unitario):
    try:
        monto_total = len(butaca_ids) * precio_unitario
        
        codigo_compra = f"COMP-{uuid.uuid4().hex[:12].upper()}"

        with db.begin() as conn:
            # 1. Insertar la compra
            query_compra = text("""
                INSERT INTO compras (usuario_id, funcion_id, codigo, total, estado)
                VALUES (:usuario_id, :funcion_id, :codigo, :total, 'pendiente')
            """)
            resultado_compra = conn.execute(query_compra, {
                "usuario_id": usuario_id,
                "funcion_id": funcion_id,
                "codigo": codigo_compra,
                "total": monto_total
            })
            compra_id = resultado_compra.lastrowid

            # 2. Insertar las entradas asociadas
            query_entrada = text("""
                INSERT INTO entradas (compra_id, funcion_id, butaca_id, precio, qr_codigo, estado)
                VALUES (:compra_id, :funcion_id, :butaca_id, :precio, :qr_codigo, 'pendiente')
            """)
            
            for b_id in butaca_ids:
                qr_codigo = f"QR-F{funcion_id}-B{b_id}-{uuid.uuid4().hex}"
                
                conn.execute(query_entrada, {
                    "compra_id": compra_id,
                    "funcion_id": funcion_id,
                    "butaca_id": b_id,
                    "precio": precio_unitario,
                    "qr_codigo": qr_codigo
                })

        return {
            "compra_id": compra_id,
            "codigo_compra": codigo_compra,
            "monto_total": monto_total
        }

    except Exception as e:
        print(f"Error en la transacción de compra: {e}")
        return None
    
def obtener_compra_por_id(id_compra, usuario_id):
    query_compra = """
        SELECT c.id, c.codigo, c.total, c.estado, c.fecha_compra, c.numero_factura,
               f.id AS funcion_id, f.fecha_hora_inicio, f.fecha_hora_fin,
               p.titulo AS pelicula, s.nombre AS sala, l.nombre AS local
        FROM compras c
        JOIN funciones f ON c.funcion_id = f.id
        JOIN peliculas p ON f.pelicula_id = p.id
        JOIN salas s ON f.sala_id = s.id
        JOIN locales l ON s.local_id = l.id
        WHERE c.id = :id AND c.usuario_id = :usuario_id
    """
    
    query_entradas = """
        SELECT e.id, e.precio, e.estado,
               b.fila, b.numero, b.tipo AS tipo_butaca
        FROM entradas e
        JOIN butacas b ON e.butaca_id = b.id
        WHERE e.compra_id = :id
    """
    
    query_servicios = """
        SELECT cs.cantidad, cs.precio_unitario, cs.subtotal,
               s.nombre AS servicio
        FROM compra_servicios cs
        JOIN servicios s ON cs.servicio_id = s.id
        WHERE cs.compra_id = :id
    """

    valores = {"id": id_compra}

    conn = db.connect()
    
    resultado_compra = conn.execute(text(query_compra), {"id": id_compra, "usuario_id": usuario_id}).fetchone()
    if not resultado_compra:
        conn.close()
        return None

    compra = {
        "id": resultado_compra.id,
        "codigo": resultado_compra.codigo,
        "total": float(resultado_compra.total),
        "estado": resultado_compra.estado,
        "fecha_compra": resultado_compra.fecha_compra,
        "numero_factura": resultado_compra.numero_factura,
        "funcion_id": resultado_compra.funcion_id,
        "fecha_hora_inicio": resultado_compra.fecha_hora_inicio,
        "fecha_hora_fin": resultado_compra.fecha_hora_fin,
        "pelicula": resultado_compra.pelicula,
        "sala": resultado_compra.sala,
        "local": resultado_compra.local,
        "entradas": [],
        "servicios": []
    }

    resultado_entradas = conn.execute(text(query_entradas), valores)
    for fila in resultado_entradas:
        compra["entradas"].append({
            "id": fila.id,
            "butaca": f"{fila.fila}{fila.numero}",
            "tipo_butaca": fila.tipo_butaca,
            "precio": float(fila.precio),
            "estado": fila.estado
        })

    resultado_servicios = conn.execute(text(query_servicios), valores)
    for fila in resultado_servicios:
        compra["servicios"].append({
            "servicio": fila.servicio,
            "cantidad": fila.cantidad,
            "precio_unitario": float(fila.precio_unitario),
            "subtotal": float(fila.subtotal)
        })

    conn.close()
    return compra
#-------------------------------------------------
def obtener_compras_usuario(usuario_id, filtros, offset, limit):
    """
    Devuelve (filas, total) con las compras del usuario autenticado.
    filtros: dict con claves opcionales ya validadas por el service:
        estado, fecha_desde, fecha_hasta
    """
    condiciones = ["c.usuario_id = :usuario_id"]
    params = {"usuario_id": usuario_id}

    if filtros.get("estado"):
        condiciones.append("c.estado = :estado")
        params["estado"] = filtros["estado"]

    if filtros.get("fecha_desde"):
        condiciones.append("c.fecha_compra >= :fecha_desde")
        params["fecha_desde"] = filtros["fecha_desde"]

    if filtros.get("fecha_hasta"):
        condiciones.append("c.fecha_compra <= :fecha_hasta")
        params["fecha_hasta"] = filtros["fecha_hasta"]

    where = "WHERE " + " AND ".join(condiciones)

    sql_count = text(f"SELECT COUNT(*) AS total FROM compras c {where}")
    
    sql = text(f"""
        SELECT c.id, c.codigo, c.total, c.estado, c.fecha_compra,
               f.fecha_hora_inicio,
               p.titulo AS pelicula_titulo, p.poster_url,
               s.nombre AS sala_nombre, l.nombre AS local_nombre,
               (SELECT COUNT(*) FROM entradas e
                 WHERE e.compra_id = c.id) AS cantidad_entradas,
               (SELECT COUNT(*) FROM compra_servicios cs
                 WHERE cs.compra_id = c.id) AS cantidad_servicios
        FROM compras c
        JOIN funciones f ON c.funcion_id = f.id
        JOIN peliculas p ON f.pelicula_id = p.id
        JOIN salas     s ON f.sala_id    = s.id
        JOIN locales   l ON s.local_id   = l.id
        {where}
        ORDER BY c.fecha_compra DESC
        LIMIT :limit OFFSET :offset
    """)
    
    params["limit"] = limit
    params["offset"] = offset

    # Usamos un solo bloque connect() para hacer las dos consultas
    with db.connect() as conn:
        total = conn.execute(sql_count, params).scalar()
        filas = conn.execute(sql, params).fetchall()

    return filas, total

ESTADOS_CANCELABLES = ("pendiente", "pagada")
HORAS_LIMITE_CANCELACION = 2

def cancelar_compra_en_bd(id_compra, id_usuario, motivo):
    conn = db.connect()

    try:
        query = """
            SELECT
                c.usuario_id,
                c.estado,
                (
                    SELECT f.fecha_hora_inicio
                    FROM funciones f
                    WHERE f.id = c.funcion_id
                ) AS fecha_hora_inicio,
                NOW() > DATE_SUB(
                    (
                        SELECT f.fecha_hora_inicio
                        FROM funciones f
                        WHERE f.id = c.funcion_id
                    ),
                    INTERVAL :horas HOUR
                ) AS fuera_de_plazo
            FROM compras c
            WHERE c.id = :id_compra
            FOR UPDATE
        """

        valores = {"id_compra": id_compra, "motivo": motivo}

        resultado = conn.execute(
            text(query),
            {"id_compra": id_compra, "horas": HORAS_LIMITE_CANCELACION}
        )
        compra = resultado.fetchone()

        if compra is None:
            conn.rollback()
            return "no_existe"

        if compra.usuario_id != id_usuario:
            conn.rollback()
            return "no_existe"

        if compra.estado not in ESTADOS_CANCELABLES:
            conn.rollback()
            return "no_cancelable"

        if compra.fuera_de_plazo:
            conn.rollback()
            return "fuera_de_plazo"

        query = """
            UPDATE compras
            SET estado = 'cancelada',
                fecha_cancelacion = NOW(),
                motivo_cancelacion = :motivo
            WHERE id = :id_compra
        """

        conn.execute(text(query), valores)

        query = """
            UPDATE entradas
            SET estado = 'cancelada',
                fecha_cancelacion = NOW()
            WHERE compra_id = :id_compra
        """

        conn.execute(text(query), valores)

        conn.commit()

        return "cancelada"

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

def buscar_compra(id):

    query = "SELECT id, estado, usuario_id FROM compras WHERE id = :id"

    valores = {"id": id}

    conn = db.connect()
    resultado = conn.execute(text(query), valores)

    compras = []
    for fila in resultado:
        compra = {"id": fila.id, "estado": fila.estado, "usuario_id": fila.usuario_id}
        compras.append(compra)

    conn.close()

    if len(compras) == 0:
        return None

    return compras[0]

def agregar_servicio_a_compra(compra_id, servicio_id, cantidad):

    select_query = "SELECT precio FROM servicios WHERE id = :servicio_id"
    insert_query = """ INSERT INTO compra_servicios (compra_id, servicio_id, cantidad, precio_unitario, subtotal)
    VALUES (:compra_id, :servicio_id, :cantidad, :precio_unitario, :subtotal) """
    total_query = "UPDATE compras SET total = total + :subtotal WHERE id = :compra_id"

    conn = db.connect()

    try:
        fila = conn.execute(text(select_query), {"servicio_id": servicio_id}).fetchone()

        if fila is None:
            return "no_existe"

        precio = fila.precio
        subtotal = precio * cantidad

        valores = {
            "compra_id": compra_id,
            "servicio_id": servicio_id,
            "cantidad": cantidad,
            "precio_unitario": precio,
            "subtotal": subtotal,
        }

        conn.execute(text(insert_query), valores)
        conn.execute(text(total_query), valores)
        conn.commit()

        return {"precio_unitario": precio, "subtotal": subtotal}

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

def pagar_compra(id, numero_factura):

    compra_query = "UPDATE compras SET estado = 'pagada', numero_factura = :numero_factura WHERE id = :id AND estado = 'pendiente'"
    entradas_query = "UPDATE entradas SET estado = 'valida' WHERE compra_id = :id AND estado = 'pendiente'"

    valores = {"id": id, "numero_factura": numero_factura}

    conn = db.connect()
    conn.execute(text(compra_query), valores)
    conn.execute(text(entradas_query), valores)
    conn.commit()
    conn.close()

def obtener_datos_mail(compra_id):
    query = """
        SELECT u.email, u.nombre, c.total, c.numero_factura,
               e.qr_codigo, b.fila, b.numero, s.nombre AS sala,
               p.titulo AS pelicula, f.fecha_hora_inicio
        FROM compras c
        JOIN usuarios u ON c.usuario_id = u.id
        JOIN entradas e ON e.compra_id = c.id
        JOIN butacas b ON e.butaca_id = b.id
        JOIN funciones f ON c.funcion_id = f.id
        JOIN salas s ON f.sala_id = s.id
        JOIN peliculas p ON f.pelicula_id = p.id
        WHERE c.id = :id
    """
    with db.connect() as conn:
        return conn.execute(text(query), {"id": compra_id}).fetchall()


def marcar_email_enviado(compra_id):
    with db.begin() as conn:
        conn.execute(text("UPDATE compras SET email_enviado = TRUE WHERE id = :id"), {"id": compra_id})
