from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Dict, List
import uuid

from app.core.config import settings
from app.core.security import pwd_context
from app.db.repository import JSONRepository

router = APIRouter(prefix="/admin", tags=["Admin"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/admin/login")

students_repo = JSONRepository(settings.STUDENTS_FILE)
admins_repo = JSONRepository(settings.ADMINS_FILE)


def get_current_admin(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        subject: str = payload.get("sub")
        role: str = payload.get("role")
        if role != "admin" or not subject:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    admin = admins_repo.get_by_id(subject)
    if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin not found")
    return admin


@router.get("/stats")
def get_stats(current_admin: Dict = Depends(get_current_admin)):
    return {
        "total_students": len(students_repo.get_all()),
        "total_admins": len(admins_repo.get_all()),
    }


@router.get("/students")
def list_students(current_admin: Dict = Depends(get_current_admin)) -> List[Dict]:
    return students_repo.get_all()


@router.post("/students")
def create_student(student: Dict, current_admin: Dict = Depends(get_current_admin)):
    if students_repo.get_by_email(student.get("email")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )
    student_id = f"STU_{uuid.uuid4().hex[:8].upper()}"
    student["id"] = student_id
    if "password" in student:
        student["password"] = pwd_context.hash(student["password"])
    students_repo.create(student)
    return student


@router.put("/students/{student_id}")
def update_student(student_id: str, updates: Dict, current_admin: Dict = Depends(get_current_admin)):
    existing = students_repo.get_by_id(student_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
        )
    if "password" in updates:
        updates["password"] = pwd_context.hash(updates["password"])
    updated = students_repo.update(student_id, updates)
    return updated


@router.delete("/students/{student_id}")
def delete_student(student_id: str, current_admin: Dict = Depends(get_current_admin)):
    success = students_repo.delete(student_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
        )
    return {"detail": "Student deleted"}
