from flask import request, jsonify, render_template, Blueprint, url_for
from flask_mail import Message
from src.application.use_cases import UploadBinaryCase, ApproveBinaryCase
from src.infrastructure.file_repository import FileRepository
from src.infrastructure.json_repository import JsonRepository
from src.app.extensions import mail

routes_bp = Blueprint("routes_bp", __name__)

JSON_PATH = "database.json"


@routes_bp.route("/")
def home():
    return render_template("home.html")


@routes_bp.route('/upload', methods=['POST'])
def upload():
    file = request.files.get("file")
    environment = request.form.get("environment")
    email_destino = request.form.get("email")

    if not file or not environment:
        return jsonify({"error": "Missing file or environment"}), 400

    use_case = UploadBinaryCase(FileRepository(), JsonRepository)
    binary = use_case.execute(file, environment)

    # Si es producción y hay correo → enviar email para aprobación
    if environment == "prod" and email_destino:
        send_approval_email(binary.id, email_destino)

    return jsonify({
        'id': binary.id,
        'filename': binary.filename,
        'status': binary.status,
        'environment': binary.environment,
        'uploaded_at': binary.uploaded_at.isoformat(),
        'signed_file': None
    })


def send_approval_email(file_id: str, email_destino: str):
    link = f"{request.url_root.rstrip('/')}{url_for('routes_bp.approve')}?file_id={file_id}"

    msg = Message(
        subject="Aprobación requerida - Binary Manager",
        recipients=[email_destino]
    )

    msg.html = f"""
        <h2>Se requiere aprobación</h2>
        <p>Haz clic para aprobar:</p>
        <a href="{link}" 
           style="display:inline-block; padding: 10px 15px; background: #2e7d32; color: white; text-decoration:none; border-radius:6px;">
            Aprobar
        </a>
    """

    mail.send(msg)


@routes_bp.route("/files")
def list_files():
    repo = JsonRepository(JSON_PATH)
    records = repo.all()

    normalized = []
    for r in records:
        normalized.append({
            "id": r.get("id") or r.get("file_id"),
            "filename": r.get("filename"),
            "environment": r.get("environment"),
            "status": r.get("status"),
            "uploaded_at": r.get("uploaded_at"),
            "signed_file": r.get("signed_file")
        })

    return jsonify(normalized), 200


@routes_bp.route("/approve")
def approve():
    file_id = request.args.get("file_id")
    if not file_id:
        return "Falta file_id", 400

    repo = JsonRepository(JSON_PATH)
    file_repo = FileRepository()
    use_case = ApproveBinaryCase(repo, file_repo)

    ok = use_case.execute(file_id)
    if not ok:
        return "Archivo no encontrado", 404

    return "Archivo aprobado correctamente", 200
