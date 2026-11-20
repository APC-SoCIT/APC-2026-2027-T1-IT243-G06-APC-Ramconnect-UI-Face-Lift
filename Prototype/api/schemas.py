from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# --- Auth Schemas ---
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: Optional[str] = "applicant"

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    token: Optional[str] = None

# --- Public & CMS Schemas ---
class SiteSettingsSchema(BaseModel):
    school_name: str = "Asia Pacific College"
    motto: str = "Industry. Integrity. Innovation."
    headline: str = "Your industry-based learning begins here!"
    welcome_title: str = "Welcome to Asia Pacific College!"
    welcome_text: str = "Your first step to dedication to improve your career starts here."
    schedule_title: str = "Important Admission Schedule"
    gold_color: str = "#FDB813"
    navy_color: str = "#0B1E3D"
    background_style: str = "mesh-gradient"
    hero_image: Optional[str] = ""
    footer_text: str = "© 2026-2027 Asia Pacific College. All rights reserved."
    privacy_notice: str = ""
    privacy_consent: str = ""
    reservation_fee: float = 5000.00
    student_email_domain: str = "student.apc.edu.ph"

class MilestoneSchema(BaseModel):
    id: Optional[str] = None
    date_text: str
    title: str
    description: Optional[str] = ""
    sort_order: int = 0

class PromoSchema(BaseModel):
    promo_id: Optional[str] = None
    promo_title: str
    promo_body: str
    promo_image: Optional[str] = ""
    promo_link: Optional[str] = ""
    promo_sort_order: int = 0
    promo_active_status: bool = True

class CourseSchema(BaseModel):
    id: str
    name: str
    level: str = "College/Undergraduate"
    category: str = "School of Computing and Information Technologies"
    description: str
    outcomes: List[str] = []
    info_url: Optional[str] = ""
    quota: int = 100
    sort_order: int = 0
    active: bool = True

# --- Form Builder Schemas ---
class FormFieldSchema(BaseModel):
    formfield_id: Optional[str] = None
    section_id: Optional[str] = None
    label: str
    field_key: str
    field_type: str = "text"
    field_options: List[str] = []
    field_required: bool = False
    field_help_text: Optional[str] = ""
    field_placeholder: Optional[str] = ""
    field_width: str = "half"
    field_sort_order: int = 0
    field_locked: bool = False

class FormSectionSchema(BaseModel):
    section_id: Optional[str] = None
    title: str
    description: Optional[str] = ""
    sort_order: int = 0
    fields: List[FormFieldSchema] = []

# --- Inquiries & CRM Schemas ---
class InquiryCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    mobile: str
    guardian_name: Optional[str] = ""
    guardian_contact: Optional[str] = ""
    program_interest: Optional[str] = ""
    visit_mode: str = "onsite"
    preferred_date: Optional[str] = None
    question: str

class InquiryNoteCreate(BaseModel):
    comment: str

class InquiryUpdateStatus(BaseModel):
    status: str

# --- Application Schemas ---
class ApplicationCreate(BaseModel):
    course_id: str
    first_name: str
    middle_name: Optional[str] = ""
    last_name: str
    email: EmailStr
    mobile: str
    entry_status: str = "Freshman"
    acad_year: str = "2026-2027"
    term: str = "Term 1"
    birth_date: Optional[str] = None
    sex: Optional[str] = "Male"
    nationality: Optional[str] = "Filipino"
    region: Optional[str] = ""
    city: Optional[str] = ""
    barangay: Optional[str] = ""
    home_address: Optional[str] = ""
    zip_code: Optional[str] = ""
    prev_school: Optional[str] = ""
    prev_school_sector: Optional[str] = "Private"
    prev_school_year: Optional[str] = ""
    answers: Dict[str, Any] = {}

class ApplicationUpdateStatus(BaseModel):
    status: str
    officer_notes: Optional[str] = ""

class PaymentSubmit(BaseModel):
    bank: str
    account_name: str
    account_last4: str
    reference_number: str
    amount: float
