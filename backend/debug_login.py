import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

supabase_url = os.environ.get("SUPABASE_URL")
service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
anon_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpzamVwenRreXFveGV6ZmNvdWtzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTAwOTE2NTUsImV4cCI6MjEwNTY2NzY1NX0.66Bn2DNb622x6tGJC2P7IHfY21Wo5qVZf_ZIkHwhcfs"

print("=== Step 1: List users via admin API ===")
admin_client = create_client(supabase_url, service_key)

try:
    users = admin_client.auth.admin.list_users()
    for u in users:
        print(f"  User: {u.email} | confirmed: {u.email_confirmed_at} | id: {u.id}")
except Exception as e:
    print(f"  Error listing users: {e}")

print("\n=== Step 2: Try login with anon key ===")
anon_client = create_client(supabase_url, anon_key)
try:
    res = anon_client.auth.sign_in_with_password({
        "email": "8189844814@shiftapp.local",
        "password": "Satz@5517"
    })
    print(f"  SUCCESS! User: {res.user.email}, ID: {res.user.id}")
except Exception as e:
    print(f"  Login error: {e}")

print("\n=== Step 3: Reset password via admin ===")
try:
    users = admin_client.auth.admin.list_users()
    for u in users:
        if u.email == "8189844814@shiftapp.local":
            admin_client.auth.admin.update_user_by_id(str(u.id), {
                "password": "Satz@5517",
                "email_confirm": True
            })
            print(f"  Password reset and email confirmed for {u.email}")
            break
except Exception as e:
    print(f"  Error: {e}")

print("\n=== Step 4: Retry login ===")
anon_client2 = create_client(supabase_url, anon_key)
try:
    res = anon_client2.auth.sign_in_with_password({
        "email": "8189844814@shiftapp.local",
        "password": "Satz@5517"
    })
    print(f"  SUCCESS! User: {res.user.email}, ID: {res.user.id}")
except Exception as e:
    print(f"  Login error: {e}")
