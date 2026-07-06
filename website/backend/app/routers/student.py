from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Any
from app.db.repository import JSONRepository
from app.core.config import settings
from datetime import datetime

router = APIRouter(prefix="/student", tags=["Student Dashboard"])

students_repo = JSONRepository(settings.STUDENTS_FILE)

# Dummy Global Data for Dashboard
NOTIFICATIONS = [
    {"title": "Semester Exams", "description": "Timetable has been released for final exams.", "date": str(datetime.now().date()), "type": "warning"},
    {"title": "Fee Due Reminder", "description": "Last date for bus fee payment is next Friday.", "date": str(datetime.now().date()), "type": "info"}
]

EVENTS = [
    {"icon": "💻", "title": "National Level Hackathon", "date": str(datetime.now().date()), "location": "Main Seminar Hall"},
    {"icon": "🎨", "title": "College Culturals 2026", "date": str(datetime.now().date()), "location": "Open Auditorium"}
]

@router.get("/profile")
def get_student_profile() -> Any:
    # Right now, returns first student in JSON for quick testing
    students = students_repo.get_all()
    if not students:
        raise HTTPException(status_code=404, detail="No students found")
    
    s = students[0]
    return {
        "firstName": s.get("full_name", "").split()[0] if s.get("full_name") else "Student",
        "lastName": s.get("full_name", "").split()[-1] if s.get("full_name") and len(s.get("full_name").split()) > 1 else "",
        "name": s.get("full_name", "Student"),
        "rollNumber": s.get("register_number", "-"),
        "email": s.get("email", "-"),
        "phone": s.get("phone", "-"),
        "department": s.get("department", "-"),
        "year": s.get("year", "1st"),
        "dob": s.get("dob", "-"),
        "bloodGroup": "O+",
        "address": s.get("address", "-")
    }

@router.get("/stats")
def get_student_stats() -> Any:
    return {
        "attendancePercentage": 85,
        "avgMarks": 78,
        "cgpa": "8.20",
        "feeStatus": "Paid"
    }

@router.get("/notifications")
def get_student_notifications() -> List[Any]:
    return NOTIFICATIONS

@router.get("/events")
def get_student_events() -> List[Any]:
    return EVENTS

@router.get("/attendance")
def get_student_attendance() -> Any:
    return {
        "subjects": [
            {"code": "CS301", "name": "Data Structures", "totalClasses": 40, "attended": 36, "percentage": 90},
            {"code": "CS302", "name": "Operating Systems", "totalClasses": 45, "attended": 32, "percentage": 71}
        ]
    }