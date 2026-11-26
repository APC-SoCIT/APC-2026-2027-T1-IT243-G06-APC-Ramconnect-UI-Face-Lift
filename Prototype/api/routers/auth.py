import uuid
from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional
from ..schemas import LoginRequest, RegisterRequest, UserResponse
from ..database import DB, supabase, get_supabase_db, create_anon_client

router = APIRouter(prefix="/auth", tags=["Authentication"])


def create_mock_token(user_id: str, email: str, role: str) -> str:
    return f"token_{user_id}_{role}"


def _lookup_public_user(email: str) -> Optional[dict]:
    client = get_supabase_db()
    if not client:
        return None
    try:
        res = client.table("users").select("id, email, full_name, role").ilike("email", email).limit(1).execute()
        if res.data:
            return res.data[0]
    except Exception:
        pass
    return None


def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    if not authorization:
        raise HTTPException(status_code=401, detail="Authentication required")
    token = authorization.replace("Bearer ", "").strip()
    if token.startswith("token_"):
        parts = token.split("_")
        if len(parts) >= 3:
            u_id, role = parts[1], "_".join(parts[2:])
            for u in DB["users"]:
                if u["id"] == u_id:
                    return u
            return {"id": u_id, "role": role, "email": "user@apc.edu.ph", "full_name": "Authenticated User"}
    if supabase and token:
        try:
            res = supabase.auth.get_user(token)
            if res and res.user:
                profile = _lookup_public_user(res.user.email)
                meta = res.user.user_metadata or {}
                return {
                    "id": str(res.user.id),
                    "email": res.user.email,
                    "role": (profile or {}).get("role") or meta.get("role") or "applicant",
                    "full_name": (profile or {}).get("full_name") or meta.get("full_name") or res.user.email,
                }
        except Exception:
            pass
    raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/login", response_model=UserResponse)
def login(req: LoginRequest):
    email_clean = req.email.strip()

    # 1. Try Supabase Auth first using an isolated client
    auth_client = create_anon_client()
    if auth_client:
        try:
            auth_res = auth_client.auth.sign_in_with_password({"email": email_clean, "password": req.password})
            if auth_res and auth_res.user and auth_res.session:
                profile = _lookup_public_user(auth_res.user.email)
                meta = auth_res.user.user_metadata or {}
                role = (profile or {}).get("role") or meta.get("role") or (
                    "admission_officer" if email_clean.lower().endswith("@apc.edu.ph") else "applicant"
                )
                full_name = (profile or {}).get("full_name") or meta.get("full_name") or email_clean.split("@")[0]
                return UserResponse(
                    id=str(auth_res.user.id),
                    email=auth_res.user.email,
                    full_name=full_name,
                    role=role,
                    token=auth_res.session.access_token
                )
        except Exception as e:
            err_msg = str(e).lower()
            if "email not confirmed" in err_msg:
                raise HTTPException(status_code=403, detail="Email not confirmed. Check your inbox or configure SUPABASE_SERVICE_ROLE_KEY.")

    # 2. Check local seeded / fallback DB users
    for u in DB["users"]:
        if u["email"].lower() == email_clean.lower():
            if u["password"] == req.password:
                token = create_mock_token(u["id"], u["email"], u["role"])
                return UserResponse(
                    id=u["id"],
                    email=u["email"],
                    full_name=u["full_name"],
                    role=u["role"],
                    token=token
                )
            raise HTTPException(status_code=401, detail="Invalid email or password.")

    raise HTTPException(status_code=401, detail="Invalid email or password.")


@router.post("/register", response_model=UserResponse)
def register(req: RegisterRequest):
    email_clean = req.email.strip()
    if _lookup_public_user(email_clean):
        raise HTTPException(status_code=409, detail="An account with this email already exists.")
    for u in DB["users"]:
        if u["email"].lower() == email_clean.lower():
            raise HTTPException(status_code=409, detail="An account with this email already exists.")

    new_id = str(uuid.uuid4())
    role = "admission_officer" if email_clean.lower().endswith("@apc.edu.ph") else "applicant"
    new_user = {
        "id": new_id,
        "email": email_clean,
        "full_name": req.full_name,
        "role": role,
        "password": req.password
    }
    DB["users"].append(new_user)
    token = create_mock_token(new_id, email_clean, role)
    return UserResponse(id=new_id, email=email_clean, full_name=req.full_name, role=role, token=token)


@router.get("/me", response_model=UserResponse)
def get_me(user: dict = Depends(get_current_user)):
    return UserResponse(
        id=user.get("id"),
        email=user.get("email"),
        full_name=user.get("full_name", user.get("email")),
        role=user.get("role", "applicant")
    )
