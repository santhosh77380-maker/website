from pydantic import BaseModel, EmailStr
from typing import Optional

class AdminBase(BaseModel):
    name: str
    email: EmailStr
    department: Optional[str] = None

class AdminCreate(AdminBase):
    password: str

class AdminUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None

class AdminResponse(AdminBase):
    id: str
    role: str

    class Config:
        from_attributes = True
