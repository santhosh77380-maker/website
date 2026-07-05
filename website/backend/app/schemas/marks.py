from pydantic import BaseModel
from typing import Optional

class MarksBase(BaseModel):
    student_id: str
    semester: int
    subject_code: str
    subject_name: str
    internal_marks: float
    external_marks: float
    total_marks: float
    grade: str
    result: str # Pass / Fail

class MarksCreate(MarksBase):
    pass

class MarksUpdate(BaseModel):
    internal_marks: Optional[float] = None
    external_marks: Optional[float] = None
    total_marks: Optional[float] = None
    grade: Optional[str] = None
    result: Optional[str] = None

class MarksResponse(MarksBase):
    id: str

    class Config:
        from_attributes = True
