
import os
from dotenv import load_dotenv
from flask import Flask

from src.routes.sesiones import sesiones_bp
from src.routes.usuarios import usuarios_bp
from src.routes.servicios import servicios_bp
from src.routes.entradas import entradas_bp
from src.routes.locales import locales_bp
from src.routes.salas import salas_bp
from src.routes.peliculas import peliculas_bp
from src.routes.estadisticas import estadisticas_bp
from src.routes.funciones import funciones_bp
from src.routes.compras import compras_bp

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

app.register_blueprint(sesiones_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(servicios_bp)
app.register_blueprint(entradas_bp)
app.register_blueprint(locales_bp)
app.register_blueprint(salas_bp)
app.register_blueprint(peliculas_bp)
app.register_blueprint(estadisticas_bp)
app.register_blueprint(funciones_bp)
app.register_blueprint(compras_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

