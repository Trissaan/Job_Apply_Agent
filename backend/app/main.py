from fastapi import FastAPI
from app.auth.routes import router as auth_router  # Import the router
from app.resume.routes import router as resume_router
from app.routes.preferences import router as prefs_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "AI Job Agent Backend is running!"}

# Add routes
app.include_router(auth_router, prefix="/auth")
app.include_router(resume_router, prefix="/resume")
app.include_router(prefs_router, prefix="/user")