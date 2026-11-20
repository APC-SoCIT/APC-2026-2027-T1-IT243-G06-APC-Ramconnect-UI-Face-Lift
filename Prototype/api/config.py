import os

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", os.getenv("SUPABASE_ANON_KEY", ""))
JWT_SECRET = os.getenv("JWT_SECRET", "apc-ramconnect-secret-key-2026")
JWT_ALGORITHM = "HS256"
