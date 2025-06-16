from fastapi import APIRouter, Query
from app.jobs.scrapers.seek import scrape_seek_jobs
import asyncio

router = APIRouter()

@router.get("/seek-jobs", operation_id="get_seek_jobs")
def get_seek_jobs(title: str = Query(..., alias="job_title"), location: str = "melbourne"):
    try:
        jobs = asyncio.run(scrape_seek_jobs(title, location))
        return {"jobs": jobs}
    except Exception as ex:
        return {"error": f"Exception: {str(ex)}"}
