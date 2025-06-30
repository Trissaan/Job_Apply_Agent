import requests

# ✅ Set your local environment config
base_url = "http://localhost:8000"
auth_token = "eyJraWQiOiJQYjJUMmp0SDdqSk5pRTdcL09HMnZ2WWhqR3U5UVFxd05wb25kRzJIRUpaND0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJjOTFlZTQxOC03MGMxLTcwZTMtMGQwOC1mNTBkYWNlNTY4ODYiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuYXAtc291dGhlYXN0LTIuYW1hem9uYXdzLmNvbVwvYXAtc291dGhlYXN0LTJfdlNvbkJwaHVQIiwiY2xpZW50X2lkIjoiNXQwdjgxOXVwZW0xdW5lcjB1cjVyOTZtNGsiLCJvcmlnaW5fanRpIjoiNWYxZWI4NDMtZjYwMy00YTk5LTljMzMtMGI3MmMyMjcxMDI1IiwiZXZlbnRfaWQiOiI2ODBiYmUyYi0zNzBjLTRlNDEtYmJhOS0zMjU2MGUyODZkYzUiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIiwiYXV0aF90aW1lIjoxNzUxMTc3MDQ3LCJleHAiOjE3NTExODA2NDcsImlhdCI6MTc1MTE3NzA0NywianRpIjoiYTE1ZWQwZWMtOGE5YS00NDgzLWEzYTUtMTJkYjNkMGQyZTdiIiwidXNlcm5hbWUiOiJjOTFlZTQxOC03MGMxLTcwZTMtMGQwOC1mNTBkYWNlNTY4ODYifQ.Lc1hUCXUAFLmbLmfEKyDvyJgTA-wFQ1kD11_0bSQXSke7k6t0FUykSZcp-2TA9qjWHTxcbVetE0C7v5YUn8kus_8v8wRQ5LCoEvmewfUXDCYL9ZIgfggBZghCcgKG42fbkWDLMrGlnQedfwiRzFgZo6iyHA6hiyD2F8e4NcLWRA4MQI2ULX8899v6sbUr6OP9DPPoXMoeWEMH6ySOYtI71b-2_Zq_9-352RW23ZuyqJwVsb4yBs8mxJsBi0adA4UKKiMOupvOUDNi2JqCilcrl2-toeYz243HKo_W7tSG4FYNlrZ7hq7ftzsnse-dQvLrQUlZ8BJFMQmw3q7-DPwEQ"  # 🔐 Replace with your actual JWT
headers = {"Authorization": f"Bearer {auth_token}"}

# ✅ FIXED Windows path issue (use raw string or escape slashes)
resume_path = r"E:\Personal\Resume\Base resume\Trissaan_A_S Resume .pdf"

# ✅ Correct endpoint paths based on your `main.py` setup
upload_resume_url = f"{base_url}/resume/upload-resume"       # Or use /api/resume/upload-resume if you remount the prefix
apply_now_url = f"{base_url}/api/apply-now?dry_run=true"      # Apply now with dry-run mode

# Track results
print("\n📤 Step 1: Uploading Resume")
try:
    with open(resume_path, "rb") as resume_file:
        files = {"file": resume_file}
        response = requests.post(upload_resume_url, headers=headers, files=files)
        print("Status:", response.status_code)
        print("Response:", response.json())
except Exception as e:
    print("❌ Upload failed:", e)

print("\n🚀 Step 2: Triggering Dry-Run Apply")
try:
    response = requests.post(apply_now_url, headers=headers)
    print("Status:", response.status_code)
    print("Response:", response.json())
except Exception as e:
    print("❌ Dry-run failed:", e)
