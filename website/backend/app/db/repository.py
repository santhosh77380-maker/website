import json
import os
from typing import List, Dict, Any, Optional

class JSONRepository:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.filepath):
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, 'w') as f:
                json.dump([], f)

    def _read_data(self) -> List[Dict[str, Any]]:
        with open(self.filepath, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def _write_data(self, data: List[Dict[str, Any]]):
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=4)

    def get_all(self) -> List[Dict[str, Any]]:
        return self._read_data()

    def get_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        data = self._read_data()
        for item in data:
            if item.get("id") == item_id:
                return item
        return None
        
    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        data = self._read_data()
        for item in data:
            if item.get("email") == email:
                return item
        return None

    def create(self, item: Dict[str, Any]) -> Dict[str, Any]:
        data = self._read_data()
        data.append(item)
        self._write_data(data)
        return item

    def update(self, item_id: str, updated_item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        data = self._read_data()
        for i, item in enumerate(data):
            if item.get("id") == item_id:
                data[i] = {**item, **updated_item}
                self._write_data(data)
                return data[i]
        return None

    def delete(self, item_id: str) -> bool:
        data = self._read_data()
        initial_length = len(data)
        data = [item for item in data if item.get("id") != item_id]
        if len(data) < initial_length:
            self._write_data(data)
            return True
        return False
