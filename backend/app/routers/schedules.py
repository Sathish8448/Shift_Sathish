from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from datetime import date, datetime
import pytz

from app.dependencies import get_supabase, get_admin_user, get_current_user

router = APIRouter(prefix="/api/schedules", tags=["schedules"])

class ScheduleCreate(BaseModel):
    user_id: str
    shift_id: str
    schedule_date: date
    notes: Optional[str] = None

class ScheduleUpdate(BaseModel):
    shift_id: Optional[str] = None
    notes: Optional[str] = None

class ImportItem(BaseModel):
    user_id: str
    shift_id: str
    schedule_date: date
    month_year: str

class ImportConfirm(BaseModel):
    items: List[ImportItem]
    
class ParseRequest(BaseModel):
    content: str

@router.get("")
def list_schedules(month_year: Optional[str] = None, user=Depends(get_current_user), supabase=Depends(get_supabase)):
    query = supabase.table("schedules").select("*")
    if month_year:
        query = query.eq("month_year", month_year)
    res = query.execute()
    return res.data

@router.get("/today")
def get_today_schedule(user=Depends(get_current_user), supabase=Depends(get_supabase)):
    ist = pytz.timezone('Asia/Kolkata')
    today = datetime.now(ist).date().isoformat()
    res = supabase.table("schedules").select("*").eq("schedule_date", today).execute()
    return res.data

@router.get("/date/{date_str}")
def get_date_schedule(date_str: str, user=Depends(get_current_user), supabase=Depends(get_supabase)):
    res = supabase.table("schedules").select("*").eq("schedule_date", date_str).execute()
    return res.data

@router.post("")
def create_schedule(sched: ScheduleCreate, admin=Depends(get_admin_user), supabase=Depends(get_supabase)):
    month_year = sched.schedule_date.strftime("%Y-%m")
    data = sched.model_dump()
    data["schedule_date"] = str(data["schedule_date"])
    data["month_year"] = month_year
    res = supabase.table("schedules").insert(data).execute()
    return res.data[0] if res.data else None

@router.put("/{schedule_id}")
def update_schedule(schedule_id: str, sched: ScheduleUpdate, admin=Depends(get_admin_user), supabase=Depends(get_supabase)):
    data = sched.model_dump(exclude_unset=True)
    res = supabase.table("schedules").update(data).eq("id", schedule_id).execute()
    return res.data[0] if res.data else None

@router.delete("/{schedule_id}")
def delete_schedule(schedule_id: str, admin=Depends(get_admin_user), supabase=Depends(get_supabase)):
    supabase.table("schedules").delete().eq("id", schedule_id).execute()
    return {"msg": "Deleted"}

@router.post("/import/parse")
def parse_import(payload: ParseRequest, admin=Depends(get_admin_user)):
    from app.services.schedule_parser import parse_schedules
    return parse_schedules(payload.content)

@router.post("/import/confirm")
def confirm_import(payload: ImportConfirm, admin=Depends(get_admin_user), supabase=Depends(get_supabase)):
    items = [item.model_dump() for item in payload.items]
    for item in items:
        item["schedule_date"] = str(item["schedule_date"])
    res = supabase.table("schedules").upsert(items, on_conflict="user_id, schedule_date").execute()
    return {"inserted": len(items)}
