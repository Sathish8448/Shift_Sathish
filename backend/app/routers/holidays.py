from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import date
from typing import Optional

from app.dependencies import get_supabase, get_admin_user, get_current_user

router = APIRouter(prefix="/api/holidays", tags=["holidays"])

class HolidayCreate(BaseModel):
    holiday_date: date
    name: str

class HolidayUpdate(BaseModel):
    holiday_date: Optional[date] = None
    name: Optional[str] = None

@router.get("")
def list_holidays(user=Depends(get_current_user), supabase=Depends(get_supabase)):
    res = supabase.table("public_holidays").select("*").execute()
    return res.data

@router.post("")
def create_holiday(holiday: HolidayCreate, admin=Depends(get_admin_user), supabase=Depends(get_supabase)):
    data = holiday.model_dump()
    data["holiday_date"] = str(data["holiday_date"])
    res = supabase.table("public_holidays").insert(data).execute()
    return res.data[0] if res.data else None

@router.put("/{holiday_id}")
def update_holiday(holiday_id: str, holiday: HolidayUpdate, admin=Depends(get_admin_user), supabase=Depends(get_supabase)):
    data = holiday.model_dump(exclude_unset=True)
    if "holiday_date" in data:
        data["holiday_date"] = str(data["holiday_date"])
    res = supabase.table("public_holidays").update(data).eq("id", holiday_id).execute()
    return res.data[0] if res.data else None

@router.delete("/{holiday_id}")
def delete_holiday(holiday_id: str, admin=Depends(get_admin_user), supabase=Depends(get_supabase)):
    supabase.table("public_holidays").delete().eq("id", holiday_id).execute()
    return {"msg": "Deleted"}
