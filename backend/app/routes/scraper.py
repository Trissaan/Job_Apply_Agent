from fastapi import APIRouter, Query
import subprocess
import json

router = APIRouter()

@router.get("/seek-jobs", operation_id="get_seek_jobs")
def get_seek_jobs(title: str = Query(..., alias="job_title"), location: str = "melbourne"):
    try:
        result = subprocess.check_output(
            ["python", "bots/seek_worker.py", title, location],
            text=True
        )

        print("🔍 RAW subprocess output:")
        #print(result)  # This will show what's breaking json.loads()

        # TEMP: return raw output instead of parsing it
        #return {"raw_output": result}
        parsed = json.loads(result)
        return {"jobs": parsed}

    except subprocess.CalledProcessError as e:
        return {"error": f"CalledProcessError: {e.output}"}
    except Exception as ex:
        return {"error": f"Exception: {str(ex)}"}
