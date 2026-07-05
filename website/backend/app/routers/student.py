from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse
from app.services.student_service import StudentService
from app.utils.response import success_response
from app.dependencies import get_current_admin, get_current_student, get_current_user

router = APIRouter()

# Admin routes for managing students
@router.post("/", dependencies=[Depends(get_current_admin)])
async def create_student(student: StudentCreate):
    new_student = StudentService.create_student(student)
    return success_response("Student created successfully", data=new_student)

@router.get("/", dependencies=[Depends(get_current_admin)])
async def get_all_students():
    students = StudentService.get_all_students()
    return success_response("Students retrieved successfully", data=students)

@router.get("/{student_id}", dependencies=[Depends(get_current_admin)])
async def get_student(student_id: str):
    student = StudentService.get_student_by_id(student_id)
    return success_response("Student retrieved successfully", data=student)

@router.put("/{student_id}", dependencies=[Depends(get_current_admin)])
async def update_student(student_id: str, student: StudentUpdate):
    updated = StudentService.update_student(student_id, student)
    return success_response("Student updated successfully", data=updated)

@router.delete("/{student_id}", dependencies=[Depends(get_current_admin)])
async def delete_student(student_id: str):
    StudentService.delete_student(student_id)
    return success_response("Student deleted successfully")

# Student self-service routes
@router.get("/me/profile")
async def get_my_profile(current_user: Dict[str, Any] = Depends(get_current_student)):
    student = StudentService.get_student_by_id(current_user["id"])
    return success_response("Profile retrieved successfully", data=student)

@router.put("/me/profile")
async def update_my_profile(student_update: StudentUpdate, current_user: Dict[str, Any] = Depends(get_current_student)):
    # Prevent students from updating certain fields (like register_number) directly here,
    # or handle via specific schema. For now, allow basic update via StudentUpdate.
    updated = StudentService.update_student(current_user["id"], student_update)
    return success_response("Profile updated successfully", data=updated)
