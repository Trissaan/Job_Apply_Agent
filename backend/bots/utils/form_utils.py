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
            else:
                elem.fill(value)
            print(f"✅ Filled '{field['label']}' with '{value}'")
        except Exception as e:
            print(f"❌ Could not fill {field['label']}: {e}")
