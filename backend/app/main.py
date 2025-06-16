from fastapi import FastAPI
from app.auth.auth_api import router as auth_router
from app.resume.resume_api import router as resume_router
from app.user.preferences import router as prefs_router
from app.jobs.job_scraper_api import router as scraper_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "AI Job Agent Backend is running!"}

# Register routes
app.include_router(auth_router, prefix="/auth")
app.include_router(resume_router, prefix="/resume")
app.include_router(prefs_router, prefix="/user")
app.include_router(scraper_router, prefix="/jobs")
