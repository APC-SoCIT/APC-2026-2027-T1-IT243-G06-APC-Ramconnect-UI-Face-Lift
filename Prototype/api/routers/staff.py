from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from ..schemas import ApplicationUpdateStatus, SiteSettingsSchema, FormSectionSchema, CourseSchema
from ..database import DB

router = APIRouter(prefix="/staff", tags=["Staff Management"])

@router.get("/stats")
def get_dashboard_stats():
    total_inquiries = len(DB["inquiries"])
    new_inquiries = len([i for i in DB["inquiries"] if i.get("status") == "New"])
    total_apps = len(DB["applications"])
    qualified_apps = len([a for a in DB["applications"] if a.get("status") == "Qualified"])
    enrolled_apps = len([a for a in DB["applications"] if a.get("status") == "Enrolled"])
    return {
        "total_inquiries": total_inquiries,
        "new_inquiries": new_inquiries,
        "total_applications": total_apps,
        "qualified_applications": qualified_apps,
        "enrolled_applications": enrolled_apps
    }

@router.get("/applicants")
def list_applicants(query: Optional[str] = None, status: Optional[str] = None):
    results = DB["applications"]
    if status and status != "All":
        results = [a for a in results if a.get("status") == status]
    if query:
        q = query.lower()
        results = [
            a for a in results
            if q in a.get("first_name", "").lower()
            or q in a.get("last_name", "").lower()
            or q in a.get("email", "").lower()
            or q in a.get("course_id", "").lower()
            or q in a.get("course_name", "").lower()
        ]
    return results

@router.patch("/applicants/{app_id}/status")
def update_applicant_status(app_id: str, req: ApplicationUpdateStatus):
    for a in DB["applications"]:
        if a["appform_id"] == app_id:
            a["status"] = req.status
            if req.officer_notes:
                a["officer_notes"] = req.officer_notes
            return {"message": "Status updated successfully", "application": a}
    raise HTTPException(status_code=404, detail="Application not found")

@router.put("/settings")
def update_site_settings(settings: SiteSettingsSchema):
    DB["settings"].update(settings.model_dump())
    return {"message": "Site settings updated", "settings": DB["settings"]}

@router.put("/form-builder")
def update_form_builder(sections: List[Dict[str, Any]]):
    DB["sections"] = sections
    return {"message": "Form structure published successfully", "sections": DB["sections"]}

@router.put("/courses/{course_id}")
def update_course(course_id: str, course_data: Dict[str, Any]):
    for c in DB["courses"]:
        if c["id"] == course_id:
            c.update(course_data)
            return {"message": "Course updated", "course": c}
    raise HTTPException(status_code=404, detail="Course not found")

@router.post("/courses")
def add_course(course_data: Dict[str, Any]):
    DB["courses"].append(course_data)
    return {"message": "Course added", "course": course_data}
