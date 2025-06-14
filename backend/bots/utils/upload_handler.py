from bots.utils.form_utils import extract_possible_upload_targets
from bots.utils.claude_client import get_best_resume_upload_target

def smart_resume_upload(page, resume_path):
    # ✅ Phase 1: Try standard upload
    try:
        print("📎 Trying standard resume upload...")
        page.wait_for_selector("input[type='file']", timeout=5000)
        page.locator("input[type='file']").first.set_input_files(resume_path)
        print("✅ Resume uploaded via standard file input.")
        return True
    except Exception as e:
        print(f"⚠️ Standard upload failed: {e}")

    # 🤖 Phase 2: Claude fallback
    try:
        print("🤖 Attempting Claude-powered fallback to find hidden upload...")
        possible_targets = extract_possible_upload_targets(page)
        best_index = get_best_resume_upload_target(possible_targets)

        if best_index.isdigit():
            el = page.locator("*:visible").nth(int(best_index))
            el.click(force=True)
            page.wait_for_selector("input[type='file']", timeout=5000)
            page.locator("input[type='file']").first.set_input_files(resume_path)
            print("✅ Resume uploaded via Claude-identified fallback.")
            return True
        else:
            print("❌ Claude did not find a valid upload target.")
    except Exception as e:
        print(f"❌ Fallback upload failed: {e}")

    return False
