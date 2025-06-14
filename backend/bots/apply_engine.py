from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
from bots.handlers.workday import apply_workday
from bots.handlers.greenhouse import apply_greenhouse
from bots.handlers.lever import apply_lever
from bots.handlers.livehire import apply_livehire
from bots.handlers.google_form import apply_google_form

def detect_platform(url: str):
    if "workday" in url:
        return "workday"
    elif "greenhouse" in url:
        return "greenhouse"
    elif "lever" in url:
        return "lever"
    elif "livehire" in url:
        return "livehire"
    elif "docs.google.com/forms" in url:
        return "google_form"
    else:
        return "unknown"

def apply_to_job(url: str, resume_path: str, user_info: dict):
    platform = detect_platform(url)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        page.goto(url, timeout=60000)

        if platform == "workday":
            apply_workday(page, resume_path, user_info)
        elif platform == "greenhouse":
            apply_greenhouse(page, resume_path, user_info)
        elif platform == "lever":
            apply_lever(page, resume_path, user_info)
        elif platform == "livehire":
            apply_livehire(page, resume_path, user_info)
        elif platform == "google_form":
            apply_google_form(page, resume_path, user_info)
        else:
            print(f"[!] Unknown platform for: {url}")
        
        browser.close()
