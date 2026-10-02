from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel

# Assuming common dependency injection paths
from app.dependencies import get_supabase, get_admin_user, get_current_user

router = APIRouter(prefix="/api/users", tags=["users"])

class UserCreate(BaseModel):
    full_name: str
    mobile_number: str
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

class PasswordReset(BaseModel):
    new_password: str

@router.post("")
def create_user(user: UserCreate, admin=Depends(get_admin_user), supabase=Depends(get_supabase)):
    email = f"{user.mobile_number}@shiftapp.local"
    try:
        auth_user = supabase.auth.admin.create_user({
            "email": email,
            "password": user.password,
            "email_confirm": True,
            "phone_confirm": True
        })
        user_id = auth_user.user.id
        
        profile_data = {
            "id": user_id,
            "full_name": user.full_name,
            "mobile_number": user.mobile_number,
            "role": "user"
        }
        res = supabase.table("profiles").insert(profile_data).execute()
        return res.data[0] if res.data else None
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("")
def list_users(admin=Depends(get_admin_user), supabase=Depends(get_supabase)):
    res = supabase.table("profiles").select("*").execute()
    return res.data

@router.patch("/{user_id}")
def update_user(user_id: str, user: UserUpdate, admin=Depends(get_admin_user), supabase=Depends(get_supabase)):
    update_data = user.model_dump(exclude_unset=True)
    if not update_data:
        return {"msg": "No fields to update"}
    res = supabase.table("profiles").update(update_data).eq("id", user_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="User not found")
    return res.data[0]

@router.post("/{user_id}/reset-password")
def reset_password(user_id: str, payload: PasswordReset, admin=Depends(get_admin_user), supabase=Depends(get_supabase)):
    try:
        supabase.auth.admin.update_user_by_id(user_id, {"password": payload.new_password})
        return {"msg": "Password reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{user_id}/deactivate")
def deactivate_user(user_id: str, admin=Depends(get_admin_user), supabase=Depends(get_supabase)):
    res = supabase.table("profiles").update({"is_active": False}).eq("id", user_id).execute()
    return res.data[0] if res.data else None

@router.patch("/{user_id}/activate")
def activate_user(user_id: str, admin=Depends(get_admin_user), supabase=Depends(get_supabase)):
    res = supabase.table("profiles").update({"is_active": True}).eq("id", user_id).execute()
    return res.data[0] if res.data else None
