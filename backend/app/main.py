import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.auth_api import router as auth_router
from app.resume.resume_api import router as resume_router
from app.user.preferences import router as prefs_router
from app.user import dashboard_api
from app.jobs.job_scraper_api import router as scraper_router
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer
from app.user.job_suggestions_api import router as suggest_router
from app.jobs.auto_apply_scheduler import scheduler  
from app.jobs.apply_now_api import router as apply_now_router
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()

bearer_scheme = HTTPBearer()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="AI Job Agent",
        version="1.0.0",
        description="Backend for AI Job Agent with JWT Auth",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"bearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
scheduler = BackgroundScheduler()
@app.on_event("startup")
def start_scheduler():
    if not scheduler.running:
        scheduler.start()
        print("✅ Scheduler started")
    
@app.get("/")
def read_root():
    return {"message": "AI Job Agent Backend is running!"}

# Register routes
app.include_router(auth_router, prefix="/auth")
app.include_router(resume_router, prefix="/resume")
app.include_router(prefs_router, prefix="/user")
app.include_router(scraper_router, prefix="/jobs")
app.include_router(suggest_router)
app.include_router(apply_now_router, prefix = "/api")
app.include_router(dashboard_api.router)
