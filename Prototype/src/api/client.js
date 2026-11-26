// Unified API Client for APC RamConnect
// Connects to FastAPI /api endpoints with seamless fallback state

const STORAGE_KEYS = {
  SETTINGS: 'apc_ramconnect_settings',
  COURSES: 'apc_ramconnect_courses',
  MILESTONES: 'apc_ramconnect_milestones',
  PROMOS: 'apc_ramconnect_promos',
  SECTIONS: 'apc_ramconnect_sections',
  INQUIRIES: 'apc_ramconnect_inquiries',
  APPLICATIONS: 'apc_ramconnect_applications',
  CURRENT_USER: 'apc_ramconnect_user'
};

// Initial Seed Data (mirrors backend seed.sql)
const DEFAULT_SETTINGS = {
  school_name: "Asia Pacific College",
  motto: "Industry. Integrity. Innovation.",
  headline: "Your industry-based learning begins here!",
  welcome_title: "Welcome to Asia Pacific College!",
  welcome_text: "Your first step to dedication to improve your career starts here. Your pursuit for learning, passion for knowledge, creativity, commitment, and value for advancing education will bring you closer to your goals.",
  schedule_title: "Important Admission Schedule",
  gold_color: "#FDB813",
  navy_color: "#0B1E3D",
  background_style: "mesh-gradient",
  hero_image: "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?auto=format&fit=crop&w=1200&q=80",
  footer_text: "© 2026-2027 Asia Pacific College. All rights reserved. APC RamConnect.",
  privacy_notice: "APC collects and maintains personal data as part of its records management process in accordance with Republic Act 10173 (Data Privacy Act of 2012).",
  privacy_consent: "I have read and understood the collection, processing, and management of my personal data along with the policies and guidelines stated in the Asia Pacific College Data Privacy Policy.",
  reservation_fee: 5000.00,
  student_email_domain: "student.apc.edu.ph"
};

const DEFAULT_COURSES = [
  {
    id: "BSCS",
    name: "Bachelor of Science in Computer Science",
    level: "College/Undergraduate",
    category: "School of Computing and Information Technologies",
    description: "Covers algorithms, artificial intelligence, software engineering, and computational complexity with heavy industry projects.",
    outcomes: ["Software Engineer", "AI/ML Specialist", "Algorithm Designer", "Data Scientist", "Systems Architect"],
    info_url: "https://apc.edu.ph/programs/bscs",
    quota: 120,
    sort_order: 1,
    active: true
  },
  {
    id: "BSIT",
    name: "Bachelor of Science in Information Technology",
    level: "College/Undergraduate",
    category: "School of Computing and Information Technologies",
    description: "Focuses on enterprise network infrastructure, cloud engineering, full-stack web and mobile systems development.",
    outcomes: ["Full-Stack Developer", "DevOps Engineer", "Cloud Infrastructure Architect", "IT Systems Analyst", "Database Administrator"],
    info_url: "https://apc.edu.ph/programs/bsit",
    quota: 150,
    sort_order: 2,
    active: true
  },
  {
    id: "BMMA",
    name: "Bachelor of Multimedia Arts",
    level: "College/Undergraduate",
    category: "School of Multimedia and Arts",
    description: "Combines creative storytelling, 3D modeling, UI/UX interaction design, digital animation, and video production.",
    outcomes: ["UI/UX Designer", "Motion Graphic Artist", "Creative Director", "3D Asset Animator", "Digital Art Director"],
    info_url: "https://apc.edu.ph/programs/bmma",
    quota: 100,
    sort_order: 3,
    active: true
  },
  {
    id: "BSBA-BA",
    name: "BS in Business Administration - Business Analytics",
    level: "College/Undergraduate",
    category: "School of Management",
    description: "Bridges business strategy, predictive modeling, financial analytics, and corporate decision science.",
    outcomes: ["Business Intelligence Analyst", "Analytics Consultant", "Product Operations Manager", "Market Risk Strategist"],
    info_url: "https://apc.edu.ph/programs/bsba",
    quota: 80,
    sort_order: 4,
    active: true
  },
  {
    id: "ABPsych",
    name: "Bachelor of Arts in Psychology",
    level: "College/Undergraduate",
    category: "School of Humanities and Social Sciences",
    description: "Equips learners with empirical behavioral research, industrial-organizational psychology, and clinical foundations.",
    outcomes: ["HR Talent Strategist", "Behavioral Researcher", "Organizational Development Consultant", "Guidance Specialist"],
    info_url: "https://apc.edu.ph/programs/abpsych",
    quota: 60,
    sort_order: 5,
    active: true
  },
  {
    id: "ACT-CST",
    name: "Associate in Computer Technology - Cybersecurity Track",
    level: "College/Undergraduate",
    category: "School of Computing and Information Technologies",
    description: "A 2-year intensive ladderized program focusing on defensive blue-team operations, vulnerability assessment, and threat triage.",
    outcomes: ["Cyber Security Analyst", "SOC Tier-1 Responder", "Network Security Technician", "Penetration Tester"],
    info_url: "https://apc.edu.ph/programs/act",
    quota: 75,
    sort_order: 6,
    active: true
  }
];

const DEFAULT_MILESTONES = [
  { id: "m1", date_text: "17 April 2026", title: "Start of Online Application / Registration Period", description: "Opening of the online intake portal for Academic Year 2026-2027.", sort_order: 1 },
  { id: "m2", date_text: "15 May 2026", title: "Last Day of Submission of Application", description: "Final deadline for prospective students to submit application dossiers.", sort_order: 2 },
  { id: "m3", date_text: "28 June 2026", title: "Schedule of Qualifying Examination", description: "On-campus & virtual diagnostic testing for qualified applicants.", sort_order: 3 }
];

const DEFAULT_PROMOS = [
  {
    promo_id: "p1",
    promo_title: "President's Scholarship",
    promo_body: "Full tuition & matriculation support specifically for incoming High Honors and Valedictorian high school graduates.",
    promo_image: "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=600&q=80",
    promo_link: "https://apc.edu.ph/scholarships",
    promo_sort_order: 1,
    promo_active_status: true
  },
  {
    promo_id: "p2",
    promo_title: "Tech Innovator Grant",
    promo_body: "50% tuition reduction structure focusing heavily on digital portfolios, robotics, and coding proficiency.",
    promo_image: "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=600&q=80",
    promo_link: "https://apc.edu.ph/grants",
    promo_sort_order: 2,
    promo_active_status: true
  },
  {
    promo_id: "p3",
    promo_title: "Financial Aid Equity",
    promo_body: "Need-based adjustments maintaining academic access and continuity for deserving students and dependents.",
    promo_image: "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=600&q=80",
    promo_link: "https://apc.edu.ph/financial-aid",
    promo_sort_order: 3,
    promo_active_status: true
  }
];

const DEFAULT_SECTIONS = [
  {
    section_id: "sec-1",
    title: "Preferred Program",
    description: "Select your target degree program, entry level, and academic year.",
    sort_order: 1,
    fields: [
      { formfield_id: "f1-1", label: "Academic Year & Term", field_key: "acad_term", field_type: "select", field_options: ["AY 2026-2027, Term 1", "AY 2026-2027, Term 2", "AY 2026-2027, Term 3"], field_required: true, field_help_text: "Upcoming intake", field_placeholder: "Select Academic Term", field_width: "half", field_sort_order: 1, field_locked: true },
      { formfield_id: "f1-2", label: "Applying For", field_key: "app_level", field_type: "select", field_options: ["College/Undergraduate", "Senior High School", "Graduate Studies"], field_required: true, field_help_text: "School level", field_placeholder: "Select Level", field_width: "half", field_sort_order: 2, field_locked: true },
      { formfield_id: "f1-3", label: "Entry Status", field_key: "entry_status", field_type: "select", field_options: ["Freshman", "Transferee", "Second Degree"], field_required: true, field_help_text: "Applicant category", field_placeholder: "Select Status", field_width: "half", field_sort_order: 3, field_locked: true }
    ]
  },
  {
    section_id: "sec-2",
    title: "Basic Information (Per Birth Certificate)",
    description: "Ensure names match your government-issued birth certificate.",
    sort_order: 2,
    fields: [
      { formfield_id: "f2-1", label: "First Name", field_key: "first_name", field_type: "text", field_options: [], field_required: true, field_help_text: "", field_placeholder: "e.g. Juan", field_width: "half", field_sort_order: 1, field_locked: true },
      { formfield_id: "f2-2", label: "Middle Name", field_key: "middle_name", field_type: "text", field_options: [], field_required: false, field_help_text: "Leave blank if none", field_placeholder: "e.g. Santos", field_width: "half", field_sort_order: 2, field_locked: false },
      { formfield_id: "f2-3", label: "Last Name", field_key: "last_name", field_type: "text", field_options: [], field_required: true, field_help_text: "", field_placeholder: "e.g. Dela Cruz", field_width: "half", field_sort_order: 3, field_locked: true },
      { formfield_id: "f2-4", label: "Date of Birth", field_key: "birth_date", field_type: "date", field_options: [], field_required: true, field_help_text: "Must match birth certificate", field_placeholder: "", field_width: "half", field_sort_order: 4, field_locked: true },
      { formfield_id: "f2-5", label: "Sex", field_key: "sex", field_type: "select", field_options: ["Male", "Female", "Prefer not to say"], field_required: true, field_help_text: "Biological sex", field_placeholder: "Select", field_width: "half", field_sort_order: 5, field_locked: false },
      { formfield_id: "f2-6", label: "Nationality", field_key: "nationality", field_type: "text", field_options: [], field_required: true, field_help_text: "", field_placeholder: "Filipino", field_width: "half", field_sort_order: 6, field_locked: false }
    ]
  },
  {
    section_id: "sec-3",
    title: "Contact Details",
    description: "Used to send status updates and verification codes.",
    sort_order: 3,
    fields: [
      { formfield_id: "f3-1", label: "Applicant Email", field_key: "email", field_type: "email", field_options: [], field_required: true, field_help_text: "We will email your login link", field_placeholder: "applicant@gmail.com", field_width: "half", field_sort_order: 1, field_locked: true },
      { formfield_id: "f3-2", label: "Mobile Number", field_key: "mobile", field_type: "tel", field_options: [], field_required: true, field_help_text: "11-digit PH mobile", field_placeholder: "09171234567", field_width: "half", field_sort_order: 2, field_locked: true },
      { formfield_id: "f3-3", label: "Home Address", field_key: "home_address", field_type: "text", field_options: [], field_required: true, field_help_text: "House No., Street, Barangay", field_placeholder: "Unit 4B, Chino Roces Ave.", field_width: "full", field_sort_order: 3, field_locked: false },
      { formfield_id: "f3-4", label: "City / Municipality", field_key: "city", field_type: "text", field_options: [], field_required: true, field_help_text: "", field_placeholder: "Makati City", field_width: "half", field_sort_order: 4, field_locked: false }
    ]
  },
  {
    section_id: "sec-4",
    title: "Previous School Information",
    description: "Information on secondary school background.",
    sort_order: 4,
    fields: [
      { formfield_id: "f4-1", label: "Previous School Name", field_key: "prev_school", field_type: "text", field_options: [], field_required: true, field_help_text: "", field_placeholder: "Pasay City National Science HS", field_width: "half", field_sort_order: 1, field_locked: false },
      { formfield_id: "f4-2", label: "School Sector", field_key: "prev_school_sector", field_type: "select", field_options: ["Private", "Public"], field_required: true, field_help_text: "", field_placeholder: "Select", field_width: "half", field_sort_order: 2, field_locked: false },
      { formfield_id: "f4-3", label: "Last Year Attended", field_key: "prev_school_year", field_type: "text", field_options: [], field_required: true, field_help_text: "e.g. 2025", field_placeholder: "2025", field_width: "half", field_sort_order: 3, field_locked: false }
    ]
  }
];

const DEFAULT_INQUIRIES = [
  {
    inquiry_id: "INQ-94812",
    first_name: "Gabriel",
    last_name: "Reyes",
    email: "gabriel.reyes@gmail.com",
    mobile: "09189876543",
    guardian_name: "Eduardo Reyes",
    guardian_contact: "09176543210",
    program_interest: "BSCS",
    visit_mode: "onsite",
    preferred_date: "2026-05-10",
    question: "Does the Computer Science curriculum have specializations in Cybersecurity or Artificial Intelligence?",
    status: "New",
    created_at: new Date(Date.now() - 3600000 * 4).toISOString(),
    notes: []
  },
  {
    inquiry_id: "INQ-48201",
    first_name: "Samantha",
    last_name: "Tan",
    email: "sam.tan@yahoo.com",
    mobile: "09228887766",
    guardian_name: "Lilian Tan",
    guardian_contact: "09228887755",
    program_interest: "BMMA",
    visit_mode: "online",
    preferred_date: "2026-05-12",
    question: "Can I inquire if there are portfolio review requirements for the Multimedia Arts scholarship?",
    status: "Contacted",
    created_at: new Date(Date.now() - 3600000 * 24).toISOString(),
    notes: [
      {
        note_id: "note-1",
        author_name: "Maria Santos",
        comment: "Called applicant and emailed BMMA portfolio guidelines.",
        created_at: new Date(Date.now() - 3600000 * 18).toISOString()
      }
    ]
  }
];

const DEFAULT_APPLICATIONS = [
  {
    appform_id: "APP-2026-001",
    user_id: "u-app-1",
    course_id: "BSCS",
    course_name: "Bachelor of Science in Computer Science",
    email: "applicant@gmail.com",
    first_name: "Juan",
    middle_name: "Santos",
    last_name: "Dela Cruz",
    mobile: "09171234567",
    entry_status: "Freshman",
    acad_year: "2026-2027",
    term: "Term 1",
    birth_date: "2007-06-15",
    sex: "Male",
    nationality: "Filipino",
    home_address: "APC Compound, 3 Humabon St, Magallanes",
    city: "Makati City",
    prev_school: "Makati Science High School",
    prev_school_sector: "Public",
    prev_school_year: "2025",
    answers: {},
    status: "Qualified",
    officer_notes: "All initial credentials verified. Qualified to pay reservation fee.",
    payment_amount: 5000.00,
    created_at: new Date(Date.now() - 3600000 * 48).toISOString()
  }
];

// Local Storage Helper
function loadStore(key, defaultValue) {
  try {
    const saved = localStorage.getItem(key);
    return saved ? JSON.parse(saved) : defaultValue;
  } catch (e) {
    return defaultValue;
  }
}

function saveStore(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch (e) {}
}

function authHeaders(json = true) {
  const headers = {};
  if (json) headers['Content-Type'] = 'application/json';
  const token = localStorage.getItem('apc_ramconnect_token');
  if (token) headers['Authorization'] = `Bearer ${token}`;
  return headers;
}

async function parseApiError(res, fallbackMsg) {
  const data = await res.json().catch(() => ({}));
  const err = new Error(data.detail || fallbackMsg);
  err.status = res.status;
  return err;
}

export const api = {
  // --- Public CMS Data ---
  async getSettings() {
    try {
      const res = await fetch('/api/public/settings');
      if (res.ok) return await res.json();
    } catch (e) {}
    return loadStore(STORAGE_KEYS.SETTINGS, DEFAULT_SETTINGS);
  },

  async getCourses() {
    try {
      const res = await fetch('/api/public/courses');
      if (res.ok) return await res.json();
    } catch (e) {}
    return loadStore(STORAGE_KEYS.COURSES, DEFAULT_COURSES);
  },

  async getMilestones() {
    try {
      const res = await fetch('/api/public/milestones');
      if (res.ok) return await res.json();
    } catch (e) {}
    return loadStore(STORAGE_KEYS.MILESTONES, DEFAULT_MILESTONES);
  },

  async getPromos() {
    try {
      const res = await fetch('/api/public/promos');
      if (res.ok) return await res.json();
    } catch (e) {}
    return loadStore(STORAGE_KEYS.PROMOS, DEFAULT_PROMOS);
  },

  async getFormSchema() {
    try {
      const res = await fetch('/api/public/form-schema');
      if (res.ok) return await res.json();
    } catch (e) {}
    return loadStore(STORAGE_KEYS.SECTIONS, DEFAULT_SECTIONS);
  },

  // --- Inquiries CRM ---
  async createInquiry(payload) {
    try {
      const res = await fetch('/api/inquiries', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) return await res.json();
    } catch (e) {}

    // Fallback store
    const inquiries = loadStore(STORAGE_KEYS.INQUIRIES, DEFAULT_INQUIRIES);
    const refId = "INQ-" + Math.floor(10000 + Math.random() * 90000);
    const newInquiry = {
      inquiry_id: refId,
      ...payload,
      status: 'New',
      created_at: new Date().toISOString(),
      notes: []
    };
    inquiries.unshift(newInquiry);
    saveStore(STORAGE_KEYS.INQUIRIES, inquiries);
    return { message: "Inquiry submitted successfully.", reference_id: refId, inquiry: newInquiry };
  },

  async getInquiries(status = 'All') {
    try {
      const res = await fetch(`/api/inquiries?status=${encodeURIComponent(status)}`);
      if (res.ok) return await res.json();
    } catch (e) {}
    const list = loadStore(STORAGE_KEYS.INQUIRIES, DEFAULT_INQUIRIES);
    return status === 'All' ? list : list.filter(i => i.status === status);
  },

  async updateInquiryStatus(id, status) {
    try {
      const res = await fetch(`/api/inquiries/${id}/status`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status })
      });
      if (res.ok) return await res.json();
    } catch (e) {}
    const list = loadStore(STORAGE_KEYS.INQUIRIES, DEFAULT_INQUIRIES);
    const target = list.find(i => i.inquiry_id === id);
    if (target) {
      target.status = status;
      saveStore(STORAGE_KEYS.INQUIRIES, list);
    }
    return { inquiry: target };
  },

  async addInquiryNote(id, comment) {
    try {
      const res = await fetch(`/api/inquiries/${id}/notes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ comment })
      });
      if (res.ok) return await res.json();
    } catch (e) {}
    const list = loadStore(STORAGE_KEYS.INQUIRIES, DEFAULT_INQUIRIES);
    const target = list.find(i => i.inquiry_id === id);
    const note = {
      note_id: "note-" + Date.now(),
      author_name: "Admissions Officer",
      comment,
      created_at: new Date().toISOString()
    };
    if (target) {
      if (!target.notes) target.notes = [];
      target.notes.push(note);
      saveStore(STORAGE_KEYS.INQUIRIES, list);
    }
    return { note };
  },

  // --- Applications ---
  async createApplication(payload) {
    try {
      const res = await fetch('/api/applications', {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify(payload)
      });
      if (res.ok) return await res.json();
      throw await parseApiError(res, 'Failed to submit application.');
    } catch (e) {
      if (!(e instanceof TypeError)) throw e;
    }

    // Offline fallback
    const apps = loadStore(STORAGE_KEYS.APPLICATIONS, DEFAULT_APPLICATIONS);
    if (apps.some(a => a.email?.toLowerCase() === payload.email?.toLowerCase())) {
      const err = new Error('An account with this email already exists. Please log in instead.');
      err.status = 409;
      throw err;
    }
    const courses = loadStore(STORAGE_KEYS.COURSES, DEFAULT_COURSES);
    const course = courses.find(c => c.id === payload.course_id);
    const appId = "APP-2026-" + Math.floor(1000 + Math.random() * 9000);
    const birthYear = (payload.birth_date || '').match(/\d{4}/)?.[0] || '';
    const defaultPassword = `${payload.first_name || ''}${payload.last_name || ''}`.replace(/\s+/g, '').toLowerCase() + birthYear;
    const newApp = {
      appform_id: appId,
      course_name: course ? course.name : payload.course_id,
      ...payload,
      status: 'Submitted',
      officer_notes: 'Application received and queued for admission review.',
      payment_amount: 5000.00,
      created_at: new Date().toISOString()
    };
    apps.unshift(newApp);
    saveStore(STORAGE_KEYS.APPLICATIONS, apps);
    return {
      message: "Application submitted successfully.",
      appform_id: appId,
      application: newApp,
      default_password: defaultPassword,
      user: {
        id: 'u-' + Math.random().toString(36).substring(2, 9),
        email: payload.email,
        full_name: `${payload.first_name} ${payload.last_name}`.trim(),
        role: 'applicant',
        token: 'mock_token_applicant'
      }
    };
  },

  async getMyApplication(email) {
    try {
      const url = email ? `/api/applications/my?email=${encodeURIComponent(email)}` : '/api/applications/my';
      const res = await fetch(url, { headers: authHeaders(false) });
      if (res.ok) return await res.json();
      if (res.status === 404 || res.status === 400) return null;
      throw await parseApiError(res, 'Failed to load application.');
    } catch (e) {
      if (!(e instanceof TypeError)) throw e;
    }
    if (!email) return null;
    const apps = loadStore(STORAGE_KEYS.APPLICATIONS, DEFAULT_APPLICATIONS);
    return apps.find(a => a.email?.toLowerCase() === email.toLowerCase()) || null;
  },

  async payReservationFee(appId, paymentPayload) {
    try {
      const res = await fetch(`/api/applications/${appId}/pay`, {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify(paymentPayload)
      });
      if (res.ok) return await res.json();
      throw await parseApiError(res, 'Payment verification failed.');
    } catch (e) {
      if (!(e instanceof TypeError)) throw e;
    }

    const apps = loadStore(STORAGE_KEYS.APPLICATIONS, DEFAULT_APPLICATIONS);
    const app = apps.find(a => a.appform_id === appId);
    if (app) {
      app.status = 'Enrolled';
      app.payment_bank = paymentPayload.bank;
      app.payment_reference = paymentPayload.reference_number;
      app.paid_at = new Date().toISOString();
      const firstInitial = (app.first_name || 's')[0].toLowerCase();
      const lastName = (app.last_name || 'student').toLowerCase().replace(/\s+/g, '');
      app.student_id = `2026-${Math.floor(10000 + Math.random() * 90000)}`;
      app.student_email = `${firstInitial}${lastName}@student.apc.edu.ph`;
      app.officer_notes = "Payment verified. Official student profile synchronized with RAMPortal.";
      saveStore(STORAGE_KEYS.APPLICATIONS, apps);
      return {
        message: "Payment verified and enrollment confirmed!",
        student_id: app.student_id,
        student_email: app.student_email,
        application: app
      };
    }
    throw new Error("Application not found");
  },

  // --- Staff Management ---
  async getApplicants(query = '', status = 'All') {
    try {
      const res = await fetch(`/api/staff/applicants?query=${encodeURIComponent(query)}&status=${encodeURIComponent(status)}`, {
        headers: authHeaders(false)
      });
      if (res.ok) return await res.json();
      throw await parseApiError(res, 'Failed to load applicants.');
    } catch (e) {
      if (!(e instanceof TypeError)) throw e;
    }
    let list = loadStore(STORAGE_KEYS.APPLICATIONS, DEFAULT_APPLICATIONS);
    if (status !== 'All') {
      list = list.filter(a => a.status === status);
    }
    if (query) {
      const q = query.toLowerCase();
      list = list.filter(a => 
        (a.first_name && a.first_name.toLowerCase().includes(q)) ||
        (a.last_name && a.last_name.toLowerCase().includes(q)) ||
        (a.email && a.email.toLowerCase().includes(q)) ||
        (a.course_id && a.course_id.toLowerCase().includes(q))
      );
    }
    return list;
  },

  async updateApplicantStatus(appId, status, officer_notes) {
    try {
      const res = await fetch(`/api/staff/applicants/${appId}/status`, {
        method: 'PATCH',
        headers: authHeaders(),
        body: JSON.stringify({ status, officer_notes })
      });
      if (res.ok) return await res.json();
      throw await parseApiError(res, 'Failed to update applicant status.');
    } catch (e) {
      if (!(e instanceof TypeError)) throw e;
    }
    const apps = loadStore(STORAGE_KEYS.APPLICATIONS, DEFAULT_APPLICATIONS);
    const app = apps.find(a => a.appform_id === appId);
    if (app) {
      app.status = status;
      if (officer_notes) app.officer_notes = officer_notes;
      saveStore(STORAGE_KEYS.APPLICATIONS, apps);
    }
    return { application: app };
  },

  async saveSiteSettings(settings) {
    try {
      const res = await fetch('/api/staff/settings', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(settings)
      });
      if (res.ok) return await res.json();
    } catch (e) {}
    saveStore(STORAGE_KEYS.SETTINGS, settings);
    return { settings };
  },

  async saveFormSections(sections) {
    try {
      const res = await fetch('/api/staff/form-builder', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(sections)
      });
      if (res.ok) return await res.json();
    } catch (e) {}
    saveStore(STORAGE_KEYS.SECTIONS, sections);
    return { sections };
  },

  async updateCourse(courseId, courseData) {
    try {
      const res = await fetch(`/api/staff/courses/${courseId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(courseData)
      });
      if (res.ok) return await res.json();
    } catch (e) {}
    const courses = loadStore(STORAGE_KEYS.COURSES, DEFAULT_COURSES);
    const target = courses.find(c => c.id === courseId);
    if (target) {
      Object.assign(target, courseData);
      saveStore(STORAGE_KEYS.COURSES, courses);
    }
    return { course: target };
  }
};
