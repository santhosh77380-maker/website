from typing import Any, Generic, TypeVar, Optional
from pydantic import BaseModel
from datetime import datetime, timezone
T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None
    timestamp: str

def success_response(message: str, data: Any = None) -> dict:
    return {"success": True, "message": message, "data": data if data is not None else {}, "timestamp": datetime.now(timezone.utc).isoformat()}

def error_response(message: str, data: Any = None) -> dict:
    return {"success": False, "message": message, "data": data if data is not None else {}, "timestamp": datetime.now(timezone.utc).isoformat()}