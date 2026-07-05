from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any, Optional
from app.schemas.marks import MarksCreate, MarksUpdate
from app.services.marks_service import MarksService
from app.utils.response import success_response
from app.dependencies import get_current_admin, get_current_student

router = APIRouter()

# Admin routes
@router.post("/", dependencies=[Depends(get_current_admin)])
async def create_mark(record: MarksCreate):
    new_record = MarksService.create_mark(record)
    return success_response("Marks recorded successfully", data=new_record)

@router.get("/all", dependencies=[Depends(get_current_admin)])
async def get_all_marks():
    records = MarksService.get_all_marks()
    return success_response("Marks retrieved", data=records)

@router.get("/student/{student_id}", dependencies=[Depends(get_current_admin)])
async def get_student_marks_admin(student_id: str, semester: Optional[int] = Query(None)):
    records = MarksService.get_student_marks(student_id, semester)
    return success_response("Student marks retrieved", data=records)

@router.put("/{mark_id}", dependencies=[Depends(get_current_admin)])
async def update_mark(mark_id: str, record: MarksUpdate):
    updated = MarksService.update_mark(mark_id, record)
    return success_response("Marks updated successfully", data=updated)

@router.delete("/{mark_id}", dependencies=[Depends(get_current_admin)])
async def delete_mark(mark_id: str):
    MarksService.delete_mark(mark_id)
    return success_response("Marks deleted successfully")

# Student self-service routes
@router.get("/me")
async def get_my_marks(semester: Optional[int] = Query(None), current_user: Dict[str, Any] = Depends(get_current_student)):
    records = MarksService.get_student_marks(current_user["id"], semester)
    return success_response("Marks retrieved successfully", data=records)
