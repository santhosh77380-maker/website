from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from app.schemas.admin import AdminCreate, AdminUpdate
from app.services.admin_service import AdminService
from app.utils.response import success_response
from app.dependencies import get_current_admin

router = APIRouter()

@router.post("/", dependencies=[Depends(get_current_admin)])
async def create_admin(admin: AdminCreate):
    new_admin = AdminService.create_admin(admin)
    return success_response("Admin created successfully", data=new_admin)

@router.get("/", dependencies=[Depends(get_current_admin)])
async def get_all_admins():
    admins = AdminService.get_all_admins()
    return success_response("Admins retrieved successfully", data=admins)

@router.get("/{admin_id}", dependencies=[Depends(get_current_admin)])
async def get_admin(admin_id: str):
    admin = AdminService.get_admin_by_id(admin_id)
    return success_response("Admin retrieved successfully", data=admin)

@router.put("/{admin_id}", dependencies=[Depends(get_current_admin)])
async def update_admin(admin_id: str, admin: AdminUpdate):
    updated = AdminService.update_admin(admin_id, admin)
    return success_response("Admin updated successfully", data=updated)

@router.delete("/{admin_id}", dependencies=[Depends(get_current_admin)])
async def delete_admin(admin_id: str):
    AdminService.delete_admin(admin_id)
    return success_response("Admin deleted successfully")
