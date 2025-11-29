from dataclasses import dataclass
from datetime import datetime

@dataclass
class BinaryFile:
    id: str
    filename: str
    environment: str
    status: str
    uploaded_at: datetime
    signed_file: str = None   # path al archivo firmado
