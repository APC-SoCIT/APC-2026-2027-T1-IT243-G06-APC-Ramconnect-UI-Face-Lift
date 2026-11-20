import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from ..schemas import InquiryCreate, InquiryNoteCreate, InquiryUpdateStatus
from ..database import DB
from .auth import get_current_user

router = APIRouter(prefix="/inquiries", tags=["Inquiries CRM"])

@router.post("")
def create_inquiry(req: InquiryCreate):
    new_id = f"INQ-{uuid.uuid4().hex[:6].upper()}"
    inquiry_record = {
        "inquiry_id": new_id,
        "first_name": req.first_name,
        "last_name": req.last_name,
        "email": req.email,
        "mobile": req.mobile,
        "guardian_name": req.guardian_name,
        "guardian_contact": req.guardian_contact,
        "program_interest": req.program_interest,
        "visit_mode": req.visit_mode,
        "preferred_date": req.preferred_date,
        "question": req.question,
        "status": "New",
        "created_at": datetime.now().isoformat(),
        "notes": []
    }
    DB["inquiries"].insert(0, inquiry_record)
    return {
        "message": "Inquiry submitted successfully.",
        "reference_id": new_id,
        "inquiry": inquiry_record
    }

@router.get("")
def list_inquiries(status: Optional[str] = None):
    results = DB["inquiries"]
    if status and status != "All":
        results = [i for i in results if i.get("status") == status]
    return results

@router.patch("/{inquiry_id}/status")
def update_inquiry_status(inquiry_id: str, req: InquiryUpdateStatus):
    for i in DB["inquiries"]:
        if i["inquiry_id"] == inquiry_id:
            i["status"] = req.status
            return {"message": "Status updated", "inquiry": i}
    raise HTTPException(status_code=404, detail="Inquiry not found")

@router.post("/{inquiry_id}/notes")
def add_inquiry_note(inquiry_id: str, req: InquiryNoteCreate):
    for i in DB["inquiries"]:
        if i["inquiry_id"] == inquiry_id:
            note = {
                "note_id": str(uuid.uuid4()),
                "author_name": "Admissions Officer",
                "comment": req.comment,
                "created_at": datetime.now().isoformat()
            }
            if "notes" not in i:
                i["notes"] = []
            i["notes"].append(note)
            return {"message": "Note added", "note": note}
    raise HTTPException(status_code=404, detail="Inquiry not found")
