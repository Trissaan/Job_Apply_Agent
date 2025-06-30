from bots.utils.form_utils import extract_possible_upload_targets
from bots.utils.claude_client import get_best_resume_upload_target
import re 
import boto3
import os

def upload_resume_to_s3(file_path: str, user_id: str):
    s3 = boto3.client("s3")
    bucket_name = os.getenv("S3_BUCKET_NAME")
    object_name = f"resumes/{user_id}/{os.path.basename(file_path)}"

    s3.upload_file(file_path, bucket_name, object_name)
    print(f"✅ Uploaded to S3: {object_name}")

def smart_resume_upload(page, resume_path):
    # ✅ Phase 1: Try standard upload
    try:
        print("📎 Trying standard resume upload...")
        page.wait_for_selector("input[type='file']", timeout=5000)
        page.locator("input[type='file']").first.set_input_files(resume_path)
        print("✅ Resume uploaded via standard file input.")
        return True
    except Exception as e:
        print(f"⚠️ Standard upload failed: {e}")
        page.screenshot(path="png/resume_upload_fallback_attempt.png")

    # 🤖 Phase 2: Claude fallback
    try:
        print("🤖 Attempting Claude-powered fallback to find hidden upload...")
        possible_targets = extract_possible_upload_targets(page)
        best_index = get_best_resume_upload_target(possible_targets)

        best_index = re.findall(r"\b\d+\b", best_index.strip())
        best_index = best_index[0] if best_index else "none"

        if best_index.strip().isdigit():
            index = int(best_index.strip())
            print(f"🤖 Claude says to click element #{index}")
            el = page.locator("*:visible").nth(index)
            el.click(force=True)
            page.wait_for_selector("input[type='file']", timeout=5000)
            page.locator("input[type='file']").first.set_input_files(resume_path)
            print("✅ Resume uploaded via Claude-identified fallback.")
            return True
        else:
            print("❌ Claude did not find a valid upload target.")
    except Exception as e:
        print(f"❌ Fallback upload failed: {e}")

    return False
