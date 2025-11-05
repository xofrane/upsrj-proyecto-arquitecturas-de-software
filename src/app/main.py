from flask import Flask
from cryptography.fernet import Fernet
from src.app.routes import register_routes
from src.common.vars import Hosts

# === Agregar criptografía para el test ===
key = Fernet.generate_key()
f = Fernet(key)
message = b"A really secret message. Not for prying eyes."
token = f.encrypt(message)
# =========================================

def create_app() -> Flask:
    """
    Crea la aplicación principal de Flask
    """
    app = Flask(__name__)
    register_routes(app)
    return app

app = create_app()

if __name__ == '__main__':
    hosts = Hosts()
    app.run(host=hosts.main[0], port=hosts.main[1])
