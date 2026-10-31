from flask import Flask
from src.routes.locales import locales_bp

app = Flask(__name__)

app.register_blueprint(locales_bp)

if __name__ == '__main__':
    app.run(debug=True)