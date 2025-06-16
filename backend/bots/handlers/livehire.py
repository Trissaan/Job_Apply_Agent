import os
from bots.utils.claude_client import get_best_apply_button
from bots.utils.form_utils import extract_form_fields, fill_form_by_index
from bots.utils.claude_field_mapper import get_field_mapping_from_claude
from app.resume.gpt_utils import generate_cover_letter  
from app.resume.export_utils import generate_pdf_from_text
from bots.utils.job_parser import extract_job_details_ai
from bots.utils.upload_handler import smart_resume_upload
from bots.utils.logger import log_application



def apply_livehire(page, resume_path, user_info):
    print("🧠 Starting LiveHire Application Process...")

    try:
        # Step 1: Extract Job Title & Description using AI
        job_title, company, jd_text, tags = extract_job_details_ai(page)
        print(f"🧠 Claude-extracted title: {job_title}")
        print(f"📄 JD length: {len(jd_text)} chars")

        # Step 2: Generate cover letter and save PDF
        cover_letter_text = generate_cover_letter(jd_text, user_info.get("resume_text", ""), job_title)
        cover_letter_path = generate_pdf_from_text(cover_letter_text)
        user_info["cover_letter"] = cover_letter_text
        user_info["cover_letter_path"] = cover_letter_path

        # Step 3: Find and click the best apply button
        page.wait_for_selector("button", timeout=10000)
        buttons = page.locator("button")
        matched_button = None
        for i in range(buttons.count()):
            text = buttons.nth(i).text_content()
            if text and any(keyword in text.strip().lower() for keyword in ["resume", "cv", "upload"]):
                matched_button = buttons.nth(i)
                print(f"✅ Found resume-related button: '{text.strip()}'")
                break

        if not matched_button:
            texts = [btn.text_content() for btn in buttons.element_handles()]
            best_button = get_best_apply_button(texts)
            print(f"🤖 Claude says to click: '{best_button}'")
            matched_button = page.locator(f"button:has-text('{best_button}')").first

        matched_button.wait_for(timeout=10000)
        matched_button.click()

        # Step 4: Initial form filling phase
        print("📝 Phase 1: Filling initial form fields...")
        fields = extract_form_fields(page)
        mapping = get_field_mapping_from_claude(user_info, fields)
        fill_form_by_index(page, fields, mapping, user_info)

        """# Step 5: Wait for dynamic form elements (like file upload)
        try:
            print("📎 Waiting for resume upload field to appear...")
            page.wait_for_selector("input[type='file']", timeout=15000)
            page.locator("input[type='file']").first.set_input_files(resume_path)
            print("📎 Resume uploaded after dynamic form load.")
        except Exception as e:
            print(f"❌ Resume upload failed: {e}")"""
        # Step 5: Upload resume using hybrid strategy
        if smart_resume_upload(page, resume_path):
            print("📎 Resume upload complete.")
        else:
            print("⚠️ Resume upload could not be completed. Proceeding anyway...")

        # Step 6 (Optional): Re-extract and re-fill any new fields
        print("🔁 Phase 2: Rechecking form after dynamic load...")
        updated_fields = extract_form_fields(page)
        updated_mapping = get_field_mapping_from_claude(user_info, updated_fields)
        fill_form_by_index(page, updated_fields, updated_mapping, user_info)

        # Step 7: Submit application
        try:
            submit = page.locator("button[type='submit'], button:has-text('Submit'), button:has-text('Apply')").first
            submit.click()
            print("🚀 Application submitted.")
            log_application(
                job_title=job_title,
                company=company,
                job_description=jd_text,
                cover_letter_text=cover_letter_text,
                platform="LiveHire",
                job_url=page.url,
                tags=tags
            )


        except Exception as e:
            print(f"❌ Could not click submit button: {e}")

        # Step 8: Screenshot for success
        page.screenshot(path="png/livehire_success.png")

        # Step 9: Cleanup
        try:
            os.remove(cover_letter_path)
            print("🧹 Cleaned up temporary cover letter PDF.")
        except Exception as e:
            print(f"⚠️ Could not delete temp PDF: {e}")

    except Exception as e:
        print(f"❌ Failed to apply on LiveHire: {e}")
        page.screenshot(path="png/livehire_failed.png")
