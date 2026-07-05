from typing import List, Dict, Any
from app.repositories.admin import AdminRepository
from app.schemas.admin import AdminCreate, AdminUpdate
from app.exceptions import NotFoundException, DuplicateResourceException
from app.security import get_password_hash

class AdminService:
    @staticmethod
    def get_all_admins() -> List[Dict[str, Any]]:
        admins = AdminRepository.get_all()
        for a in admins:
            a.pop("password_hash", None)
        return admins

    @staticmethod
    def get_admin_by_id(admin_id: str) -> Dict[str, Any]:
        admin = AdminRepository.get_by_id(admin_id)
        if not admin:
            raise NotFoundException("Admin not found")
        admin.pop("password_hash", None)
        return admin

    @staticmethod
    def create_admin(admin_data: AdminCreate) -> Dict[str, Any]:
        if AdminRepository.get_by_email(admin_data.email):
            raise DuplicateResourceException("Email already registered")

        data = admin_data.model_dump()
        password = data.pop("password")
        data["password_hash"] = get_password_hash(password)
        data["role"] = "admin"
        
        new_admin = AdminRepository.create(data)
        new_admin.pop("password_hash", None)
        return new_admin

    @staticmethod
    def update_admin(admin_id: str, update_data: AdminUpdate) -> Dict[str, Any]:
        admin = AdminRepository.get_by_id(admin_id)
        if not admin:
            raise NotFoundException("Admin not found")
            
        update_dict = update_data.model_dump(exclude_unset=True)
        
        if "email" in update_dict and update_dict["email"] != admin.get("email"):
            if AdminRepository.get_by_email(update_dict["email"]):
                raise DuplicateResourceException("Email already in use")

        updated_admin = AdminRepository.update(admin_id, update_dict)
        updated_admin.pop("password_hash", None)
        return updated_admin

    @staticmethod
    def delete_admin(admin_id: str) -> bool:
        if not AdminRepository.get_by_id(admin_id):
            raise NotFoundException("Admin not found")
        return AdminRepository.delete(admin_id)
