import requests

# ✅ Set your local environment config
base_url = "http://localhost:8000/api"
auth_token = "your_jwt_token_here"  # 🔐 Replace with your real JWT
headers = {"Authorization": f"Bearer {auth_token}"}
resume_path = "temp/your_resume.pdf"  # 🔄 Update with your resume path

# Upload Resume
print("\n📤 Step 1: Uploading Resume")
with open(resume_path, "rb") as resume_file:
    files = {"file": resume_file}
    res = requests.post(f"{base_url}/upload-resume", headers=headers, files=files)
    print("Status:", res.status_code)
    print("Response:", res.json())

# Trigger Dry-Run Apply
print("\n🚀 Step 2: Triggering Dry-Run Apply")
res = requests.post(f"{base_url}/apply-now?dry_run=true", headers=headers)
print("Status:", res.status_code)
print("Response:", res.json())
