from datetime import datetime
from uuid import uuid4
from src.domain.models import BinaryFile
import os

class UploadBinaryCase:

    def __init__(self, file_repo, db_repo_cls):
        self.file_repo = file_repo
        # db_repo_cls es la clase JsonRepository; le pasamos la ruta "database.json"
        self.db_repo = db_repo_cls("database.json")

    def execute(self, file, environment: str) -> BinaryFile:
        binary_id = str(uuid4())
        filename = self.file_repo.save(file, binary_id)

        status = "pending" if environment == "prod" else "signed"

        binary = BinaryFile(
            id=binary_id,
            filename=filename,
            environment=environment,
            status=status,
            uploaded_at=datetime.now()
        )

        # Guardamos registro en DB (normalizamos keys a 'id')
        self.db_repo.add_record({
            "id": binary.id,
            "filename": binary.filename,
            "environment": binary.environment,
            "status": binary.status,
            "uploaded_at": binary.uploaded_at.isoformat(),
            "signed_file": None
        })

        return binary


class ApproveBinaryCase:

    def __init__(self, db_repo, file_repo):
        """
        db_repo: instancia de JsonRepository ya inicializada con path
        file_repo: instancia de FileRepository
        """
        self.db_repo = db_repo
        self.file_repo = file_repo

    def execute(self, file_id: str):
        """
        1) Buscar registro
        2) Si existe, leer binario original
        3) Crear una versión firmada (simulada) y guardarla en data/signed
        4) Actualizar registro con status 'approved', 'approved_at', y 'signed_file'
        """
        # Cargar todos y encontrar el registro
        records = self.db_repo.load()
        target = None
        for entry in records:
            if entry.get("id") == file_id or entry.get("file_id") == file_id:
                target = entry
                break

        if not target:
            return False

        original_path = target.get("filename")
        if not original_path or not os.path.exists(original_path):
            # si no existe el archivo original, sólo marcar aprobado sin signed_file
            update = {
                "status": "approved",
                "approved_at": datetime.now().isoformat(),
                "signed_file": None
            }
            return self.db_repo.update_record(file_id, update)

        # Leemos el original
        try:
            original_bytes = self.file_repo.load(original_path)
        except Exception:
            original_bytes = None

        # Creamos contenido "firmado" (simulación) y lo guardamos
        if original_bytes is not None:
            signed_bytes = original_bytes + b"\n--SIGNED--\n" + datetime.now().isoformat().encode()
            signed_path = self.file_repo.move_to_signed(original_path, signed_bytes)
        else:
            signed_path = None

        update = {
            "status": "approved",
            "approved_at": datetime.now().isoformat(),
            "signed_file": signed_path
        }

        return self.db_repo.update_record(file_id, update)
