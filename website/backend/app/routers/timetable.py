from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any
from app.schemas.timetable import TimetableCreate, TimetableUpdate
from app.services.timetable_service import TimetableService
from app.utils.response import success_response
from app.dependencies import get_current_admin, get_current_student

router = APIRouter()

# Admin routes
@router.post("/", dependencies=[Depends(get_current_admin)])
async def create_timetable_entry(record: TimetableCreate):
    new_record = TimetableService.create_timetable_entry(record)
    return success_response("Timetable entry created successfully", data=new_record)

@router.get("/all", dependencies=[Depends(get_current_admin)])
async def get_all_timetables():
    records = TimetableService.get_all_timetables()
    return success_response("All timetables retrieved", data=records)

@router.put("/{tt_id}", dependencies=[Depends(get_current_admin)])
async def update_timetable_entry(tt_id: str, record: TimetableUpdate):
    updated = TimetableService.update_timetable_entry(tt_id, record)
    return success_response("Timetable entry updated", data=updated)

@router.delete("/{tt_id}", dependencies=[Depends(get_current_admin)])
async def delete_timetable_entry(tt_id: str):
    TimetableService.delete_timetable_entry(tt_id)
    return success_response("Timetable entry deleted")

# Public / Student route
@router.get("/department")
async def get_department_timetable(department: str = Query(...), semester: int = Query(...)):
    # Accessible without auth or with auth depending on requirements, but let's just make it public or student
    records = TimetableService.get_department_timetable(department, semester)
    return success_response("Timetable retrieved", data=records)
