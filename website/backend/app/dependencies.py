from typing import Dict, Any
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.security import decode_access_token
from app.exceptions import UnauthorizedException, ForbiddenException
from app.database import JSONDatabase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/student/login")
def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    payload = decode_access_token(token)
    if not payload.get("sub") or not payload.get("role"): raise UnauthorizedException("Invalid token")
    table = "admins.json" if payload["role"] == "admin" else "students.json"
    user = JSONDatabase.find_one(table, {"id": payload["sub"]})
    if not user: raise UnauthorizedException("User not found")
    user["role"] = payload["role"]
    return user
def get_current_admin(user: Dict[str, Any] = Depends(get_current_user)):
    if user.get("role") != "admin": raise ForbiddenException("Admin only")
    return user
def get_current_student(user: Dict[str, Any] = Depends(get_current_user)):
    if user.get("role") != "student": raise ForbiddenException("Student only")
    return user