from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class AttendanceBase(BaseModel):
    student_id: str
    date: str  # Format YYYY-MM-DD
    status: str  # Present, Absent, Half-Day
    remarks: Optional[str] = None

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceUpdate(BaseModel):
    status: Optional[str] = None
    remarks: Optional[str] = None

class AttendanceResponse(AttendanceBase):
    id: str

    class Config:
        from_attributes = True

class BulkAttendanceCreate(BaseModel):
    records: List[AttendanceCreate]
