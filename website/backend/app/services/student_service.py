from typing import List, Dict, Any
from app.repositories.student import StudentRepository
from app.schemas.student import StudentCreate, StudentUpdate
from app.exceptions import NotFoundException, DuplicateResourceException
from app.security import get_password_hash

class StudentService:
    @staticmethod
    def get_all_students() -> List[Dict[str, Any]]:
        students = StudentRepository.get_all()
        for s in students:
            s.pop("password_hash", None)
        return students

    @staticmethod
    def get_student_by_id(student_id: str) -> Dict[str, Any]:
        student = StudentRepository.get_by_id(student_id)
        if not student:
            raise NotFoundException("Student not found")
        student.pop("password_hash", None)
        return student

    @staticmethod
    def create_student(student_data: StudentCreate) -> Dict[str, Any]:
        if StudentRepository.get_by_email(student_data.email):
            raise DuplicateResourceException("Email already registered")
            
        if StudentRepository.get_by_register_number(student_data.register_number):
            raise DuplicateResourceException("Register number already exists")

        data = student_data.model_dump()
        password = data.pop("password")
        data["password_hash"] = get_password_hash(password)
        data["role"] = "student"
        
        new_student = StudentRepository.create(data)
        new_student.pop("password_hash", None)
        return new_student

    @staticmethod
    def update_student(student_id: str, update_data: StudentUpdate) -> Dict[str, Any]:
        student = StudentRepository.get_by_id(student_id)
        if not student:
            raise NotFoundException("Student not found")
            
        update_dict = update_data.model_dump(exclude_unset=True)
        
        # Check uniqueness if changing email or register number
        if "email" in update_dict and update_dict["email"] != student.get("email"):
            if StudentRepository.get_by_email(update_dict["email"]):
                raise DuplicateResourceException("Email already in use")

        updated_student = StudentRepository.update(student_id, update_dict)
        updated_student.pop("password_hash", None)
        return updated_student

    @staticmethod
    def delete_student(student_id: str) -> bool:
        if not StudentRepository.get_by_id(student_id):
            raise NotFoundException("Student not found")
        return StudentRepository.delete(student_id)
