# ai_website_generator/ai/prompts.py

import json


def get_master_plan_prompt(user_prompt: str) -> str:
    # 这个提示词本身已经很好，无需修改
    return f"""
    Act as a professional web design strategist. For a user requesting a website about "{user_prompt}", create a comprehensive website plan in a single, valid JSON object.

    The JSON object must contain:
    - `site_title`: A creative and fitting title for the website.
    - `theme_description`: A short paragraph describing the visual mood, style, and concept.
    - `sections`: An array of objects, where each object represents a section of the website.
      Each section object must have:
      - `type`: A unique, descriptive, snake_case name for the section (e.g., "hero_section", "featured_models_section").
      - `content`: An object containing all the text and image data for that section. Use descriptive keys. If there's a list of items (like features, gallery images, models), use a key ending in `_list` (e.g., `features_list`, `gallery_images_list`). For images, provide an object with `image_prompt` and `image_size`.

    Generate the full JSON plan now. Ensure the JSON is perfectly formatted, with no trailing commas or extra text.
    """


def get_template_prompt(section_type: str, example_content: dict) -> str:
    # --- ！！！重大修改！！！ ---
    # 这个提示词被大幅强化，强制AI遵循严格的规则
    return f"""
    You are an expert Jinja2 and HTML template designer.
    Generate a single, robust HTML `<section>` block for a section of type '{section_type}'.

    **CRITICAL INSTRUCTIONS (MUST BE FOLLOWED):**

    1.  **CSS CLASS NAMES:**
        *   The main `<section>` tag MUST have a class `section-{section_type}`.
        *   All child elements inside the section MUST use BEM-style class names. The format is `section-{section_type}__element--modifier`.
        *   Example: For `hero_section`, the title's class must be `section-hero_section__heading`. A button's class could be `section-hero_section__button` or `section-hero_section__cta`.
        *   **THIS IS NOT OPTIONAL. Follow this naming convention precisely.**

    2.  **DATA RENDERING:**
        *   Use `{{{{ variable }}}}` for all text placeholders.
        *   **ALWAYS check for existence** with `{{% if variable %}}` before trying to display it.
        *   **LISTS:** For any key ending in `_list` (e.g., `models_list`), you MUST iterate over it using `{{% for item in models_list %}}`. Inside the loop, access properties with `{{{{ item.property }}}}`.
        *   **IMAGES:** If you find a key named `image`, `background_image`, or `preview_image`, it is an object. You MUST generate an `<img>` tag.
            - The `src` attribute MUST be `{{{{ ...image.image_url }}}}`. (e.g., `{{{{ image.image_url }}}}`, `{{{{ item.image.image_url }}}}`).
            - The `alt` attribute SHOULD be `{{{{ ...image.image_prompt }}}}`.
        *   **PLACEHOLDER PROMPTS:** If a key ends in `_prompt` (e.g., `search_filter_prompt`), simply render its text content within a `<div>` or `<p>` tag for placeholder purposes.

    3.  **HTML STRUCTURE:**
        *   Use semantic HTML5.
        *   Wrap the entire output in a single `<section>...</section>` block.
        *   Do not include `<html>`, `<head>`, or `<body>` tags.
        *   Use Jinja2 comments `{{# ... #}}` for logic comments if needed.

    **Example content keys for context (do not hardcode them, infer logic based on the rules above):**
    ```json
    {json.dumps(example_content, indent=2)}
    ```
    """


def get_css_prompt(master_plan: dict, design_specs_str: str) -> str:
    # --- ！！！重大修改！！！ ---
    # 这个提示词现在接收设计规范，并强制AI使用它们
    theme_description = master_plan.get(
        "theme_description", "A modern, professional website."
    )
    section_types = {
        s.get("type") for s in master_plan.get("sections", []) if s.get("type")
    }
    # 生成 BEM 风格的类名给 AI 作为参考
    unique_section_classes = ", ".join([f".section-{st}" for st in section_types])
    example_child_classes = ", ".join(
        [f".section-{st}__heading" for st in section_types]
    )

    return f"""
    You are a professional web designer and CSS expert.
    Your task is to generate a complete, beautiful, and modern `style.css` file based on a theme description and a **strict set of design specifications**.

    **Theme Description**: "{theme_description}"

    **CRITICAL DESIGN SPECIFICATIONS (MUST BE FOLLOWED):**
    You MUST use the exact colors and fonts provided below. DO NOT invent your own.
    ```css
    {design_specs_str}
    ```

    **CRITICAL INSTRUCTIONS (MUST BE FOLLOWED):**

    1.  **USE THE PROVIDED SPECS:** You MUST use the CSS custom properties (e.g., `var(--color-primary)`) and `@import` the specified Google Fonts from the design specifications above.
    2.  **CLASS NAME MATCHING:** The HTML is built using BEM-style class names. Your CSS selectors MUST match this structure precisely.
        *   Style the main section containers, for example: `{unique_section_classes}`.
        *   Style the child elements within each section, for example: `{example_child_classes}`.
        *   **THIS IS THE MOST IMPORTANT RULE. Your CSS will not work if the class names do not match.**
    3.  **GENERATE COMPLETE CSS:** Include base styles for `body`, headings (`h1`, `h2`, etc.), paragraphs, and links.
    4.  **RESPONSIVE DESIGN:** MUST include `@media` queries for mobile devices (e.g., `@media (max-width: 768px)`).
    5.  **MODERN TECHNIQUES:** Use Flexbox or Grid for layout. Add subtle transitions for a premium feel.
    6.  **OUTPUT RAW CSS ONLY:** Do not include `<style>` tags, markdown formatting like ```css, or any explanations.
    """


def get_design_doc_prompt(master_plan: dict) -> str:
    # 这个提示词本身已经很好，无需修改
    master_plan_str = json.dumps(master_plan, indent=2, ensure_ascii=False)
    return f"""
    You are a senior web design consultant and technical writer.
    Based on the following JSON data representing a website plan, write a comprehensive and insightful design document in Markdown format.
    Go into great detail for each section, explaining the "why" behind design choices and how they align with the project's goals.

    The document must be structured with the following detailed sections:
    ## 1. Core Concept & Brand Story
    - **Strategic Core:** Elaborate on the core brand identity derived from the `theme_description`.
    - **Brand Narrative:** How will the website tell a story?
    - **Key Messaging:** What are the primary messages the website should convey?

    ## 2. Visual Design Language
    - **Overall Mood & Tone:** Describe the intended feeling.
    - **Color Palette Rationale:** Propose a specific color palette (with hex codes) and justify each choice. Use a list or code block for clarity.
    - **Typography Rationale:** Propose specific Google Fonts and explain why they are suitable. Use a list or code block for clarity.
    - **Imagery & Iconography Style:** Describe the style of photography, referencing `image_prompt` examples.

    ## 3. Site Architecture & User Experience (UX)
    - **Overall Structure:** Describe the page flow and navigation strategy.
    - **Detailed Section Analysis:** For EACH section in the JSON, provide a breakdown of its Purpose, Content Strategy, and UX/UI Considerations.

    Use the provided JSON data extensively to support your analysis. Be professional and detailed.

    **JSON Data:**
    ```json
    {master_plan_str}
    ```
    """


def get_fix_template_prompt(
    broken_html: str, error_message: str, section_type: str
) -> str:
    # 这个提示词本身已经很好，无需修改
    return f"""
    You are an expert Jinja2 and HTML template debugger. Your task is to fix a broken template file.

    **Context:**
    - The template is for a website section of type: `{section_type}`.
    - When trying to load this template, the rendering engine produced the following error: "{error_message}"

    **Broken Template Code:**
    ```html
    {broken_html}
    ```

    **Instructions:**
    1.  Analyze the error message and the broken code.
    2.  Identify the syntax error (e.g., mismatched tags, unclosed comments, incorrect loops).
    3.  Correct the error and provide the complete, valid Jinja2/HTML code for the entire section.
    4.  **CRITICAL: Do NOT add any explanations, apologies, or markdown formatting.** Only output the raw, corrected HTML code. Ensure all Jinja2 syntax (`{{% ... %}}`, `{{{{ ... }}}}`, `{{# ... #}}`) is perfectly valid.
    """
