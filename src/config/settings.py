import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "data", "binaries")
SIGNED_FOLDER = os.path.join(BASE_DIR, "data", "signed")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SIGNED_FOLDER, exist_ok=True)

# SMTP
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USE_TLS = True

# VARIABLES DE ENTORNO (no quemadas)
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_DEFAULT_SENDER = MAIL_USERNAME
