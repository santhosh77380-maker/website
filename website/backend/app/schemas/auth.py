from pydantic import BaseModel, EmailStr
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class StudentCreate(BaseModel):
    full_name: str = ""
    email: EmailStr
    phone: Optional[str] = ""
    register_number: Optional[str] = ""
    department: Optional[str] = ""
    course: Optional[str] = ""
    year: Optional[str] = ""
    semester: Optional[str] = ""
    gender: Optional[str] = ""
    dob: Optional[str] = ""
    address: Optional[str] = ""
    password: str

class StudentResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    phone: str
    register_number: str
    department: str
    course: str
    year: str
    semester: str
    gender: str
    dob: str
    address: str

class AdminResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
