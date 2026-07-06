from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.config import settings
from app.db.repository import JSONRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/student/login")

students_repo = JSONRepository(settings.STUDENTS_FILE)
admins_repo = JSONRepository(settings.ADMINS_FILE)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        subject: str = payload.get("sub")
        role: str = payload.get("role")
        if subject is None or role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = None
    # 'sub' contains the user id (student or admin) to avoid leaking emails in tokens
    if role == "student":
        user = students_repo.get_by_id(subject)
    elif role == "admin":
        user = admins_repo.get_by_id(subject)
        
    if user is None:
        raise credentials_exception
        
    user["role"] = role
    return user

async def get_current_student(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "student":
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return current_user

async def get_current_admin(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return current_user
