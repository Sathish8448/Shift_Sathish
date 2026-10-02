from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
import pytz

from app.dependencies import get_supabase, get_admin_user, get_current_user

router = APIRouter(prefix="/api/visitors", tags=["visitors"])

@router.post("/track")
def track_visit(user=Depends(get_current_user), supabase=Depends(get_supabase)):
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    thirty_mins_ago = now - timedelta(minutes=30)
    
    recent = supabase.table("visitor_logs").select("*") \
        .eq("user_id", user["id"]) \
        .gte("visited_at", thirty_mins_ago.isoformat()) \
        .execute()
        
    if recent.data:
        return {"msg": "Already tracked recently", "log": recent.data[0]}
        
    log_data = {
        "user_id": user["id"],
        "visited_at": now.isoformat(),
        "visit_date": now.date().isoformat()
    }
    res = supabase.table("visitor_logs").insert(log_data).execute()
    return res.data[0] if res.data else None

@router.get("/today")
def get_today_visitors(admin=Depends(get_admin_user), supabase=Depends(get_supabase)):
    ist = pytz.timezone('Asia/Kolkata')
    today = datetime.now(ist).date().isoformat()
    
    res = supabase.table("visitor_logs").select("*, profiles(full_name)").eq("visit_date", today).execute()
    return res.data

@router.get("/stats")
def get_visitor_stats(admin=Depends(get_admin_user), supabase=Depends(get_supabase)):
    res = supabase.table("visitor_logs").select("*, profiles(full_name)").execute()
    stats = {}
    for row in res.data:
        uid = row["user_id"]
        if uid not in stats:
            stats[uid] = {
                "user_id": uid,
                "full_name": row.get("profiles", {}).get("full_name"),
                "visits": 0
            }
        stats[uid]["visits"] += 1
    return list(stats.values())
