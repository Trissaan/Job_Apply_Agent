from utils.claude_client import get_best_apply_button
from app.utils.form_utils import extract_form_fields, fill_form_by_index
from app.utils.claude_field_mapper import get_field_mapping_from_claude

def apply_livehire(page, resume_path, user_info):
    print("🧠 Starting LiveHire Application Process...")

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

        # Step 5: Extract form structure
        print("🔍 Extracting visible form fields...")
        fields = extract_form_fields(page)

        # Step 6: Get Claude's index-to-userinfo mapping
        print("🧠 Asking Claude to map fields to user info...")
        mapping = get_field_mapping_from_claude(user_info, fields)

        # Step 7: Fill the form
        fill_form_by_index(page, fields, mapping, user_info)

        # Step 8: Upload Resume
        try:
            page.set_input_files("input[type='file']", resume_path)
            print("📎 Resume uploaded.")
        except Exception as e:
            print(f"❌ Resume upload failed: {e}")

        # Step 9: Submit the form
        try:
            submit = page.locator("button[type='submit'], button:has-text('Submit'), button:has-text('Apply')").first
            submit.click()
            print("🚀 Application submitted.")
        except Exception as e:
            print(f"❌ Could not click submit button: {e}")

        # Step 10: Screenshot
        page.screenshot(path="png/livehire_success.png")

    except Exception as e:
        print(f"❌ Failed to apply on LiveHire: {e}")
        page.screenshot(path="png/livehire_failed.png")
