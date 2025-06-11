from utils.claude_client import get_best_apply_button

def apply_livehire(page, resume_path, user_info):
    print("🧠 Using Claude to choose apply button...")

    try:
        # Step 1: Wait for buttons to load
        page.wait_for_selector("button", timeout=10000)
        buttons = page.locator("button")
        texts = [btn.text_content() for btn in buttons.element_handles()]
        print(f"🧠 Found buttons: {texts}")

        best_button = get_best_apply_button(texts)
        print(f"🤖 Claude says to click: '{best_button}'")

        # Step 2: Click that button
        button = page.locator(f"button:has-text('{best_button}')")
        button.wait_for(timeout=10000)
        button.click()

        # Step 3: Continue with form filling like before
        page.wait_for_selector("input#firstName", timeout=15000)
        page.fill("input#firstName", user_info["first_name"])
        page.fill("input#lastName", user_info["last_name"])
        page.fill("input#emailAddress", user_info["email"])
        page.fill("input#mobileNumber", user_info["phone"])
        page.set_input_files("input[type='file']", resume_path)
        page.click("button[type='submit']")

        print("✅ Application submitted on LiveHire.")
        page.screenshot(path="livehire_success.png")

    except Exception as e:
        print(f"❌ Failed to apply on LiveHire: {e}")
        page.screenshot(path="livehire_failed.png")
