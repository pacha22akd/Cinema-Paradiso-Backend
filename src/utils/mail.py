import os
import io
import smtplib
import qrcode
from email.message import EmailMessage


def generar_qr_png(texto): 
    imagen = qrcode.make(texto)
    archivo = io.BytesIO() 
    imagen.save(archivo, format="PNG")
    return archivo.getvalue()


def enviar_mail_compra(filas):
    remitente = os.getenv("MAIL_USUARIO")
    contrasena = os.getenv("MAIL_CONTRASENA") 
    compra = filas[0] 

    mensaje = EmailMessage()
    mensaje["Subject"] = f"Cine Paradiso - Tu compra {compra.numero_factura}"
    mensaje["From"] = remitente
    mensaje["To"] = compra.email

    texto = f"Hola {compra.nombre}!\n\n"
    texto += "Tu compra fue confirmada.\n"
    texto += f"Factura: {compra.numero_factura}\n"
    texto += f"Total: ${compra.total}\n\n"
    texto += "Tus entradas:\n"
    for fila in filas:
        texto += f"- {fila.pelicula} | {fila.fecha_hora_inicio} | {fila.sala} | Butaca {fila.fila}{fila.numero}\n"
    texto += "\nPresentá el código QR de cada entrada en la puerta del cine.\n"
    mensaje.set_content(texto)

    for fila in filas:
        imagen_qr = generar_qr_png(fila.qr_codigo)
        mensaje.add_attachment(imagen_qr, maintype="image", subtype="png",
                               filename=f"entrada_{fila.fila}{fila.numero}.png")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
        servidor.login(remitente, contrasena)
        servidor.send_message(mensaje)