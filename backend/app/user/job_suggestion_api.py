from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.claude_client import claude_ask

router = APIRouter()

class SuggestInput(BaseModel):
    query: str

@router.post("/user/suggest-job-titles")
def suggest_job_titles(data: SuggestInput):
    try:
        prompt = f"""
You are a job matching assistant. The user typed part of a job title: "{data.query}".
Suggest 5 complete job titles that are commonly associated with this input.
Only return a JSON list like:
["Data Analyst", "Data Scientist", "BI Analyst", "Marketing Analyst", "Operations Analyst"]
"""
        response = claude_ask(prompt)
        return {"suggestions": eval(response.strip())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Suggestion failed: {e}")


class TitleInput(BaseModel):
    job_title: str

@router.post("/user/suggest-industries")
def suggest_industries(data: TitleInput):
    try:
        prompt = f"""
You are an industry-matching assistant. Based on the job title "{data.job_title}",
suggest 3 to 6 industries this role is commonly found in. Only return a JSON list like:
["Tech", "Finance", "Healthcare"]
"""
        response = claude_ask(prompt)
        return {"industries": eval(response.strip())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Industry suggestion failed: {e}")
