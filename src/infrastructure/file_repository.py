import os 
from datetime import datetime
from typing import BinaryIO

class FileRepository:

    def __init__(self, base_path: str = "data"):
        self.base_path = base_path
        self.binary_dir = os.path.join(base_path, "binaries")
        self.signed_dir = os.path.join(base_path, "signed")
        self.__ensure_directories()

    def __ensure_directories(self) -> None:
        os.makedirs(self.binary_dir, exist_ok=True)
        os.makedirs(self.signed_dir, exist_ok=True)

    def save(self, file: BinaryIO, file_id: str, signed: bool = False) -> str:
        directory = self.signed_dir if signed else self.binary_dir
        filename = f"{file_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.bin"
        file_path = os.path.join(directory, filename)

        # Si flask FileStorage
        if hasattr(file, "save"):
            file.save(file_path)
        else:
            # file puede ser bytes-like
            with open(file_path, "wb") as f:
                try:
                    f.write(file.read())
                except Exception:
                    f.write(file)  # si ya es bytes

        return file_path

    def move_to_signed(self, original_path: str, signed_data: bytes) -> str:
        # keep name from original, prefix with signed_
        original_name = os.path.basename(original_path)
        signed_filename = f"signed_{original_name}"
        signed_path = os.path.join(self.signed_dir, signed_filename)

        with open(signed_path, "wb") as signed_file:
            signed_file.write(signed_data)

        return signed_path

    def load(self, file_path: str) -> bytes:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, "rb") as f:
            return f.read()

    def delete(self, file_path: str) -> None:
        if os.path.exists(file_path):
            os.remove(file_path)

    def list_files(self, signed: bool = False) -> list:
        directory = self.signed_dir if signed else self.binary_dir
        return sorted(os.listdir(directory))
