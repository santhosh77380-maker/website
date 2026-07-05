from typing import TypeVar, Generic, Dict, Any, List, Optional
import uuid
from app.database import JSONDatabase
T = TypeVar('T')

class BaseRepository(Generic[T]):
    table_name: str = "base"
    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]: return JSONDatabase.read_all(cls.table_name)
    @classmethod
    def get_by_id(cls, item_id: str) -> Optional[Dict[str, Any]]: return JSONDatabase.find_one(cls.table_name, {"id": item_id})
    @classmethod
    def find_one(cls, query: Dict[str, Any]) -> Optional[Dict[str, Any]]: return JSONDatabase.find_one(cls.table_name, query)
    @classmethod
    def find_many(cls, query: Dict[str, Any]) -> List[Dict[str, Any]]: return JSONDatabase.find_many(cls.table_name, query)
    @classmethod
    def create(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if "id" not in data: data["id"] = str(uuid.uuid4())
        return JSONDatabase.insert(cls.table_name, data)
    @classmethod
    def update(cls, item_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]: return JSONDatabase.update_one(cls.table_name, {"id": item_id}, data)
    @classmethod
    def delete(cls, item_id: str) -> bool: return JSONDatabase.delete_one(cls.table_name, {"id": item_id})