from playwright.async_api import async_playwright
import traceback
import difflib
from bots.utils.claude_client import get_best_apply_button

async def apply_to_seek_job(job_url: str, resume_path: str, name: str, email: str):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)  # Set to True for prod
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto(job_url, timeout=20000)
            print(f"Visiting job: {job_url}")

            # 🔍 Step 1: Get all visible buttons
            buttons = await page.query_selector_all("button")
            button_texts = []

            for btn in buttons:
                try:
                    label = (await btn.text_content() or "").strip()
                    if label:
                        button_texts.append(label)
                except:
                    continue

            if not button_texts:
                print("⚠️ No visible buttons found.")
                raise RuntimeError("no_buttons_found")

            # 🧠 Step 2: Ask Claude which button to click
            best_button_label = get_best_apply_button(button_texts)
            print(f"🤖 Claude suggests: '{best_button_label}'")

            # 🖱️ Step 3: Click the correct button
            clicked = False
            for btn in buttons:
                text = (await btn.text_content() or "").strip()
                if text.lower() in best_button_label.lower() or best_button_label.lower() in text.lower():
                    await btn.click()
                    clicked = True
                    print(f"✅ Clicked fuzzy-matched button: '{text}' (Claude said: '{best_button_label}')")
                    await page.wait_for_timeout(3000)
                    break

            # Optional: use difflib for best match if still not found
            if not clicked:
                close_match = difflib.get_close_matches(best_button_label, button_texts, n=1, cutoff=0.6)
                if close_match:
                    for btn in buttons:
                        text = (await btn.text_content() or "").strip()
                        if text == close_match[0]:
                            await btn.click()
                            clicked = True
                            print(f"✅ Clicked closest match: '{text}'")
                            await page.wait_for_timeout(3000)
                            break

            # 📁 Step 4: Upload resume
            file_input = await page.query_selector('input[type="file"]')
            if file_input:
                await file_input.set_input_files(resume_path)
                print(f"📎 Resume uploaded: {resume_path}")
            else:
                print("⚠️ Resume upload field not found.")

            # 👤 Step 5: Fill in name/email (if fields exist)
            try:
                name_input = await page.query_selector('input[name="name"]')
                if name_input:
                    await name_input.fill(name)

                email_input = await page.query_selector('input[name="email"]')
                if email_input:
                    await email_input.fill(email)
            except:
                print("ℹ️ Optional fields not found or already pre-filled.")

            # ✅ Step 6: Submit the application
            try:
                submit_button = await page.query_selector('button[type="submit"]')
                if submit_button:
                    await submit_button.click()
                    print("✅ Application submitted!")
            except:
                print("⚠️ Could not find Submit button")

            await page.wait_for_timeout(3000)
            await browser.close()

    except RuntimeError as err:
        print(f"⚠️ Skipped job due to logic: {err}")
        traceback.print_exc()
    except Exception:
        print("❌ Failed to apply to Seek job")
        traceback.print_exc()
