import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from ..schemas import ApplicationCreate, PaymentSubmit
from ..database import DB
from .auth import get_current_user

router = APIRouter(prefix="/applications", tags=["Applications"])

@router.post("")
def submit_application(req: ApplicationCreate):
    # Lookup course title
    course_name = req.course_id
    for c in DB["courses"]:
        if c["id"] == req.course_id:
            course_name = c["name"]
            break

    app_id = f"APP-{datetime.now().year}-{uuid.uuid4().hex[:5].upper()}"
    new_app = {
        "appform_id": app_id,
        "user_id": None,
        "course_id": req.course_id,
        "course_name": course_name,
        "email": req.email,
        "first_name": req.first_name,
        "middle_name": req.middle_name,
        "last_name": req.last_name,
        "mobile": req.mobile,
        "entry_status": req.entry_status,
        "acad_year": req.acad_year,
        "term": req.term,
        "birth_date": req.birth_date,
        "sex": req.sex,
        "nationality": req.nationality,
        "region": req.region,
        "city": req.city,
        "barangay": req.barangay,
        "home_address": req.home_address,
        "zip_code": req.zip_code,
        "prev_school": req.prev_school,
        "prev_school_sector": req.prev_school_sector,
        "prev_school_year": req.prev_school_year,
        "answers": req.answers,
        "status": "Submitted",
        "officer_notes": "Application received and queued for admission review.",
        "payment_amount": DB["settings"].get("reservation_fee", 5000.00),
        "created_at": datetime.now().isoformat()
    }
    
    # Check if a user with this email exists, link it
    for u in DB["users"]:
        if u["email"].lower() == req.email.lower():
            new_app["user_id"] = u["id"]
            break
    if not new_app["user_id"]:
        # Auto-create applicant user account so they can log in
        user_id = str(uuid.uuid4())
        DB["users"].append({
            "id": user_id,
            "email": req.email,
            "full_name": f"{req.first_name} {req.last_name}",
            "role": "applicant",
            "password": "user123"
        })
        new_app["user_id"] = user_id

    DB["applications"].insert(0, new_app)
    return {
        "message": "Application submitted successfully.",
        "appform_id": app_id,
        "application": new_app
    }

@router.get("/my")
def get_my_application(email: Optional[str] = None):
    # If email provided, filter by email, otherwise return the most recent active application
    if email:
        for a in DB["applications"]:
            if a["email"].lower() == email.lower():
                return a
    if DB["applications"]:
        return DB["applications"][0]
    raise HTTPException(status_code=404, detail="No active application found")

@router.get("/{app_id}")
def get_application(app_id: str):
    for a in DB["applications"]:
        if a["appform_id"] == app_id:
            return a
    raise HTTPException(status_code=404, detail="Application not found")

@router.post("/{app_id}/pay")
def pay_reservation_fee(app_id: str, payment: PaymentSubmit):
    for a in DB["applications"]:
        if a["appform_id"] == app_id:
            if a.get("status") not in ["Qualified", "Under Review", "Submitted"]:
                raise HTTPException(status_code=400, detail="Application is not qualified for payment.")
            
            # Update payment info
            a["payment_bank"] = payment.bank
            a["payment_account_name"] = payment.account_name
            a["payment_account_last4"] = payment.account_last4
            a["payment_reference"] = payment.reference_number
            a["paid_at"] = datetime.now().isoformat()
            a["status"] = "Enrolled"
            
            # Generate official institutional credentials
            # e.g., student ID: 2026-10823, email: jdelacruz@student.apc.edu.ph
            clean_first = a['first_name'][0].lower() if a['first_name'] else 's'
            clean_last = a['last_name'].replace(" ", "").lower() if a['last_name'] else 'student'
            domain = DB["settings"].get("student_email_domain", "student.apc.edu.ph")
            
            a["student_id"] = f"2026-{uuid.uuid4().int % 90000 + 10000}"
            a["student_email"] = f"{clean_first}{clean_last}@{domain}"
            a["transferred_at"] = datetime.now().isoformat()
            a["officer_notes"] = "Payment verified. Official student profile synchronized with RAMPortal."
            
            return {
                "message": "Payment verified and enrollment confirmed!",
                "student_id": a["student_id"],
                "student_email": a["student_email"],
                "application": a
            }
    raise HTTPException(status_code=404, detail="Application not found")
