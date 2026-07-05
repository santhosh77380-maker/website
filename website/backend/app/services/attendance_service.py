from typing import List, Dict, Any
from app.repositories.attendance import AttendanceRepository
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate, BulkAttendanceCreate
from app.exceptions import NotFoundException

class AttendanceService:
    @staticmethod
    def get_all_attendance() -> List[Dict[str, Any]]:
        return AttendanceRepository.get_all()

    @staticmethod
    def get_attendance_by_id(attendance_id: str) -> Dict[str, Any]:
        record = AttendanceRepository.get_by_id(attendance_id)
        if not record:
            raise NotFoundException("Attendance record not found")
        return record

    @staticmethod
    def get_student_attendance(student_id: str) -> List[Dict[str, Any]]:
        return AttendanceRepository.find_many({"student_id": student_id})

    @staticmethod
    def create_attendance(data: AttendanceCreate) -> Dict[str, Any]:
        return AttendanceRepository.create(data.model_dump())

    @staticmethod
    def bulk_create_attendance(bulk_data: BulkAttendanceCreate) -> List[Dict[str, Any]]:
        created = []
        for record in bulk_data.records:
            created.append(AttendanceRepository.create(record.model_dump()))
        return created

    @staticmethod
    def update_attendance(attendance_id: str, data: AttendanceUpdate) -> Dict[str, Any]:
        record = AttendanceRepository.get_by_id(attendance_id)
        if not record:
            raise NotFoundException("Attendance record not found")
        return AttendanceRepository.update(attendance_id, data.model_dump(exclude_unset=True))

    @staticmethod
    def delete_attendance(attendance_id: str) -> bool:
        if not AttendanceRepository.get_by_id(attendance_id):
            raise NotFoundException("Attendance record not found")
        return AttendanceRepository.delete(attendance_id)
