from fastapi import APIRouter, Depends
from app.dependencies import get_supabase, get_admin_user

router = APIRouter(prefix="/api/messages", tags=["messages"])

@router.delete("/{message_id}")
def delete_message(message_id: str, admin=Depends(get_admin_user), supabase=Depends(get_supabase)):
    supabase.table("messages").delete().eq("id", message_id).execute()
    return {"msg": "Deleted"}
