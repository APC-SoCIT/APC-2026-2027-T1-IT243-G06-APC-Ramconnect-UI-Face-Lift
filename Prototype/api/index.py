from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, public, inquiries, applications, staff

app = FastAPI(
    title="APC RamConnect Admissions API",
    description="High-performance backend API powering the APC RamConnect admissions platform.",
    version="2.0.0"
)

# Enable CORS for local Vite dev and Vercel production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes under /api
app.include_router(auth.router, prefix="/api")
app.include_router(public.router, prefix="/api")
app.include_router(inquiries.router, prefix="/api")
app.include_router(applications.router, prefix="/api")
app.include_router(staff.router, prefix="/api")

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "APC RamConnect API",
        "version": "2.0.0"
    }
