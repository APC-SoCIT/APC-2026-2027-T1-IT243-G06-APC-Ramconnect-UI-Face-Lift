from fastapi import APIRouter
from typing import List, Dict, Any
from ..database import DB, supabase

router = APIRouter(prefix="/public", tags=["Public CMS Data"])

@router.get("/settings")
def get_site_settings():
    return DB["settings"]

@router.get("/courses")
def get_courses():
    return [c for c in DB["courses"] if c.get("active", True)]

@router.get("/milestones")
def get_milestones():
    return sorted(DB["milestones"], key=lambda x: x.get("sort_order", 0))

@router.get("/promos")
def get_promos():
    return sorted([p for p in DB["promos"] if p.get("promo_active_status", True)], key=lambda x: x.get("promo_sort_order", 0))

@router.get("/form-schema")
def get_form_schema():
    return sorted(DB["sections"], key=lambda x: x.get("sort_order", 0))
