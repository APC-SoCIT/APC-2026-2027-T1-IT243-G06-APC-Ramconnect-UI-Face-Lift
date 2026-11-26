import re
import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from ..schemas import ApplicationCreate, PaymentSubmit
from ..database import DB, supabase_admin, get_supabase_db, create_anon_client
from .auth import create_mock_token, get_current_user

router = APIRouter(prefix="/applications", tags=["Applications"])


def _build_default_password(first_name: str, last_name: str, birth_date: Optional[str]) -> str:
    """Build applicant default password: lowercase(firstname + lastname) + birth_year."""
    if not birth_date:
        raise HTTPException(status_code=400, detail="Date of birth is required to generate your applicant account.")
    match = re.search(r"(\d{4})", birth_date)
    if not match:
        raise HTTPException(status_code=400, detail="Invalid date of birth format.")
    clean_name = re.sub(r"\s+", "", f"{first_name}{last_name}").lower()
    if not clean_name:
        raise HTTPException(status_code=400, detail="First name and last name are required.")
    return f"{clean_name}{match.group(1)}"


def _extract_acad_term(req: ApplicationCreate) -> tuple[str, str]:
    acad_term = (req.answers or {}).get("acad_term", "")
    if "," in acad_term:
        year_part, term_part = [p.strip() for p in acad_term.split(",", 1)]
        year_part = year_part.replace("AY ", "").strip()
        return year_part or req.acad_year, term_part or req.term
    return req.acad_year, req.term


def _email_exists(email: str) -> bool:
    client = get_supabase_db()
    if client:
        try:
            u_res = client.table("users").select("id").ilike("email", email).limit(1).execute()
            if u_res.data:
                return True
            a_res = client.table("applications").select("appform_id").ilike("email", email).limit(1).execute()
            if a_res.data:
                return True
        except Exception:
            pass
    for u in DB["users"]:
        if u["email"].lower() == email.lower():
            return True
    for a in DB["applications"]:
        if a["email"].lower() == email.lower():
            return True
    return False


@router.post("")
def submit_application(req: ApplicationCreate):
    email_clean = req.email.strip()

    # UC-APP-02 Ext 4a: Block duplicate email registration
    if _email_exists(email_clean):
        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists. Please log in instead."
        )

    default_password = _build_default_password(req.first_name, req.last_name, req.birth_date)
    full_name = " ".join(part for part in [req.first_name.strip(), req.last_name.strip()] if part)
    acad_year, term = _extract_acad_term(req)

    # Lookup course title
    course_name = req.course_id
    for c in DB["courses"]:
        if c["id"] == req.course_id:
            course_name = c["name"]
            break

    user_id = str(uuid.uuid4())
    session_token = None
    db_client = get_supabase_db()

    # Create user in Supabase Auth + public.users when Supabase is configured
    if supabase_admin:
        try:
            created = supabase_admin.auth.admin.create_user({
                "email": email_clean,
                "password": default_password,
                "email_confirm": True,
                "user_metadata": {"full_name": full_name, "role": "applicant"}
            })
            if created and created.user:
                user_id = str(created.user.id)
        except Exception as e:
            err_msg = str(e).lower()
            if "already" in err_msg or "registered" in err_msg or "exists" in err_msg:
                raise HTTPException(
                    status_code=409,
                    detail="An account with this email already exists. Please log in instead."
                )
            raise HTTPException(status_code=500, detail=f"Failed to create Supabase user: {e}")

        # Ensure public.users row exists for FK + role lookups
        try:
            supabase_admin.table("users").upsert({
                "id": user_id,
                "email": email_clean,
                "full_name": full_name,
                "role": "applicant",
                "password_hash": "supabase_auth"
            }, on_conflict="email").execute()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save user profile in Supabase: {e}")

        auth_client = create_anon_client()
        if auth_client:
            try:
                auth_res = auth_client.auth.sign_in_with_password({"email": email_clean, "password": default_password})
                if auth_res and auth_res.session:
                    session_token = auth_res.session.access_token
            except Exception:
                pass
    else:
        auth_client = create_anon_client()
        if auth_client:
            try:
                signup_res = auth_client.auth.sign_up({
                    "email": email_clean,
                    "password": default_password,
                    "options": {"data": {"full_name": full_name, "role": "applicant"}}
                })
                if signup_res and signup_res.user:
                    # Supabase returns empty identities if user already exists when confirmation is on
                    identities = getattr(signup_res.user, "identities", None)
                    if identities is not None and len(identities) == 0:
                        raise HTTPException(
                            status_code=409,
                            detail="An account with this email already exists. Please log in instead."
                        )
                    user_id = str(signup_res.user.id)
                    if signup_res.session:
                        session_token = signup_res.session.access_token
            except HTTPException:
                raise
            except Exception as e:
                err_msg = str(e).lower()
                if "already" in err_msg or "registered" in err_msg:
                    raise HTTPException(
                        status_code=409,
                        detail="An account with this email already exists. Please log in instead."
                    )
                raise HTTPException(status_code=500, detail=f"Failed to register Supabase user: {e}")

    app_id = str(uuid.uuid4())
    payment_amount = float(DB["settings"].get("reservation_fee", 5000.00))
    now_iso = datetime.now().isoformat()

    new_app = {
        "appform_id": app_id,
        "user_id": user_id,
        "course_id": req.course_id,
        "course_name": course_name,
        "email": email_clean,
        "first_name": req.first_name.strip(),
        "middle_name": req.middle_name or "",
        "last_name": req.last_name.strip(),
        "mobile": req.mobile.strip(),
        "entry_status": req.entry_status,
        "acad_year": acad_year,
        "term": term,
        "birth_date": req.birth_date,
        "sex": req.sex,
        "nationality": req.nationality,
        "region": req.region or "",
        "city": req.city or "",
        "barangay": req.barangay or "",
        "home_address": req.home_address or "",
        "zip_code": req.zip_code or "",
        "prev_school": req.prev_school or "",
        "prev_school_sector": req.prev_school_sector or "Private",
        "prev_school_year": req.prev_school_year or "",
        "answers": req.answers or {},
        "status": "Submitted",
        "officer_notes": "Application received and queued for admission review.",
        "payment_amount": payment_amount,
    }

    # Persist application in Supabase when configured
    if db_client:
        try:
            res = db_client.table("applications").insert(new_app).execute()
            if res.data:
                new_app = res.data[0]
                app_id = new_app.get("appform_id", app_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save application in Supabase: {e}")

    new_app.setdefault("created_at", now_iso)

    # Mirror in local DB for in-memory fallback consistency
    DB["users"].append({
        "id": user_id,
        "email": email_clean,
        "full_name": full_name,
        "role": "applicant",
        "password": default_password
    })
    DB["applications"].insert(0, new_app)

    if not session_token:
        session_token = create_mock_token(user_id, email_clean, "applicant")

    return {
        "message": "Application submitted successfully.",
        "appform_id": app_id,
        "application": new_app,
        "default_password": default_password,
        "user": {
            "id": user_id,
            "email": email_clean,
            "full_name": full_name,
            "role": "applicant",
            "token": session_token
        }
    }


@router.get("/my")
def get_my_application(email: Optional[str] = None, authorization: Optional[str] = Header(None)):
    target_email = email.strip() if email else None
    if not target_email and authorization:
        try:
            u = get_current_user(authorization)
            target_email = u.get("email")
        except HTTPException:
            pass

    if not target_email:
        raise HTTPException(status_code=400, detail="Applicant email or authentication is required.")

    client = get_supabase_db()
    if client:
        try:
            res = (
                client.table("applications")
                .select("*")
                .ilike("email", target_email)
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )
            if res.data:
                return res.data[0]
        except Exception:
            pass

    for a in DB["applications"]:
        if a["email"].lower() == target_email.lower():
            return a

    raise HTTPException(status_code=404, detail="No active application found")


@router.get("/{app_id}")
def get_application(app_id: str):
    client = get_supabase_db()
    if client:
        try:
            res = client.table("applications").select("*").eq("appform_id", app_id).limit(1).execute()
            if res.data:
                return res.data[0]
        except Exception:
            pass
    for a in DB["applications"]:
        if a["appform_id"] == app_id:
            return a
    raise HTTPException(status_code=404, detail="Application not found")


@router.post("/{app_id}/pay")
def pay_reservation_fee(app_id: str, payment: PaymentSubmit):
    target = None
    for a in DB["applications"]:
        if a["appform_id"] == app_id:
            target = a
            break

    client = get_supabase_db()
    if not target and client:
        try:
            res = client.table("applications").select("*").eq("appform_id", app_id).limit(1).execute()
            if res.data:
                target = res.data[0]
        except Exception:
            pass

    if not target:
        raise HTTPException(status_code=404, detail="Application not found")

    if target.get("status") not in ["Qualified", "Under Review", "Submitted"]:
        raise HTTPException(status_code=400, detail="Application is not qualified for payment.")

    clean_first = target["first_name"][0].lower() if target.get("first_name") else "s"
    clean_last = target["last_name"].replace(" ", "").lower() if target.get("last_name") else "student"
    domain = DB["settings"].get("student_email_domain", "student.apc.edu.ph")
    now_iso = datetime.now().isoformat()

    updates = {
        "payment_bank": payment.bank,
        "payment_account_name": payment.account_name,
        "payment_account_last4": payment.account_last4,
        "payment_reference": payment.reference_number,
        "paid_at": now_iso,
        "status": "Enrolled",
        "student_id": f"2026-{uuid.uuid4().int % 90000 + 10000}",
        "student_email": f"{clean_first}{clean_last}@{domain}",
        "transferred_at": now_iso,
        "officer_notes": "Payment verified. Official student profile synchronized with RAMPortal."
    }
    target.update(updates)

    if client:
        try:
            res = client.table("applications").update(updates).eq("appform_id", app_id).execute()
            if res.data:
                target = res.data[0]
        except Exception:
            pass

    return {
        "message": "Payment verified and enrollment confirmed!",
        "student_id": target["student_id"],
        "student_email": target["student_email"],
        "application": target
    }
