from app.repositories.base import BaseRepository
from typing import Dict, Any

class StudentRepository(BaseRepository):
    table_name = "students.json"

    @classmethod
    def get_by_email(cls, email: str) -> Dict[str, Any] | None:
        return cls.find_one({"email": email})

    @classmethod
    def get_by_register_number(cls, register_number: str) -> Dict[str, Any] | None:
        return cls.find_one({"register_number": register_number})
