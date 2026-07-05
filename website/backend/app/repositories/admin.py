from app.repositories.base import BaseRepository
from typing import Dict, Any

class AdminRepository(BaseRepository):
    table_name = "admins.json"

    @classmethod
    def get_by_email(cls, email: str) -> Dict[str, Any] | None:
        return cls.find_one({"email": email})
