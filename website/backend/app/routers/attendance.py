from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate, BulkAttendanceCreate
from app.services.attendance_service import AttendanceService
from app.utils.response import success_response
from app.dependencies import get_current_admin, get_current_student, get_current_user

router = APIRouter()

# Admin routes
@router.post("/", dependencies=[Depends(get_current_admin)])
async def create_attendance(record: AttendanceCreate):
    new_record = AttendanceService.create_attendance(record)
    return success_response("Attendance recorded successfully", data=new_record)

@router.post("/bulk", dependencies=[Depends(get_current_admin)])
async def bulk_create_attendance(records: BulkAttendanceCreate):
    new_records = AttendanceService.bulk_create_attendance(records)
    return success_response(f"{len(new_records)} attendance records created successfully", data=new_records)

@router.get("/all", dependencies=[Depends(get_current_admin)])
async def get_all_attendance():
    records = AttendanceService.get_all_attendance()
    return success_response("Attendance records retrieved", data=records)

@router.get("/student/{student_id}", dependencies=[Depends(get_current_admin)])
async def get_student_attendance_admin(student_id: str):
    records = AttendanceService.get_student_attendance(student_id)
    return success_response("Student attendance retrieved", data=records)

@router.put("/{attendance_id}", dependencies=[Depends(get_current_admin)])
async def update_attendance(attendance_id: str, record: AttendanceUpdate):
    updated = AttendanceService.update_attendance(attendance_id, record)
    return success_response("Attendance updated successfully", data=updated)

@router.delete("/{attendance_id}", dependencies=[Depends(get_current_admin)])
async def delete_attendance(attendance_id: str):
    AttendanceService.delete_attendance(attendance_id)
    return success_response("Attendance deleted successfully")

# Student self-service routes
@router.get("/me")
async def get_my_attendance(current_user: Dict[str, Any] = Depends(get_current_student)):
    records = AttendanceService.get_student_attendance(current_user["id"])
    return success_response("Attendance retrieved successfully", data=records)
