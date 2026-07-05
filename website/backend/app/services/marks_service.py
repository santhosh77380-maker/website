from typing import List, Dict, Any
from app.repositories.marks import MarksRepository
from app.schemas.marks import MarksCreate, MarksUpdate
from app.exceptions import NotFoundException

class MarksService:
    @staticmethod
    def get_all_marks() -> List[Dict[str, Any]]:
        return MarksRepository.get_all()

    @staticmethod
    def get_mark_by_id(mark_id: str) -> Dict[str, Any]:
        record = MarksRepository.get_by_id(mark_id)
        if not record:
            raise NotFoundException("Marks record not found")
        return record

    @staticmethod
    def get_student_marks(student_id: str, semester: int = None) -> List[Dict[str, Any]]:
        query = {"student_id": student_id}
        if semester is not None:
            query["semester"] = semester
        return MarksRepository.find_many(query)

    @staticmethod
    def create_mark(data: MarksCreate) -> Dict[str, Any]:
        return MarksRepository.create(data.model_dump())

    @staticmethod
    def update_mark(mark_id: str, data: MarksUpdate) -> Dict[str, Any]:
        record = MarksRepository.get_by_id(mark_id)
        if not record:
            raise NotFoundException("Marks record not found")
        return MarksRepository.update(mark_id, data.model_dump(exclude_unset=True))

    @staticmethod
    def delete_mark(mark_id: str) -> bool:
        if not MarksRepository.get_by_id(mark_id):
            raise NotFoundException("Marks record not found")
        return MarksRepository.delete(mark_id)
