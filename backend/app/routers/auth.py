from fastapi import APIRouter, Depends
from app.dependencies import get_supabase, get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.get("/me")
def get_me(user=Depends(get_current_user), supabase=Depends(get_supabase)):
    res = supabase.table("profiles").select("*").eq("id", user["id"]).execute()
    if res.data:
        return res.data[0]
    return user
