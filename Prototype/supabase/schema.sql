-- =============================================================================
-- APC RamConnect Admissions System Schema (Supabase / PostgreSQL)
-- Designed for High Scalability, Simplicity, and Full ERD Compliance
-- =============================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. USERS & ROLES
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'applicant' CHECK (role IN ('applicant', 'admission_officer', 'marketing_admin', 'registrar', 'itro_admin')),
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. SITE SETTINGS & THEME CUSTOMIZATION (/staff/design)
CREATE TABLE IF NOT EXISTS site_settings (
    id SERIAL PRIMARY KEY,
    school_name VARCHAR(255) DEFAULT 'Asia Pacific College',
    motto VARCHAR(255) DEFAULT 'Industry. Integrity. Innovation.',
    headline VARCHAR(255) DEFAULT 'Your industry-based learning begins here!',
    welcome_title VARCHAR(255) DEFAULT 'Welcome to Asia Pacific College!',
    welcome_text TEXT DEFAULT 'Your first step to dedication to improve your career starts here. Your pursuit for learning, passion for knowledge, creativity, commitment, and value for advancing education will bring you closer to your goals.',
    schedule_title VARCHAR(255) DEFAULT 'Important Admission Schedule',
    gold_color VARCHAR(20) DEFAULT '#FDB813',
    navy_color VARCHAR(20) DEFAULT '#0B1E3D',
    background_style VARCHAR(50) DEFAULT 'mesh-gradient',
    hero_image VARCHAR(500) DEFAULT 'https://images.unsplash.com/photo-1541339907198-e08756dedf3f?auto=format&fit=crop&w=1200&q=80',
    footer_text TEXT DEFAULT '© 2026-2027 Asia Pacific College. All rights reserved. APC RamConnect.',
    privacy_notice TEXT DEFAULT 'APC collects and maintains personal data as part of its records management process in accordance with Republic Act 10173 (Data Privacy Act of 2012).',
    privacy_consent TEXT DEFAULT 'I have read and understood the collection, processing, and management of my personal data along with the policies and guidelines stated in the Asia Pacific College Data Privacy Policy.',
    reservation_fee NUMERIC(10, 2) DEFAULT 5000.00,
    student_email_domain VARCHAR(100) DEFAULT 'student.apc.edu.ph',
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. SCHEDULE MILESTONES (Homepage timeline)
CREATE TABLE IF NOT EXISTS milestones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    date_text VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    sort_order INT DEFAULT 0
);

-- 4. MARKETING PROMOTIONS & SCHOLARSHIPS (/staff/design promo modules)
CREATE TABLE IF NOT EXISTS promos (
    promo_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    promo_title VARCHAR(255) NOT NULL,
    promo_body TEXT NOT NULL,
    promo_image VARCHAR(500),
    promo_link VARCHAR(500),
    promo_sort_order INT DEFAULT 0,
    promo_active_status BOOLEAN DEFAULT TRUE
);

-- 5. ACADEMIC PROGRAMS & DEGREE TRACKS
CREATE TABLE IF NOT EXISTS courses (
    id VARCHAR(50) PRIMARY KEY, -- e.g. 'BSCS', 'BSIT', 'BMMA'
    name VARCHAR(255) NOT NULL,
    level VARCHAR(100) DEFAULT 'College/Undergraduate',
    category VARCHAR(100) DEFAULT 'School of Computing and Information Technologies',
    description TEXT,
    outcomes JSONB DEFAULT '[]'::jsonb, -- Career prospects list
    info_url VARCHAR(500),
    quota INT DEFAULT 100,
    sort_order INT DEFAULT 0,
    active BOOLEAN DEFAULT TRUE
);

-- 6. DYNAMIC FORM SECTIONS & FIELDS (/staff/form-builder)
CREATE TABLE IF NOT EXISTS form_sections (
    section_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    sort_order INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS form_fields (
    formfield_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    section_id UUID REFERENCES form_sections(section_id) ON DELETE CASCADE,
    label VARCHAR(255) NOT NULL,
    field_key VARCHAR(100) NOT NULL,
    field_type VARCHAR(50) NOT NULL DEFAULT 'text', -- text, email, tel, select, date, textarea, number, checkbox
    field_options JSONB DEFAULT '[]'::jsonb,
    field_required BOOLEAN DEFAULT FALSE,
    field_help_text TEXT,
    field_placeholder VARCHAR(255),
    field_width VARCHAR(20) DEFAULT 'half', -- half, full
    field_sort_order INT DEFAULT 0,
    field_locked BOOLEAN DEFAULT FALSE -- core fields cannot be deleted
);

-- 7. PROSPECTIVE INQUIRIES & INQUIRY CRM (/inquire & /staff)
CREATE TABLE IF NOT EXISTS inquiries (
    inquiry_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    mobile VARCHAR(50) NOT NULL,
    guardian_name VARCHAR(200),
    guardian_contact VARCHAR(50),
    program_interest VARCHAR(100),
    visit_mode VARCHAR(50) DEFAULT 'onsite', -- onsite, online
    preferred_date DATE,
    question TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'New' CHECK (status IN ('New', 'Contacted', 'Scheduled', 'Closed')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS inquiry_notes (
    note_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    inquiry_id UUID REFERENCES inquiries(inquiry_id) ON DELETE CASCADE,
    author_id UUID REFERENCES users(id) ON DELETE SET NULL,
    author_name VARCHAR(255) NOT NULL,
    comment TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 8. APPLICATIONS & STUDENT DOSSIERS (/apply, /portal, /staff/applicants)
CREATE TABLE IF NOT EXISTS applications (
    appform_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    course_id VARCHAR(50) REFERENCES courses(id) ON DELETE SET NULL,
    course_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    last_name VARCHAR(100) NOT NULL,
    mobile VARCHAR(50) NOT NULL,
    entry_status VARCHAR(50) DEFAULT 'Freshman', -- Freshman, Transferee, Second Degree
    acad_year VARCHAR(50) DEFAULT '2026-2027',
    term VARCHAR(50) DEFAULT 'Term 1',
    birth_date DATE,
    sex VARCHAR(20),
    nationality VARCHAR(100) DEFAULT 'Filipino',
    
    -- Address information
    region VARCHAR(100),
    city VARCHAR(100),
    barangay VARCHAR(100),
    home_address TEXT,
    zip_code VARCHAR(20),
    
    -- Previous School Details
    prev_school VARCHAR(255),
    prev_school_sector VARCHAR(50) DEFAULT 'Private', -- Private, Public
    prev_school_year VARCHAR(50),
    
    -- Dynamic Field Answers (from Form Builder)
    answers JSONB DEFAULT '{}'::jsonb,
    
    -- Qualification & Status Tracking
    status VARCHAR(50) DEFAULT 'Submitted' CHECK (status IN ('Submitted', 'Under Review', 'Incomplete Dossier', 'Qualified', 'Rejected', 'Enrolled')),
    officer_notes TEXT,
    
    -- Reservation Fee Payment
    payment_bank VARCHAR(100),
    payment_account_name VARCHAR(200),
    payment_account_last4 VARCHAR(10),
    payment_reference VARCHAR(100),
    payment_amount NUMERIC(10, 2),
    paid_at TIMESTAMPTZ,
    
    -- Student Records & Synchronization
    student_id VARCHAR(50), -- e.g. '2026-10492' generated upon payment
    student_email VARCHAR(255), -- e.g. 'jdelacruz@student.apc.edu.ph'
    transferred_at TIMESTAMPTZ, -- Synced with RAMPortal external system
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 9. AUDIT LOGS (Lightweight, consolidated audit trail)
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    user_name VARCHAR(255),
    action VARCHAR(100) NOT NULL,
    target_type VARCHAR(100) NOT NULL, -- 'site_settings', 'program', 'form', 'applicant'
    target_id VARCHAR(100),
    details JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for high-frequency filters
CREATE INDEX IF NOT EXISTS idx_inquiries_status ON inquiries(status);
CREATE INDEX IF NOT EXISTS idx_applications_status ON applications(status);
CREATE INDEX IF NOT EXISTS idx_applications_user ON applications(user_id);
CREATE INDEX IF NOT EXISTS idx_form_fields_section ON form_fields(section_id);

-- 10. ROW LEVEL SECURITY (RLS) POLICIES
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.site_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.milestones ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.promos ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.courses ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.form_sections ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.form_fields ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.inquiries ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.inquiry_notes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;

-- Public Read Policies for Catalog & CMS
CREATE POLICY "Public read for site_settings" ON public.site_settings FOR SELECT USING (true);
CREATE POLICY "Public read for milestones" ON public.milestones FOR SELECT USING (true);
CREATE POLICY "Public read for promos" ON public.promos FOR SELECT USING (true);
CREATE POLICY "Public read for courses" ON public.courses FOR SELECT USING (true);
CREATE POLICY "Public read for form_sections" ON public.form_sections FOR SELECT USING (true);
CREATE POLICY "Public read for form_fields" ON public.form_fields FOR SELECT USING (true);

-- Inquiries: Public submission, authenticated staff access
CREATE POLICY "Public can submit inquiries" ON public.inquiries FOR INSERT WITH CHECK (true);
CREATE POLICY "Staff can view inquiries" ON public.inquiries FOR SELECT TO authenticated USING (true);
CREATE POLICY "Staff can update inquiries" ON public.inquiries FOR UPDATE TO authenticated USING (true);

-- Inquiry Notes: Staff only
CREATE POLICY "Staff can view inquiry notes" ON public.inquiry_notes FOR SELECT TO authenticated USING (true);
CREATE POLICY "Staff can create inquiry notes" ON public.inquiry_notes FOR INSERT TO authenticated WITH CHECK (true);

-- Applications: Insert allowed, users see own, staff sees all
CREATE POLICY "Applicants can insert applications" ON public.applications FOR INSERT WITH CHECK (true);
CREATE POLICY "Users can view their own application" ON public.applications FOR SELECT TO authenticated USING (auth.uid() = user_id);

-- Users: Read own profile only
CREATE POLICY "Users can view own profile" ON public.users FOR SELECT TO authenticated USING (auth.uid() = id);

-- Audit logs: Authenticated staff only
CREATE POLICY "Staff can read audit logs" ON public.audit_logs FOR SELECT TO authenticated USING (true);
CREATE POLICY "Staff can insert audit logs" ON public.audit_logs FOR INSERT TO authenticated WITH CHECK (true);

