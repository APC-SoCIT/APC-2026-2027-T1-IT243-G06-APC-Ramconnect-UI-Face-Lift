# APC RamConnect - Modern Online Admissions System

Modern, mobile-responsive web-based admissions platform for **Asia Pacific College (APC)**. Built with a decoupled component architecture using **Vue.js 3** on the frontend, **Python FastAPI** on the backend, **Supabase** for database management, and configured for seamless deployment on **Vercel**.

---

## 🚀 Tech Stack

* **Frontend:** Vue.js 3 (Composition API), Vite, Tailwind CSS, Pinia, Lucide Icons
* **Backend:** Python 3.11+, FastAPI, Pydantic v2, Uvicorn
* **Database & Auth:** Supabase (PostgreSQL with RLS), REST API & Fallback Store
* **Deployment:** Vercel (Vue SPA + Serverless Python Function via `vercel.json`)

---

## 📁 Project Architecture

```text
Prototype/
├── api/                       # Python FastAPI Backend (Vercel Serverless Function)
│   ├── index.py               # Main FastAPI app & CORS configuration
│   ├── config.py              # Supabase & JWT settings
│   ├── database.py            # Supabase connection & in-memory fallback
│   ├── schemas.py             # Pydantic validation schemas
│   ├── routers/               # Auth, Public CMS, Inquiries, Applications, Staff
│   └── requirements.txt       # Python dependencies
├── src/                       # Vue.js 3 Frontend
│   ├── components/            # CoursePicker, DynamicFormRenderer, PaymentModal, CRM Drawers
│   ├── views/                 # Home, Inquire, Apply, Portal, Login, Register, Staff Hub
│   ├── router/                # Vue Router with RBAC guards
│   ├── stores/                # Pinia state stores (auth, siteSettings)
│   ├── api/client.js          # Unified API client
│   └── style.css              # APC Brand styling (#FDB813 Gold, #0B1E3D Navy)
├── supabase/
│   ├── schema.sql             # Complete PostgreSQL schema (tables, constraints, indexes)
│   └── seed.sql               # Seed data for APC degree programs, form sections, and demo users
├── package.json               # NPM scripts and frontend dependencies
├── vite.config.js             # Vite config with API proxy
├── tailwind.config.js         # APC official brand color palette
└── vercel.json                # Vercel deployment configuration
```

---

## 🛠️ Quick Start & Local Development

### 1. Frontend Setup
From the `Prototype` directory:
```bash
# Install dependencies
npm install

# Start Vite development server (http://localhost:5173)
npm run dev
```

### 2. Backend Setup (Optional for API testing)
```bash
# Install Python packages
pip install -r api/requirements.txt

# Start FastAPI server (http://localhost:8000)
uvicorn api.index:app --reload --port 8000
```
*Note: The frontend includes seamless fallback data persistence so you can test all views, forms, payment simulation, and staff CRM functions even without running the Python backend locally.*

---

## 🔑 Demo Access Credentials

| User Role | Email | Password | Target Interface |
| :--- | :--- | :--- | :--- |
| **Admissions Staff** | `admissions@apc.edu.ph` | `admin123` | `/staff` (CRM, Dossiers, Form Builder, CMS) |
| **Prospective Applicant** | `applicant@gmail.com` | `user123` | `/portal` (Status Stepper & Online Reservation) |

*(Quick-fill buttons are also provided directly on the `/login` screen).*

---

## ☁️ Vercel Deployment

1. Push your repository to GitHub on branch `Prototype-Remake`.
2. Connect the repository to your [Vercel Dashboard](https://vercel.com).
3. Set the Root Directory in Vercel to `Prototype`.
4. (Optional) Set the following environment variables in Vercel:
   * `SUPABASE_URL`: Your Supabase Project URL
   * `SUPABASE_KEY`: Your Supabase Anon or Service Role Key
5. Click **Deploy**. Vercel will automatically build the Vue.js frontend and route `/api/*` to the Python FastAPI backend.
