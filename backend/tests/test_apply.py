from bots.apply_engine import apply_to_job

resume_path = "E:\\Personal\\Resume\\Trissaan_A_S Resume .pdf"

user_info = {
    "first_name": "Trissaan",
    "last_name": "Shanmugasundaram",
    "email": "trissaan@gmail.com",
    "phone": "0434549364"
}

# test with a real apply link you scraped
job_url = "https://www.livehire.com/careers/wearekinetic/job/KKHGN/QJJHYPZJP8/principal-cloud-data-engineer?source=SEEK"

apply_to_job(job_url, resume_path, user_info)
