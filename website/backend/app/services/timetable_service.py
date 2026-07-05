from typing import List, Dict, Any
from app.repositories.timetable import TimetableRepository
from app.schemas.timetable import TimetableCreate, TimetableUpdate
from app.exceptions import NotFoundException

class TimetableService:
    @staticmethod
    def get_all_timetables() -> List[Dict[str, Any]]:
        return TimetableRepository.get_all()

    @staticmethod
    def get_timetable_by_id(tt_id: str) -> Dict[str, Any]:
        record = TimetableRepository.get_by_id(tt_id)
        if not record:
            raise NotFoundException("Timetable entry not found")
        return record

    @staticmethod
    def get_department_timetable(department: str, semester: int) -> List[Dict[str, Any]]:
        return TimetableRepository.find_many({"department": department, "semester": semester})

    @staticmethod
    def create_timetable_entry(data: TimetableCreate) -> Dict[str, Any]:
        return TimetableRepository.create(data.model_dump())

    @staticmethod
    def update_timetable_entry(tt_id: str, data: TimetableUpdate) -> Dict[str, Any]:
        record = TimetableRepository.get_by_id(tt_id)
        if not record:
            raise NotFoundException("Timetable entry not found")
        return TimetableRepository.update(tt_id, data.model_dump(exclude_unset=True))

    @staticmethod
    def delete_timetable_entry(tt_id: str) -> bool:
        if not TimetableRepository.get_by_id(tt_id):
            raise NotFoundException("Timetable entry not found")
        return TimetableRepository.delete(tt_id)
