import os
import sys
from dotenv import load_dotenv
from supabase import create_client

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


def setup_admin():
    supabase_url = os.environ.get("SUPABASE_URL", "")
    supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")

    if not supabase_url or not supabase_key:
        print("ERROR: Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY")
        sys.exit(1)

    supabase = create_client(supabase_url, supabase_key)

    MOBILE = "8189844814"
    EMAIL = f"{MOBILE}@shiftapp.local"
    PASSWORD = "Satz@5517"

    print(f"Setting up admin account for mobile: {MOBILE}")

    user_id = None

    # Step 1: Try to create the auth user
    try:
        auth_res = supabase.auth.admin.create_user({
            "email": EMAIL,
            "password": PASSWORD,
            "email_confirm": True,
            "phone_confirm": True,
        })
        user_id = auth_res.user.id
        print(f"[OK] Auth user created (ID: {user_id})")
    except Exception as e:
        print(f"Auth user creation returned: {e}")
        print("Trying to find existing user...")

        # Look up user by listing all users
        try:
            users_response = supabase.auth.admin.list_users()
            # The response could be a list or have a .users attribute
            users_list = users_response
            if hasattr(users_response, 'users'):
                users_list = users_response.users

            for u in users_list:
                user_email = getattr(u, 'email', None)
                if user_email == EMAIL:
                    user_id = u.id
                    print(f"[OK] Found existing user (ID: {user_id})")
                    # Update password just in case
                    try:
                        supabase.auth.admin.update_user_by_id(str(user_id), {"password": PASSWORD})
                        print("[OK] Password updated")
                    except Exception:
                        pass
                    break
        except Exception as e2:
            print(f"ERROR listing users: {e2}")
            sys.exit(1)

    if not user_id:
        print("ERROR: Could not obtain user ID")
        sys.exit(1)

    # Step 2: Create/update profile
    try:
        profile_data = {
            "id": str(user_id),
            "full_name": "Admin",
            "mobile_number": MOBILE,
            "role": "admin",
            "is_active": True,
        }
        supabase.table("profiles").upsert(profile_data).execute()
        print("[OK] Admin profile created/updated successfully")
    except Exception as e:
        print(f"ERROR creating profile: {e}")
        sys.exit(1)

    print("")
    print("=" * 50)
    print("ADMIN ACCOUNT READY")
    print(f"  Mobile: {MOBILE}")
    print(f"  Password: {PASSWORD}")
    print("=" * 50)


if __name__ == "__main__":
    setup_admin()
