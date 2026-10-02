from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import time

from app.dependencies import get_supabase, get_admin_user, get_current_user

router = APIRouter(prefix="/api/shifts", tags=["shifts"])

class ShiftCreate(BaseModel):
    name: str
    start_time: time
    end_time: time
    display_order: int

class ShiftUpdate(BaseModel):
    name: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    display_order: Optional[int] = None

@router.get("")
def list_shifts(user=Depends(get_current_user), supabase=Depends(get_supabase)):
    res = supabase.table("shifts").select("*").order("display_order").execute()
    return res.data

@router.post("")
def create_shift(shift: ShiftCreate, admin=Depends(get_admin_user), supabase=Depends(get_supabase)):
    data = shift.model_dump()
    data["start_time"] = str(data["start_time"])
    data["end_time"] = str(data["end_time"])
    res = supabase.table("shifts").insert(data).execute()
    return res.data[0] if res.data else None

@router.put("/{shift_id}")
def update_shift(shift_id: str, shift: ShiftUpdate, admin=Depends(get_admin_user), supabase=Depends(get_supabase)):
    data = shift.model_dump(exclude_unset=True)
    if "start_time" in data:
        data["start_time"] = str(data["start_time"])
    if "end_time" in data:
        data["end_time"] = str(data["end_time"])
    res = supabase.table("shifts").update(data).eq("id", shift_id).execute()
    return res.data[0] if res.data else None

@router.delete("/{shift_id}")
def delete_shift(shift_id: str, admin=Depends(get_admin_user), supabase=Depends(get_supabase)):
    supabase.table("shifts").delete().eq("id", shift_id).execute()
    return {"msg": "Deleted"}
