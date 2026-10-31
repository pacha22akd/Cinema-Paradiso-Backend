import uuid
from sqlalchemy import text
from src.utils.config import engine

def registrar_compra_transaccion(usuario_id, funcion_id, butaca_ids, precio_unitario):
    try:
        monto_total = len(butaca_ids) * precio_unitario
        
        codigo_compra = f"COMP-{uuid.uuid4().hex[:12].upper()}"

        with engine.begin() as conn:
            # 1. Insertar la compra
            query_compra = text("""
                INSERT INTO compras (usuario_id, funcion_id, codigo, total, estado)
                VALUES (:usuario_id, :funcion_id, :codigo, :total, 'pagada')
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
                VALUES (:compra_id, :funcion_id, :butaca_id, :precio, :qr_codigo, 'valida')
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