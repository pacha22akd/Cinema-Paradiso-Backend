from flask import Flask
from src.routes.salas import salas_bp
from src.routes.peliculas import peliculas_bp
from src.routes.estadisticas import estadisticas_bp
from src.routes.funciones import funciones_bp
from src.routes.compras import compras_bp

app = Flask(__name__)

app.register_blueprint(salas_bp)
app.register_blueprint(peliculas_bp)
app.register_blueprint(estadisticas_bp)
app.register_blueprint(funciones_bp)
app.register_blueprint(compras_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
