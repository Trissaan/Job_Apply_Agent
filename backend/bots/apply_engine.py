from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
from bots.apply_handlers.workday import apply_workday
from bots.apply_handlers.greenhouse import apply_greenhouse
from bots.apply_handlers.lever import apply_lever
from bots.apply_handlers.livehire import apply_livehire
from bots.apply_handlers.google_form import apply_google_form
from bots.utils.claude_client import get_best_apply_button


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
        page.wait_for_load_state("load")

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
            print(f" Unknown platform. Using Claude to pick best button...")

            # STEP 1: Get all buttons and links
            button_elements = page.locator("button, a").all()
            button_texts = []

            for btn in button_elements:
                try:
                    text = btn.inner_text().strip()
                    if text:
                        button_texts.append(text)
                except:
                    continue

            print(" Found buttons:", button_texts)

            # STEP 2: Ask Claude which to click
            try:
                chosen_label = get_best_apply_button(button_texts)
                print("Claude picked:", chosen_label)

                if chosen_label.lower() == "none":
                    print(" Claude couldn't determine a suitable button.")
                else:
                    try:
                        page.click(f"text='{chosen_label}'", timeout=5000)
                        print(f" Clicked: {chosen_label}")
                    except Exception as click_err:
                        print(f"Failed to click Claude-picked button: {click_err}")

            except Exception as e:
                print(f" Claude failed to choose a button: {e}")

        browser.close()

