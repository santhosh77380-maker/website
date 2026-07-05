import json, os, threading
from typing import List, Dict, Any, Optional
from app.config import settings

class JSONDatabase:
    _locks: Dict[str, threading.Lock] = {}
    _global_lock = threading.Lock()

    @classmethod
    def _get_lock(cls, filename: str) -> threading.Lock:
        with cls._global_lock:
            if filename not in cls._locks: cls._locks[filename] = threading.Lock()
            return cls._locks[filename]

    @classmethod
    def _get_filepath(cls, table_name: str) -> str:
        return os.path.join(settings.DATABASE_DIR, f"{table_name}.json" if not table_name.endswith('.json') else table_name)

    @classmethod
    def _ensure_file(cls, filepath: str) -> None:
        if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
            with open(filepath, 'w', encoding='utf-8') as f: json.dump([], f)

    @classmethod
    def read_all(cls, table_name: str) -> List[Dict[str, Any]]:
        filepath = cls._get_filepath(table_name)
        lock = cls._get_lock(filepath)
        with lock:
            cls._ensure_file(filepath)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data if isinstance(data, list) else []
            except Exception:
                return []

    @classmethod
    def write_all(cls, table_name: str, data: List[Dict[str, Any]]) -> None:
        filepath = cls._get_filepath(table_name)
        lock = cls._get_lock(filepath)
        with lock:
            temp = filepath + ".tmp"
            with open(temp, 'w', encoding='utf-8') as f: json.dump(data, f, indent=4)
            os.replace(temp, filepath)

    @classmethod
    def insert(cls, table_name: str, record: Dict[str, Any]) -> Dict[str, Any]:
        data = cls.read_all(table_name)
        data.append(record)
        cls.write_all(table_name, data)
        return record

    @classmethod
    def find_one(cls, table_name: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        for item in cls.read_all(table_name):
            if all(item.get(k) == v for k, v in query.items()): return item
        return None

    @classmethod
    def find_many(cls, table_name: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [item for item in cls.read_all(table_name) if all(item.get(k) == v for k, v in query.items())]

    @classmethod
    def update_one(cls, table_name: str, query: Dict[str, Any], update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        data = cls.read_all(table_name)
        for idx, item in enumerate(data):
            if all(item.get(k) == v for k, v in query.items()):
                data[idx].update(update_data)
                cls.write_all(table_name, data)
                return data[idx]
        return None

    @classmethod
    def delete_one(cls, table_name: str, query: Dict[str, Any]) -> bool:
        data = cls.read_all(table_name)
        for idx, item in enumerate(data):
            if all(item.get(k) == v for k, v in query.items()):
                del data[idx]
                cls.write_all(table_name, data)
                return True
        return False