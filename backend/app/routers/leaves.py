from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import date
from typing import Optional

from app.dependencies import get_supabase, get_admin_user, get_current_user

router = APIRouter(prefix="/api/leaves", tags=["leaves"])

class LeaveCreate(BaseModel):
    user_id: str
    leave_date: date
    reason: Optional[str] = None

class LeaveUpdate(BaseModel):
    leave_date: Optional[date] = None
    reason: Optional[str] = None

@router.get("")
def list_leaves(user=Depends(get_current_user), supabase=Depends(get_supabase)):
    res = supabase.table("planned_leaves").select("*, profiles(full_name)").execute()
    return res.data

@router.post("")
def create_leave(leave: LeaveCreate, admin=Depends(get_admin_user), supabase=Depends(get_supabase)):
    data = leave.model_dump()
    data["leave_date"] = str(data["leave_date"])
    res = supabase.table("planned_leaves").insert(data).execute()
    return res.data[0] if res.data else None

@router.put("/{leave_id}")
def update_leave(leave_id: str, leave: LeaveUpdate, admin=Depends(get_admin_user), supabase=Depends(get_supabase)):
    data = leave.model_dump(exclude_unset=True)
    if "leave_date" in data:
        data["leave_date"] = str(data["leave_date"])
    res = supabase.table("planned_leaves").update(data).eq("id", leave_id).execute()
    return res.data[0] if res.data else None

@router.delete("/{leave_id}")
def delete_leave(leave_id: str, admin=Depends(get_admin_user), supabase=Depends(get_supabase)):
    supabase.table("planned_leaves").delete().eq("id", leave_id).execute()
    return {"msg": "Deleted"}
