from flask import Flask
from src.routes.estadisticas import estadisticas_bp

app = Flask(__name__)

app.register_blueprint(estadisticas_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)