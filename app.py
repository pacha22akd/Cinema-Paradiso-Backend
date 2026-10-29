from flask import Flask
from src.routes.peliculas import peliculas_bp

app = Flask(__name__)

app.register_blueprint(peliculas_bp)

if __name__ == '__main__':
    app.run(debug=True)