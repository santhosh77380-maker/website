from fastapi import APIRouter
from app.schemas.auth import LoginRequest
from app.services.auth_service import AuthService
from app.utils.response import success_response
router = APIRouter()
@router.post("/admin/login")
def admin_login(cred: LoginRequest): return success_response("OK", AuthService.authenticate(cred, "admin").model_dump())
@router.post("/student/login")
def student_login(cred: LoginRequest): return success_response("OK", AuthService.authenticate(cred, "student").model_dump())