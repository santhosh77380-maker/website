import re
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any
from app.schemas.auth import LoginRequest, StudentCreate, Token, StudentResponse, AdminResponse
from app.core.security import verify_password, get_password_hash, create_access_token
from app.db.repository import JSONRepository
from app.core.config import settings
from app.core.deps import oauth2_scheme
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])

students_repo = JSONRepository(settings.STUDENTS_FILE)
admins_repo = JSONRepository(settings.ADMINS_FILE)


def _validate_phone(phone: str) -> bool:
    if not phone:
        return True
    return bool(re.fullmatch(r"\+?[0-9\- ]{7,20}", phone))

def _validate_password_strength(pw: str) -> bool:
    # Minimum 8 chars, at least one number, one uppercase, one lowercase
    if len(pw) < 8:
        return False
    if not re.search(r"[0-9]", pw):
        return False
    if not re.search(r"[A-Z]", pw):
        return False
    if not re.search(r"[a-z]", pw):
        return False
    return True

def _generate_student_id() -> str:
    # Format STU000001 sequential
    students = students_repo.get_all()
    max_num = 0
    for s in students:
        sid = s.get('id')
        if not sid:
            continue
        m = re.match(r"STU0*(\d+)$", sid)
        if m:
            try:
                n = int(m.group(1))
                if n > max_num:
                    max_num = n
            except Exception:
                continue
    next_num = max_num + 1
    return f"STU{next_num:06d}"

@router.post("/student/login", response_model=Token)
def login_student(request: LoginRequest) -> Any:
    student = students_repo.get_by_email(request.email)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Email or Password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(request.password, student.get("password", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Email or Password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Use student id as token subject for privacy
    access_token = create_access_token(subject=student["id"], role="student")
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/admin/login", response_model=Token)
def login_admin(request: LoginRequest) -> Any:
    admin = admins_repo.get_by_email(request.email)
    if not admin or not verify_password(request.password, admin.get("password", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Email or Password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=admin["id"], role="admin")
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/student/register", response_model=Token)
def register_student(request: StudentCreate) -> Any:
    # Basic validations
    if students_repo.get_by_email(request.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # If register_number provided, ensure uniqueness
    reg_num = request.register_number.strip() if getattr(request, 'register_number', None) else ''
    if reg_num:
        all_students = students_repo.get_all()
        for s in all_students:
            if s.get('register_number') == reg_num:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Register number already exists')

    # Phone validation
    if not _validate_phone(request.phone):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid phone number')

    # Password strength
    if not _validate_password_strength(request.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Password does not meet strength requirements')

    # Prepare student data
    student_data = request.dict()

    # Generate sequential Student ID
    student_id = _generate_student_id()
    student_data['id'] = student_id

    # Auto-generate register number if not provided
    if not reg_num:
        # Create REG000001 style
        students = students_repo.get_all()
        max_reg = 0
        for s in students:
            r = s.get('register_number') or ''
            m = re.match(r"REG0*(\d+)$", r)
            if m:
                try:
                    n = int(m.group(1))
                    if n > max_reg:
                        max_reg = n
                except Exception:
                    continue
        student_data['register_number'] = f"REG{(max_reg+1):06d}"

    # Hash password
    student_data['password'] = get_password_hash(request.password)

    # Save
    try:
        students_repo.create(student_data)
        # Verify write
        if not students_repo.get_by_id(student_id):
            raise Exception('Verification failed after writing student record')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Registration failed: {str(e)}')

    # Create token with student id as subject
    access_token = create_access_token(subject=student_id, role='student')
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/student/me', response_model=StudentResponse)
def get_current_student(token: str = Depends(oauth2_scheme)):
    # This endpoint is expected to be protected via dependencies in application routes.
    # For flexibility we decode token here to return the student profile.
    from jose import jwt, JWTError
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        subject = payload.get('sub')
        role = payload.get('role')
        if not subject or role != 'student':
            raise JWTError()
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

    student = students_repo.get_by_id(subject)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Student not found')

    # Remove sensitive fields
    student_safe = {k: v for k, v in student.items() if k != 'password'}
    return student_safe


@router.get('/admin/me', response_model=AdminResponse)
def get_current_admin(token: str = Depends(oauth2_scheme)):
    from jose import jwt, JWTError
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        subject = payload.get('sub')
        role = payload.get('role')
        if not subject or role != 'admin':
            raise JWTError()
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

    admin = admins_repo.get_by_id(subject)
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Admin not found')

    admin_safe = {k: v for k, v in admin.items() if k != 'password'}
    return admin_safe
