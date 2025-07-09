# ai_website_generator/ai/generator.py

import json
import re
from ..config import MODEL_NAME_PRO, MODEL_NAME_FLASH
from . import core
from . import prompts


def ai_generate_master_plan(user_prompt: str) -> dict | None:
    """Uses Gemini to generate the master design plan JSON."""
    print(f"\n[AI] 🧠 Generating master design plan for '{user_prompt}'...")
    prompt = prompts.get_master_plan_prompt(user_prompt)
    response_text = core.generate_content(
        MODEL_NAME_PRO, prompt, response_mime_type="application/json", timeout=180
    )

    if not response_text:
        return None

    try:
        # Gemini JSON mode is good but sometimes can have trailing commas
        cleaned_text = re.sub(r",\s*([]}])", r"\1", response_text)
        master_plan = json.loads(cleaned_text)
        print("[AI] ✅ Master design plan generated and parsed successfully!")
        return master_plan
    except json.JSONDecodeError as e:
        print(f"[AI] ❌ ERROR: Failed to parse JSON from master plan response: {e}")
        print(f"[AI]    > Raw Response:\n{response_text}")
        return None


def ai_generate_template(section_type: str, example_content: dict) -> str | None:
    """Uses Gemini to generate a robust HTML template snippet."""
    print(f"\n[AI] 🏗️  Generating HTML template for '{section_type}'...")
    prompt = prompts.get_template_prompt(section_type, example_content)
    response_text = core.generate_content(MODEL_NAME_FLASH, prompt, timeout=120)

    if response_text:
        print(f"[AI] ✅ HTML template for '{section_type}' generated successfully!")
    return response_text


# --- ！！！小修改！！！ ---
# 函数签名已更新，以接收 design_specs_str
def ai_generate_css(master_plan: dict, design_specs_str: str) -> str:
    """Generates website CSS styles based on the master plan and design specs."""
    print("\n[AI] 🎨 Generating CSS styles based on theme and design document...")

    prompt = prompts.get_css_prompt(master_plan, design_specs_str)
    response_text = core.generate_content(MODEL_NAME_FLASH, prompt, timeout=120)

    if response_text:
        print("[AI] ✅ CSS styles generated successfully!")
        return response_text
    else:
        return "/* AI failed to generate CSS. Please check logs. */"


def ai_write_design_doc(master_plan: dict) -> str:
    """Generates a detailed Markdown design document from the master plan."""
    print("\n[AI] ✍️  Writing detailed professional design document...")
    if not master_plan:
        return "# Design Document Generation Failed\n\nMaster plan was empty."

    prompt = prompts.get_design_doc_prompt(master_plan)
    response_text = core.generate_content(MODEL_NAME_PRO, prompt, timeout=240)

    if response_text:
        print("[AI] ✅ Detailed design document generated successfully!")
        return response_text
    else:
        return f"# Design Document Generation Failed\n\nAn error occurred during generation. Check logs."


def ai_fix_template(
    broken_html: str, error_message: str, section_type: str
) -> str | None:
    """Uses a dedicated AI prompt to fix a broken Jinja2 template."""
    print(f"\n[AI-FIXER] 🩺 Attempting to fix template for '{section_type}'...")
    print(f"[AI-FIXER]    > Error: {error_message}")

    prompt = prompts.get_fix_template_prompt(broken_html, error_message, section_type)

    response_text = core.generate_content(MODEL_NAME_PRO, prompt, timeout=120)

    if response_text:
        print(f"[AI-FIXER] ✅ Template for '{section_type}' has been corrected by AI.")
    else:
        print(f"[AI-FIXER] ❌ AI failed to provide a fix for '{section_type}'.")

    return response_text
