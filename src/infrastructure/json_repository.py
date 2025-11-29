import json
import os

class JsonRepository:

    def __init__(self, file_path="database.json"):
        self.file_path = file_path
        # asegurar archivo existe y es lista
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f, indent=4)

    def load(self):
        with open(self.file_path, "r") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    return []
                return data
            except json.JSONDecodeError:
                return []

    def save(self, data):
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

    def all(self):
        return self.load()

    def add_record(self, data: dict):
        records = self.load()
        records.append(data)
        self.save(records)

    def update_record(self, file_id: str, updates: dict):
        records = self.load()
        updated = False

        for entry in records:
            # compatibilidad con 'id' o 'file_id'
            if entry.get("id") == file_id or entry.get("file_id") == file_id:
                entry.update(updates)
                # normalizar key 'id'
                if "file_id" in entry and "id" not in entry:
                    entry["id"] = entry.pop("file_id")
                updated = True
                break

        if updated:
            self.save(records)

        return updated
