from app.database import JSONDatabase
from app.security import verify_password, create_access_token
from app.exceptions import UnauthorizedException
from app.schemas.auth import LoginRequest, LoginResponse

class AuthService:
    @staticmethod
    def authenticate(cred: LoginRequest, role: str) -> LoginResponse:
        table = "admins.json" if role == "admin" else "students.json"
        user = JSONDatabase.find_one(table, {"email": cred.email})
        if not user or not verify_password(cred.password, user.get("password_hash", "")): raise UnauthorizedException("Invalid credentials")
        u2 = user.copy(); u2.pop("password_hash", None)
        return LoginResponse(access_token=create_access_token({"sub": user["id"], "role": role}), token_type="bearer", user=u2)