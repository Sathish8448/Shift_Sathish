from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.supabase_admin import supabase as admin_supabase

security = HTTPBearer()


def get_supabase():
    """Provide the Supabase admin client as a dependency."""
    return admin_supabase


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Validate JWT token and return user profile dict."""
    token = credentials.credentials
    try:
        res = admin_supabase.auth.get_user(token)
        if not res or not res.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired session. Please log in again."
            )
        # Fetch profile
        profile = admin_supabase.table("profiles").select("*").eq("id", res.user.id).single().execute()
        if not profile.data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User profile not found."
            )
        if not profile.data.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your account has been deactivated. Contact admin."
            )
        return profile.data
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session. Please log in again."
        )


def get_admin_user(user=Depends(get_current_user)):
    """Ensure the current user is an admin."""
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    return user
