from flask import Flask
from src.routes.compras import compras_bp

app = Flask(__name__)

app.register_blueprint(compras_bp)


@app.route("/")
def inicio():
    return {"mensaje": "Cine Paradiso funcionando"}, 200


if __name__ == "__main__":
    app.run(debug=True)
