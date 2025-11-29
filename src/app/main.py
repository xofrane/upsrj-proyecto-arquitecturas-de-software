from flask import Flask
from src.app.extensions import mail
from src.app.routes import routes_bp
from src.config import settings
from src.common.vars import Hosts

def create_app() -> Flask:
    app = Flask(__name__)

    # CONFIG MAIL
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'frandaponte6@gmail.com'
    app.config['MAIL_PASSWORD'] = 'wwmv xhvy awio ikil'
    app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

    mail.init_app(app)

    app.register_blueprint(routes_bp)
    return app

app = create_app()

if __name__ == '__main__':
    hosts = Hosts()
    app.run(host=hosts.main[0], port=hosts.main[1])
