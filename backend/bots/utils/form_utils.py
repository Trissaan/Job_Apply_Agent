def extract_form_fields(page):
    fields = []
    inputs = page.locator("input, textarea, select")

    for i in range(inputs.count()):
        elem = inputs.nth(i)
        try:
            if not elem.is_visible():
                continue
            label = elem.evaluate(
                """el => {
                    const label = el.labels?.[0]?.innerText || el.placeholder || el.getAttribute("aria-label") || el.name || el.id || "";
                    return label.trim();
                }"""
            )
            tag = elem.evaluate("el => el.tagName.toLowerCase()")
            field_type = elem.get_attribute("type") or tag
            fields.append({
                "index": i,
                "label": label,
                "type": field_type
            })
        except Exception:
            continue
    return fields


def fill_form_by_index(page, field_list, index_mapping, user_info):
    inputs = page.locator("input, textarea, select")

    for field in field_list:
        i = field["index"]
        user_key = index_mapping.get(str(i))

        if not user_key or user_key not in user_info:
            continue

        value = user_info[user_key]
        elem = inputs.nth(i)
        try:
            tag = field["type"]
            if tag == "checkbox":
                if value in [True, "true", "yes", "on"]:
                    elem.check()
            elif tag == "select":
                elem.select_option(label=value)
            elif tag == "file" and user_key.endswith("_path"):
                page.set_input_files(elem, value)
                print(f"📎 Uploaded file for '{field['label']}'")
            else:
                elem.fill(value)
                print(f"✅ Filled '{field['label']}' with '{value[:30]}'")
        except Exception as e:
            print(f"❌ Could not fill field {field['label']}: {e}")
def extract_possible_upload_targets(page):
    elements = page.locator("*:visible")
    potential_uploads = []

    for i in range(min(elements.count(), 100)):  # Limit for performance
        try:
            el = elements.nth(i)
            tag = el.evaluate("e => e.tagName.toLowerCase()")
            text = el.text_content().strip()
            aria = el.get_attribute("aria-label") or ""
            class_attr = el.get_attribute("class") or ""

            combined = f"{text} {aria} {class_attr}".lower()
            if any(keyword in combined for keyword in ["upload", "resume", "cv", "drag", "drop", "file"]):
                potential_uploads.append({
                    "index": i,
                    "tag": tag,
                    "text": text,
                    "aria": aria,
                    "classes": class_attr
                })
        except:
            continue

    return potential_uploads


