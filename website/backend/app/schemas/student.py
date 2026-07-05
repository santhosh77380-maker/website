from pydantic import BaseModel, EmailStr
from typing import Optional

class StudentBase(BaseModel):
    name: str
    email: EmailStr
    register_number: str
    department: str
    year: int
    semester: int
    phone: Optional[str] = None
    address: Optional[str] = None

class StudentCreate(StudentBase):
    password: str

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    year: Optional[int] = None
    semester: Optional[int] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class StudentResponse(StudentBase):
    id: str
    role: str

    class Config:
        from_attributes = True
