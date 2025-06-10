from apply_engine import apply_to_job

dummy_resume = "E:\\Personal\\Resume\\Trissaan_A_S Resume .pdf"

user_data = {
    "first_name": "Trissaan",
    "last_name": "Shanmugasundaram",
    "email": "trissaan@example.com",
    "phone": "0412345678"
}

# test with a real apply link you scraped
apply_link = "https://www.livehire.com/careers/wearekinetic/job/KKHGN/QJJHYPZJP8/principal-cloud-data-engineer?source=SEEK"

apply_to_job(apply_link, dummy_resume, user_data)
