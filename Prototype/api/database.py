import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from .config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_ROLE_KEY

# Initialize Supabase clients if configured
supabase = None
supabase_admin = None
if SUPABASE_URL and SUPABASE_KEY and "your-project-ref" not in SUPABASE_URL:
    try:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        if SUPABASE_SERVICE_ROLE_KEY:
            supabase_admin = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    except Exception as e:
        print(f"Supabase connection init notice: {e}")


def get_supabase_db():
    """Return service-role Supabase client when available, else anon client."""
    return supabase_admin or supabase


def create_anon_client():
    """Create an isolated Supabase anon client so auth sign-in/up does not mutate shared headers."""
    if SUPABASE_URL and SUPABASE_KEY and "your-project-ref" not in SUPABASE_URL:
        try:
            from supabase import create_client
            return create_client(SUPABASE_URL, SUPABASE_KEY)
        except Exception:
            return None
    return None

# In-memory storage layer initialized with default APC seed data
# Allows instant local development and offline preview
INITIAL_SETTINGS = {
    "id": 1,
    "school_name": "Asia Pacific College",
    "motto": "Industry. Integrity. Innovation.",
    "headline": "Your industry-based learning begins here!",
    "welcome_title": "Welcome to Asia Pacific College!",
    "welcome_text": "Your first step to dedication to improve your career starts here. Your pursuit for learning, passion for knowledge, creativity, commitment, and value for advancing education will bring you closer to your goals.",
    "schedule_title": "Important Admission Schedule",
    "gold_color": "#FDB813",
    "navy_color": "#0B1E3D",
    "background_style": "mesh-gradient",
    "hero_image": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?auto=format&fit=crop&w=1200&q=80",
    "footer_text": "© 2026-2027 Asia Pacific College. All rights reserved. APC RamConnect.",
    "privacy_notice": "APC collects and maintains personal data as part of its records management process in accordance with Republic Act 10173 (Data Privacy Act of 2012).",
    "privacy_consent": "I have read and understood the collection, processing, and management of my personal data along with the policies and guidelines stated in the Asia Pacific College Data Privacy Policy.",
    "reservation_fee": 5000.00,
    "student_email_domain": "student.apc.edu.ph"
}

INITIAL_COURSES = [
    {
        "id": "BSCS",
        "name": "Bachelor of Science in Computer Science",
        "level": "College/Undergraduate",
        "category": "School of Computing and Information Technologies",
        "description": "Covers algorithms, artificial intelligence, software engineering, and computational complexity with heavy industry projects.",
        "outcomes": ["Software Engineer", "AI/ML Specialist", "Algorithm Designer", "Data Scientist", "Systems Architect"],
        "info_url": "https://apc.edu.ph/programs/bscs",
        "quota": 120,
        "sort_order": 1,
        "active": True
    },
    {
        "id": "BSIT",
        "name": "Bachelor of Science in Information Technology",
        "level": "College/Undergraduate",
        "category": "School of Computing and Information Technologies",
        "description": "Focuses on enterprise network infrastructure, cloud engineering, full-stack web and mobile systems development.",
        "outcomes": ["Full-Stack Developer", "DevOps Engineer", "Cloud Infrastructure Architect", "IT Systems Analyst", "Database Administrator"],
        "info_url": "https://apc.edu.ph/programs/bsit",
        "quota": 150,
        "sort_order": 2,
        "active": True
    },
    {
        "id": "BMMA",
        "name": "Bachelor of Multimedia Arts",
        "level": "College/Undergraduate",
        "category": "School of Multimedia and Arts",
        "description": "Combines creative storytelling, 3D modeling, UI/UX interaction design, digital animation, and video production.",
        "outcomes": ["UI/UX Designer", "Motion Graphic Artist", "Creative Director", "3D Asset Animator", "Digital Art Director"],
        "info_url": "https://apc.edu.ph/programs/bmma",
        "quota": 100,
        "sort_order": 3,
        "active": True
    },
    {
        "id": "BSBA-BA",
        "name": "BS in Business Administration - Business Analytics",
        "level": "College/Undergraduate",
        "category": "School of Management",
        "description": "Bridges business strategy, predictive modeling, financial analytics, and corporate decision science.",
        "outcomes": ["Business Intelligence Analyst", "Analytics Consultant", "Product Operations Manager", "Market Risk Strategist"],
        "info_url": "https://apc.edu.ph/programs/bsba",
        "quota": 80,
        "sort_order": 4,
        "active": True
    },
    {
        "id": "ABPsych",
        "name": "Bachelor of Arts in Psychology",
        "level": "College/Undergraduate",
        "category": "School of Humanities and Social Sciences",
        "description": "Equips learners with empirical behavioral research, industrial-organizational psychology, and clinical foundations.",
        "outcomes": ["HR Talent Strategist", "Behavioral Researcher", "Organizational Development Consultant", "Guidance Specialist"],
        "info_url": "https://apc.edu.ph/programs/abpsych",
        "quota": 60,
        "sort_order": 5,
        "active": True
    },
    {
        "id": "ACT-CST",
        "name": "Associate in Computer Technology - Cybersecurity Track",
        "level": "College/Undergraduate",
        "category": "School of Computing and Information Technologies",
        "description": "A 2-year intensive ladderized program focusing on defensive blue-team operations, vulnerability assessment, and threat triage.",
        "outcomes": ["Cyber Security Analyst", "SOC Tier-1 Responder", "Network Security Technician", "Penetration Tester"],
        "info_url": "https://apc.edu.ph/programs/act",
        "quota": 75,
        "sort_order": 6,
        "active": True
    }
]

INITIAL_MILESTONES = [
    {
        "id": "m1",
        "date_text": "17 April 2026",
        "title": "Start of Online Application / Registration Period",
        "description": "Opening of the online intake portal for Academic Year 2026-2027.",
        "sort_order": 1
    },
    {
        "id": "m2",
        "date_text": "15 May 2026",
        "title": "Last Day of Submission of Application",
        "description": "Final deadline for prospective students to submit application dossiers.",
        "sort_order": 2
    },
    {
        "id": "m3",
        "date_text": "28 June 2026",
        "title": "Schedule of Qualifying Examination",
        "description": "On-campus & virtual diagnostic testing for qualified applicants.",
        "sort_order": 3
    }
]

INITIAL_PROMOS = [
    {
        "promo_id": "p1",
        "promo_title": "President's Scholarship",
        "promo_body": "Full tuition & matriculation support specifically for incoming High Honors and Valedictorian high school graduates.",
        "promo_image": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=600&q=80",
        "promo_link": "https://apc.edu.ph/scholarships",
        "promo_sort_order": 1,
        "promo_active_status": True
    },
    {
        "promo_id": "p2",
        "promo_title": "Tech Innovator Grant",
        "promo_body": "50% tuition reduction structure focusing heavily on digital portfolios, robotics, and coding proficiency.",
        "promo_image": "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=600&q=80",
        "promo_link": "https://apc.edu.ph/grants",
        "promo_sort_order": 2,
        "promo_active_status": True
    },
    {
        "promo_id": "p3",
        "promo_title": "Financial Aid Equity",
        "promo_body": "Need-based adjustments maintaining academic access and continuity for deserving students and dependents.",
        "promo_image": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=600&q=80",
        "promo_link": "https://apc.edu.ph/financial-aid",
        "promo_sort_order": 3,
        "promo_active_status": True
    }
]

INITIAL_SECTIONS = [
    {
        "section_id": "sec-1",
        "title": "Preferred Program",
        "description": "Select your target degree program, entry level, and academic year.",
        "sort_order": 1,
        "fields": [
            {
                "formfield_id": "f1-1",
                "label": "Academic Year & Term",
                "field_key": "acad_term",
                "field_type": "select",
                "field_options": ["AY 2026-2027, Term 1", "AY 2026-2027, Term 2", "AY 2026-2027, Term 3"],
                "field_required": True,
                "field_help_text": "Upcoming intake",
                "field_placeholder": "Select Academic Term",
                "field_width": "half",
                "field_sort_order": 1,
                "field_locked": True
            },
            {
                "formfield_id": "f1-2",
                "label": "Applying For",
                "field_key": "app_level",
                "field_type": "select",
                "field_options": ["College/Undergraduate", "Senior High School", "Graduate Studies"],
                "field_required": True,
                "field_help_text": "School level",
                "field_placeholder": "Select Level",
                "field_width": "half",
                "field_sort_order": 2,
                "field_locked": True
            },
            {
                "formfield_id": "f1-3",
                "label": "Entry Status",
                "field_key": "entry_status",
                "field_type": "select",
                "field_options": ["Freshman", "Transferee", "Second Degree"],
                "field_required": True,
                "field_help_text": "Applicant category",
                "field_placeholder": "Select Status",
                "field_width": "half",
                "field_sort_order": 3,
                "field_locked": True
            }
        ]
    },
    {
        "section_id": "sec-2",
        "title": "Basic Information (Per Birth Certificate)",
        "description": "Ensure names match your government-issued birth certificate.",
        "sort_order": 2,
        "fields": [
            {
                "formfield_id": "f2-1",
                "label": "First Name",
                "field_key": "first_name",
                "field_type": "text",
                "field_options": [],
                "field_required": True,
                "field_help_text": "",
                "field_placeholder": "e.g. Juan",
                "field_width": "half",
                "field_sort_order": 1,
                "field_locked": True
            },
            {
                "formfield_id": "f2-2",
                "label": "Middle Name",
                "field_key": "middle_name",
                "field_type": "text",
                "field_options": [],
                "field_required": False,
                "field_help_text": "Leave blank if none",
                "field_placeholder": "e.g. Santos",
                "field_width": "half",
                "field_sort_order": 2,
                "field_locked": False
            },
            {
                "formfield_id": "f2-3",
                "label": "Last Name",
                "field_key": "last_name",
                "field_type": "text",
                "field_options": [],
                "field_required": True,
                "field_help_text": "",
                "field_placeholder": "e.g. Dela Cruz",
                "field_width": "half",
                "field_sort_order": 3,
                "field_locked": True
            },
            {
                "formfield_id": "f2-4",
                "label": "Date of Birth",
                "field_key": "birth_date",
                "field_type": "date",
                "field_options": [],
                "field_required": True,
                "field_help_text": "Must match birth certificate",
                "field_placeholder": "",
                "field_width": "half",
                "field_sort_order": 4,
                "field_locked": True
            },
            {
                "formfield_id": "f2-5",
                "label": "Sex",
                "field_key": "sex",
                "field_type": "select",
                "field_options": ["Male", "Female", "Prefer not to say"],
                "field_required": True,
                "field_help_text": "Biological sex",
                "field_placeholder": "Select",
                "field_width": "half",
                "field_sort_order": 5,
                "field_locked": False
            },
            {
                "formfield_id": "f2-6",
                "label": "Nationality",
                "field_key": "nationality",
                "field_type": "text",
                "field_options": [],
                "field_required": True,
                "field_help_text": "",
                "field_placeholder": "Filipino",
                "field_width": "half",
                "field_sort_order": 6,
                "field_locked": False
            }
        ]
    },
    {
        "section_id": "sec-3",
        "title": "Contact Details",
        "description": "Used to send status updates and verification codes.",
        "sort_order": 3,
        "fields": [
            {
                "formfield_id": "f3-1",
                "label": "Applicant Email",
                "field_key": "email",
                "field_type": "email",
                "field_options": [],
                "field_required": True,
                "field_help_text": "We will email your login link",
                "field_placeholder": "applicant@gmail.com",
                "field_width": "half",
                "field_sort_order": 1,
                "field_locked": True
            },
            {
                "formfield_id": "f3-2",
                "label": "Mobile Number",
                "field_key": "mobile",
                "field_type": "tel",
                "field_options": [],
                "field_required": True,
                "field_help_text": "11-digit PH mobile",
                "field_placeholder": "09171234567",
                "field_width": "half",
                "field_sort_order": 2,
                "field_locked": True
            },
            {
                "formfield_id": "f3-3",
                "label": "Home Address",
                "field_key": "home_address",
                "field_type": "text",
                "field_options": [],
                "field_required": True,
                "field_help_text": "House No., Street, Barangay",
                "field_placeholder": "Unit 4B, Chino Roces Ave.",
                "field_width": "full",
                "field_sort_order": 3,
                "field_locked": False
            },
            {
                "formfield_id": "f3-4",
                "label": "City / Municipality",
                "field_key": "city",
                "field_type": "text",
                "field_options": [],
                "field_required": True,
                "field_help_text": "",
                "field_placeholder": "Makati City",
                "field_width": "half",
                "field_sort_order": 4,
                "field_locked": False
            }
        ]
    },
    {
        "section_id": "sec-4",
        "title": "Previous School Information",
        "description": "Information on secondary school background.",
        "sort_order": 4,
        "fields": [
            {
                "formfield_id": "f4-1",
                "label": "Previous School Name",
                "field_key": "prev_school",
                "field_type": "text",
                "field_options": [],
                "field_required": True,
                "field_help_text": "",
                "field_placeholder": "Pasay City National Science HS",
                "field_width": "half",
                "field_sort_order": 1,
                "field_locked": False
            },
            {
                "formfield_id": "f4-2",
                "label": "School Sector",
                "field_key": "prev_school_sector",
                "field_type": "select",
                "field_options": ["Private", "Public"],
                "field_required": True,
                "field_help_text": "",
                "field_placeholder": "Select",
                "field_width": "half",
                "field_sort_order": 2,
                "field_locked": False
            },
            {
                "formfield_id": "f4-3",
                "label": "Last Year Attended",
                "field_key": "prev_school_year",
                "field_type": "text",
                "field_options": [],
                "field_required": True,
                "field_help_text": "e.g. 2025",
                "field_placeholder": "2025",
                "field_width": "half",
                "field_sort_order": 3,
                "field_locked": False
            }
        ]
    }
]

# In-Memory state dict
DB = {
    "settings": INITIAL_SETTINGS.copy(),
    "courses": list(INITIAL_COURSES),
    "milestones": list(INITIAL_MILESTONES),
    "promos": list(INITIAL_PROMOS),
    "sections": list(INITIAL_SECTIONS),
    "users": [
        {
            "id": "u-admin-1",
            "email": "admissions@apc.edu.ph",
            "full_name": "Maria Santos (Admissions Lead)",
            "role": "admission_officer",
            "password": "admin123"
        },
        {
            "id": "u-app-1",
            "email": "applicant@gmail.com",
            "full_name": "Juan Dela Cruz",
            "role": "applicant",
            "password": "user123"
        }
    ],
    "inquiries": [
        {
            "inquiry_id": "inq-101",
            "first_name": "Gabriel",
            "last_name": "Reyes",
            "email": "gabriel.reyes@gmail.com",
            "mobile": "09189876543",
            "guardian_name": "Eduardo Reyes",
            "guardian_contact": "09176543210",
            "program_interest": "BSCS",
            "visit_mode": "onsite",
            "preferred_date": "2026-05-10",
            "question": "Does the Computer Science curriculum have specializations in Cybersecurity or Artificial Intelligence?",
            "status": "New",
            "created_at": datetime.now().isoformat(),
            "notes": []
        },
        {
            "inquiry_id": "inq-102",
            "first_name": "Samantha",
            "last_name": "Tan",
            "email": "sam.tan@yahoo.com",
            "mobile": "09228887766",
            "guardian_name": "Lilian Tan",
            "guardian_contact": "09228887755",
            "program_interest": "BMMA",
            "visit_mode": "online",
            "preferred_date": "2026-05-12",
            "question": "Can I inquire if there are portfolio review requirements for the Multimedia Arts scholarship?",
            "status": "Contacted",
            "created_at": datetime.now().isoformat(),
            "notes": [
                {
                    "note_id": "note-1",
                    "author_name": "Maria Santos",
                    "comment": "Called applicant and emailed BMMA portfolio guidelines.",
                    "created_at": datetime.now().isoformat()
                }
            ]
        }
    ],
    "applications": [
        {
            "appform_id": "app-2026-001",
            "user_id": "u-app-1",
            "course_id": "BSCS",
            "course_name": "Bachelor of Science in Computer Science",
            "email": "applicant@gmail.com",
            "first_name": "Juan",
            "middle_name": "Santos",
            "last_name": "Dela Cruz",
            "mobile": "09171234567",
            "entry_status": "Freshman",
            "acad_year": "2026-2027",
            "term": "Term 1",
            "birth_date": "2007-06-15",
            "sex": "Male",
            "nationality": "Filipino",
            "home_address": "APC Compound, 3 Humabon St, Magallanes",
            "city": "Makati City",
            "prev_school": "Makati Science High School",
            "prev_school_sector": "Public",
            "prev_school_year": "2025",
            "answers": {},
            "status": "Qualified",
            "officer_notes": "All initial credentials verified. Qualified to pay reservation fee.",
            "payment_bank": None,
            "payment_account_name": None,
            "payment_account_last4": None,
            "payment_reference": None,
            "payment_amount": 5000.00,
            "paid_at": None,
            "student_id": None,
            "student_email": None,
            "created_at": datetime.now().isoformat()
        }
    ]
}
