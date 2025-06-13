from utils.claude_client import get_best_apply_button

def apply_livehire(page, resume_path, user_info):
    print("🧠 Trying to find a resume-related button first...")

    try:
        # Step 1: Wait for buttons to load
        page.wait_for_selector("button", timeout=10000)
        buttons = page.locator("button")

        # Step 2: Try to find a resume-related button
        matched_button = None
        for i in range(buttons.count()):
            text = buttons.nth(i).text_content()
            if text:
                clean_text = text.strip().lower()
                if any(keyword in clean_text for keyword in ["resume", "cv", "upload"]):
                    matched_button = buttons.nth(i)
                    print(f"✅ Found resume-related button: '{clean_text}'")
                    break

        # Step 3: Fallback to Claude if no match
        if not matched_button:
            print("🤖 No resume-related button found. Using Claude...")
            texts = [btn.text_content() for btn in buttons.element_handles()]
            print(f"🧠 Found buttons: {texts}")
            best_button = get_best_apply_button(texts)
            print(f"🤖 Claude says to click: '{best_button}'")
            matched_button = page.locator(f"button:has-text('{best_button}')").first

        # Step 4: Click the matched button
        matched_button.wait_for(timeout=10000)
        matched_button.click()

        # Step 5: Fill the form
        page.wait_for_selector("input#firstName", timeout=15000)
        page.fill("input#firstName", user_info["first_name"])
        page.fill("input#lastName", user_info["last_name"])
        page.fill("input#emailAddress", user_info["email"])
        page.fill("input#mobileNumber", user_info["phone"])
        page.set_input_files("input[type='file']", resume_path)
        page.click("button[type='submit']")

        print("✅ Application submitted on LiveHire.")
        page.screenshot(path="png/livehire_success.png")

    except Exception as e:
        print(f"❌ Failed to apply on LiveHire: {e}")
        page.screenshot(path="livehire_failed.png")
