-- =============================================================================
-- APC RamConnect Seed Data
-- =============================================================================

-- Default Site Settings
INSERT INTO site_settings (id, school_name, motto, headline, welcome_title, welcome_text, schedule_title, gold_color, navy_color, reservation_fee, student_email_domain)
VALUES (
    1,
    'Asia Pacific College',
    'Industry. Integrity. Innovation.',
    'Your industry-based learning begins here!',
    'Welcome to Asia Pacific College!',
    'Your first step to dedication to improve your career starts here. Your pursuit for learning, passion for knowledge, creativity, commitment, and value for advancing education will bring you closer to your goals.',
    'Important Admission Schedule',
    '#FDB813',
    '#0B1E3D',
    5000.00,
    'student.apc.edu.ph'
) ON CONFLICT (id) DO NOTHING;

-- Schedule Milestones
INSERT INTO milestones (date_text, title, description, sort_order) VALUES
('17 April 2026', 'Start of Online Application / Registration Period', 'Opening of the online intake portal for Academic Year 2026-2027.', 1),
('15 May 2026', 'Last Day of Submission of Application', 'Final deadline for prospective students to submit application dossiers.', 2),
('28 June 2026', 'Schedule of Qualifying Examination', 'On-campus & virtual diagnostic testing for qualified applicants.', 3);

-- Promos / Opportunities Highlight
INSERT INTO promos (promo_title, promo_body, promo_image, promo_link, promo_sort_order, promo_active_status) VALUES
('President''s Scholarship', 'Full tuition & matriculation support specifically for incoming High Honors and Valedictorian high school graduates.', 'https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=600&q=80', 'https://apc.edu.ph/scholarships', 1, true),
('Tech Innovator Grant', '50% tuition reduction structure focusing heavily on digital portfolios, robotics, and coding proficiency.', 'https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=600&q=80', 'https://apc.edu.ph/grants', 2, true),
('Financial Aid Equity', 'Need-based adjustments maintaining academic access and continuity for deserving students and dependents.', 'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=600&q=80', 'https://apc.edu.ph/financial-aid', 3, true);

-- Academic Courses / Programs with Career Outcomes
INSERT INTO courses (id, name, level, category, description, outcomes, quota, sort_order, active) VALUES
('BSCS', 'Bachelor of Science in Computer Science', 'College/Undergraduate', 'School of Computing and Information Technologies', 'Covers algorithms, artificial intelligence, software engineering, and computational complexity with heavy industry projects.', '["Software Engineer", "AI/ML Specialist", "Algorithm Designer", "Data Scientist", "Systems Architect"]'::jsonb, 120, 1, true),
('BSIT', 'Bachelor of Science in Information Technology', 'College/Undergraduate', 'School of Computing and Information Technologies', 'Focuses on enterprise network infrastructure, cloud engineering, full-stack web and mobile systems development.', '["Full-Stack Developer", "DevOps Engineer", "Cloud Infrastructure Architect", "IT Systems Analyst", "Database Administrator"]'::jsonb, 150, 2, true),
('BMMA', 'Bachelor of Multimedia Arts', 'College/Undergraduate', 'School of Multimedia and Arts', 'Combines creative storytelling, 3D modeling, UI/UX interaction design, digital animation, and video production.', '["UI/UX Designer", "Motion Graphic Artist", "Creative Director", "3D Asset Animator", "Digital Art Director"]'::jsonb, 100, 3, true),
('BSBA-BA', 'BS in Business Administration - Business Analytics', 'College/Undergraduate', 'School of Management', 'Bridges business strategy, predictive modeling, financial analytics, and corporate decision science.', '["Business Intelligence Analyst", "Analytics Consultant", "Product Operations Manager", "Market Risk Strategist"]'::jsonb, 80, 4, true),
('ABPsych', 'Bachelor of Arts in Psychology', 'College/Undergraduate', 'School of Humanities and Social Sciences', 'Equips learners with empirical behavioral research, industrial-organizational psychology, and clinical foundations.', '["HR Talent Strategist", "Behavioral Researcher", "Organizational Development Consultant", "Guidance Specialist"]'::jsonb, 60, 5, true),
('ACT-CST', 'Associate in Computer Technology - Cybersecurity Track', 'College/Undergraduate', 'School of Computing and Information Technologies', 'A 2-year intensive ladderized program focusing on defensive blue-team operations, vulnerability assessment, and threat triage.', '["Cyber Security Analyst", "SOC Tier-1 Responder", "Network Security Technician", "Penetration Tester"]'::jsonb, 75, 6, true);

-- Form Sections
INSERT INTO form_sections (section_id, title, description, sort_order) VALUES
('11111111-1111-1111-1111-111111111111', 'Preferred Program', 'Select your target degree program, entry level, and academic year.', 1),
('22222222-2222-2222-2222-222222222222', 'Basic Information (Per Birth Certificate)', 'Ensure names match your government-issued birth certificate or passport.', 2),
('33333333-3333-3333-3333-333333333333', 'Contact Details', 'We will use these details to dispatch your qualification standing.', 3),
('44444444-4444-4444-4444-444444444444', 'Previous School Information', 'Provide accurate details of your most recent secondary or tertiary institution.', 4);

-- Form Fields
INSERT INTO form_fields (section_id, label, field_key, field_type, field_options, field_required, field_help_text, field_placeholder, field_width, field_sort_order, field_locked) VALUES
('11111111-1111-1111-1111-111111111111', 'Academic Year & Term', 'acad_term', 'select', '["AY 2026-2027, Term 1", "AY 2026-2027, Term 2", "AY 2026-2027, Term 3"]'::jsonb, true, 'Current upcoming admissions intake', 'Select Academic Term', 'half', 1, true),
('11111111-1111-1111-1111-111111111111', 'Applying For', 'app_level', 'select', '["College/Undergraduate", "Senior High School", "Graduate Studies"]'::jsonb, true, 'School division', 'Select Level', 'half', 2, true),
('11111111-1111-1111-1111-111111111111', 'Entry Status', 'entry_status', 'select', '["Freshman", "Transferee", "Second Degree"]'::jsonb, true, 'Applicant type', 'Select Status', 'half', 3, true),

('22222222-2222-2222-2222-222222222222', 'First Name', 'first_name', 'text', '[]'::jsonb, true, 'Given name on birth certificate', 'e.g. Juan', 'half', 1, true),
('22222222-2222-2222-2222-222222222222', 'Middle Name', 'middle_name', 'text', '[]'::jsonb, false, 'Leave blank if not applicable', 'e.g. Santos', 'half', 2, false),
('22222222-2222-2222-2222-222222222222', 'Last Name', 'last_name', 'text', '[]'::jsonb, true, 'Surname / Family name', 'e.g. Dela Cruz', 'half', 3, true),
('22222222-2222-2222-2222-222222222222', 'Date of Birth', 'birth_date', 'date', '[]'::jsonb, true, 'Must be at least 15 years of age', '', 'half', 4, true),
('22222222-2222-2222-2222-222222222222', 'Sex', 'sex', 'select', '["Male", "Female", "Prefer not to say"]'::jsonb, true, 'Biological sex on PSA copy', 'Select', 'half', 5, false),
('22222222-2222-2222-2222-222222222222', 'Nationality', 'nationality', 'text', '[]'::jsonb, true, 'Citizenship', 'e.g. Filipino', 'half', 6, false),

('33333333-3333-3333-3333-333333333333', 'Applicant Email Address', 'email', 'email', '[]'::jsonb, true, 'Active email where credentials and notifications are sent', 'juandelacruz@gmail.com', 'half', 1, true),
('33333333-3333-3333-3333-333333333333', 'Mobile Phone Number', 'mobile', 'tel', '[]'::jsonb, true, '11-digit PH mobile number starting with 09', '09171234567', 'half', 2, true),
('33333333-3333-3333-3333-333333333333', 'Current Residential Address', 'home_address', 'text', '[]'::jsonb, true, 'House No., Street, Subdivision', 'Unit 12B Tower 2, Chino Roces Ave.', 'full', 3, false),
('33333333-3333-3333-3333-333333333333', 'City / Municipality', 'city', 'text', '[]'::jsonb, true, 'City of residence', 'Makati City', 'half', 4, false),

('44444444-4444-4444-4444-444444444444', 'Previous School Name', 'prev_school', 'text', '[]'::jsonb, true, 'High school or university graduated from', 'e.g. Pasay City National Science High School', 'half', 1, false),
('44444444-4444-4444-4444-444444444444', 'School Sector', 'prev_school_sector', 'select', '["Private", "Public"]'::jsonb, true, 'Institutional sector', 'Select', 'half', 2, false),
('44444444-4444-4444-4444-444444444444', 'Last Year Attended', 'prev_school_year', 'text', '[]'::jsonb, true, 'Completion year', '2025', 'half', 3, false);

-- Default Demo Users (Password: admin123 and user123)
-- Using SHA-256 / bcrypt hash representation for mock & real auth
INSERT INTO users (id, email, full_name, role, password_hash) VALUES
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'admissions@apc.edu.ph', 'Maria Santos (Admissions Lead)', 'admission_officer', '$2b$12$e8Yk2iXGj25s0Z6kLq1LyeK7v9sH8kF7r1t9.G8m5L6kLq1LyeK7v'),
('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'applicant@gmail.com', 'Juan Dela Cruz', 'applicant', '$2b$12$e8Yk2iXGj25s0Z6kLq1LyeK7v9sH8kF7r1t9.G8m5L6kLq1LyeK7v')
ON CONFLICT (email) DO NOTHING;

-- Sample Inquiries for CRM Demo
INSERT INTO inquiries (inquiry_id, first_name, last_name, email, mobile, guardian_name, guardian_contact, program_interest, visit_mode, preferred_date, question, status) VALUES
('c1111111-1111-1111-1111-111111111111', 'Gabriel', 'Reyes', 'gabriel.reyes@gmail.com', '09189876543', 'Eduardo Reyes', '09176543210', 'BSCS', 'onsite', '2026-05-10', 'Does the Computer Science curriculum have a specialization in Game Development or Cloud Computing?', 'New'),
('c2222222-2222-2222-2222-222222222222', 'Samantha', 'Tan', 'sam.tan@yahoo.com', '09228887766', 'Lilian Tan', '09228887755', 'BMMA', 'online', '2026-05-12', 'Can I inquire if there are portfolio review requirements for the Multimedia Arts scholarship?', 'Contacted'),
('c3333333-3333-3333-3333-333333333333', 'Marco', 'Valdez', 'm.valdez@outlook.com', '09153334444', 'Elena Valdez', '09153334400', 'BSIT', 'onsite', '2026-05-15', 'I am a transferee from a different college. How do I get my credited IT subjects evaluated?', 'Scheduled');

-- Sample Inquiry Notes
INSERT INTO inquiry_notes (inquiry_id, author_id, author_name, comment) VALUES
('c2222222-2222-2222-2222-222222222222', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'Maria Santos', 'Called student and emailed BMMA portfolio rubric for Tech Innovator Grant.');

-- Sample Application for the demo applicant
INSERT INTO applications (
    appform_id, user_id, course_id, course_name, email, first_name, middle_name, last_name, mobile,
    entry_status, acad_year, term, birth_date, sex, nationality, region, city, barangay, home_address, zip_code,
    prev_school, prev_school_sector, prev_school_year, status, officer_notes, payment_amount
) VALUES (
    'd1111111-1111-1111-1111-111111111111',
    'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
    'BSCS',
    'Bachelor of Science in Computer Science',
    'applicant@gmail.com',
    'Juan',
    'Santos',
    'Dela Cruz',
    '09171234567',
    'Freshman',
    '2026-2027',
    'Term 1',
    '2007-06-15',
    'Male',
    'Filipino',
    'NCR',
    'Makati City',
    'Magallanes',
    'APC Compound, 3 Humabon St, Magallanes',
    '1232',
    'Makati Science High School',
    'Public',
    '2025',
    'Qualified',
    'Credentials, Form 137, and PSA birth certificate verified. Candidate is qualified to pay reservation fee.',
    5000.00
);
