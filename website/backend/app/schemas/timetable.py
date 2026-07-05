from pydantic import BaseModel
from typing import Optional

class TimetableBase(BaseModel):
    department: str
    semester: int
    day_of_week: str  # Monday, Tuesday, etc.
    period: int       # 1 to 8 (or whichever max periods exist)
    subject_code: str
    subject_name: str
    faculty_id: str
    faculty_name: str
    room_number: str

class TimetableCreate(TimetableBase):
    pass

class TimetableUpdate(BaseModel):
    subject_code: Optional[str] = None
    subject_name: Optional[str] = None
    faculty_id: Optional[str] = None
    faculty_name: Optional[str] = None
    room_number: Optional[str] = None

class TimetableResponse(TimetableBase):
    id: str

    class Config:
        from_attributes = True
