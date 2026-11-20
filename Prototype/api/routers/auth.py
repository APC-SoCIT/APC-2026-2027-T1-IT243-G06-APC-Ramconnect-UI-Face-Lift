import uuid
from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional
from ..schemas import LoginRequest, RegisterRequest, UserResponse
from ..database import DB, supabase
from ..config import JWT_SECRET

router = APIRouter(prefix="/auth", tags=["Authentication"])

def create_mock_token(user_id: str, email: str, role: str) -> str:
    # Lightweight token format: "user_id:role:email" or base64 token
    return f"token_{user_id}_{role}"

def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    if not authorization:
        raise HTTPException(status_code=401, detail="Authentication required")
    token = authorization.replace("Bearer ", "").strip()
    if token.startswith("token_"):
        parts = token.split("_")
        if len(parts) >= 3:
            u_id, role = parts[1], parts[2]
            for u in DB["users"]:
                if u["id"] == u_id:
                    return u
            return {"id": u_id, "role": role, "email": "user@apc.edu.ph", "full_name": "Authenticated User"}
    # If using Supabase auth token
    if supabase and authorization:
        try:
            res = supabase.auth.get_user(token)
            if res and res.user:
                return {"id": res.user.id, "email": res.user.email, "role": "applicant", "full_name": res.user.email}
        except Exception:
            pass
    raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/login", response_model=UserResponse)
def login(req: LoginRequest):
    # Try Supabase if configured
    if supabase:
        try:
            auth_res = supabase.auth.sign_in_with_password({"email": req.email, "password": req.password})
            if auth_res.user:
                role = "applicant"
                if "apc.edu.ph" in req.email:
                    role = "admission_officer"
                return UserResponse(
                    id=str(auth_res.user.id),
                    email=auth_res.user.email,
                    full_name=auth_res.user.user_metadata.get("full_name", req.email.split("@")[0]),
                    role=role,
                    token=auth_res.session.access_token
                )
        except Exception:
            pass

    # Check local DB
    for u in DB["users"]:
        if u["email"].lower() == req.email.lower():
            if u["password"] == req.password:
                token = create_mock_token(u["id"], u["email"], u["role"])
                return UserResponse(
                    id=u["id"],
                    email=u["email"],
                    full_name=u["full_name"],
                    role=u["role"],
                    token=token
                )
            else:
                raise HTTPException(status_code=400, detail="Invalid password")
    
    # Auto-allow demo admission login if apc.edu.ph email
    if req.email.endswith("@apc.edu.ph"):
        new_u = {
            "id": f"u-{uuid.uuid4().hex[:8]}",
            "email": req.email,
            "full_name": req.email.split("@")[0].title() + " (Staff)",
            "role": "admission_officer",
            "password": req.password
        }
        DB["users"].append(new_u)
        token = create_mock_token(new_u["id"], new_u["email"], new_u["role"])
        return UserResponse(id=new_u["id"], email=new_u["email"], full_name=new_u["full_name"], role=new_u["role"], token=token)

    raise HTTPException(status_code=404, detail="User account not found. Please register first.")

@router.post("/register", response_model=UserResponse)
def register(req: RegisterRequest):
    # Check if duplicate email
    for u in DB["users"]:
        if u["email"].lower() == req.email.lower():
            raise HTTPException(status_code=400, detail="An account with this email already exists.")

    new_id = str(uuid.uuid4())
    role = "admission_officer" if req.email.endswith("@apc.edu.ph") else "applicant"
    new_user = {
        "id": new_id,
        "email": req.email,
        "full_name": req.full_name,
        "role": role,
        "password": req.password
    }
    DB["users"].append(new_user)
    token = create_mock_token(new_id, req.email, role)
    return UserResponse(id=new_id, email=req.email, full_name=req.full_name, role=role, token=token)

@router.get("/me", response_model=UserResponse)
def get_me(user: dict = Depends(get_current_user)):
    return UserResponse(
        id=user.get("id"),
        email=user.get("email"),
        full_name=user.get("full_name", user.get("email")),
        role=user.get("role", "applicant")
    )
