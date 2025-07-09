# ai_website_generator/builder.py

import os
import json
import re
import shutil
import sys
from jinja2 import Environment, FileSystemLoader, TemplateError

# Import AI functions from the new ai sub-package
from . import ai as ai_engine


def mock_generate_image_url(prompt, size):
    """Simulates image generation, returns a placeholder URL."""
    try:
        width, height = 1024, 768
        size_str = str(size).lower().strip()
        if "large" in size_str or "widescreen" in size_str:
            width, height = 1920, 1080
        elif "medium" in size_str or "portrait" in size_str:
            width, height = 1080, 1350
        elif "square" in size_str:
            width, height = 1080, 1080
    except Exception:
        width, height = 1024, 768

    text = re.sub(r"[^a-zA-Z0-9 ]", "", str(prompt))[:40].replace(" ", "+")
    return f"https://via.placeholder.com/{int(width)}x{int(height)}.png?text={text}"


class WebsiteGenerator:
    def __init__(self, output_dir="output_website"):
        self.output_dir = output_dir
        if os.path.exists(self.output_dir):
            print(
                f"[BUILDER] 🗑️  Deleting existing output directory '{self.output_dir}'."
            )
            shutil.rmtree(self.output_dir)

        self.website_dir = os.path.join(self.output_dir, "website")
        self.images_dir = os.path.join(self.website_dir, "images")
        os.makedirs(self.images_dir, exist_ok=True)
        os.makedirs(os.path.join(self.website_dir, "css"), exist_ok=True)
        print(
            f"[BUILDER] ✅ Created clean output directory structure at '{self.output_dir}'."
        )

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.templates_dir = os.path.join(current_dir, "templates")
        self.env = None  # Will be initialized later

    def _render_component(self, section_data):
        section_type = section_data.get("type")
        if not section_type:
            return "<!-- Section data is missing a 'type' key. -->"

        template_name = f"{section_type}.html"
        template_path = os.path.join(self.templates_dir, template_name)
        if not os.path.exists(template_path):
            return f"<!-- Template '{template_name}' not found. -->"

        max_retries = 1
        for attempt in range(max_retries + 1):
            try:
                if not self.env:
                    self.env = Environment(loader=FileSystemLoader(self.templates_dir))
                template = self.env.get_template(template_name)
                content = section_data.get("content", {})
                if not isinstance(content, dict):
                    return f"<!-- Content for '{section_type}' is not a valid dictionary. -->"

                def process_images_recursively(data_struct):
                    if isinstance(data_struct, dict):
                        if (
                            "image_prompt" in data_struct
                            and "image_size" in data_struct
                        ):
                            data_struct["image_url"] = mock_generate_image_url(
                                data_struct["image_prompt"], data_struct["image_size"]
                            )
                        for key, value in data_struct.items():
                            data_struct[key] = process_images_recursively(value)
                    elif isinstance(data_struct, list):
                        return [
                            process_images_recursively(item) for item in data_struct
                        ]
                    return data_struct

                render_data = process_images_recursively(content)
                return template.render(**render_data)

            except TemplateError as e:
                print(
                    f"[BUILDER] ⚠️  Attempt {attempt + 1}: Failed to load/render '{template_name}'. Error: {e}"
                )

                if attempt >= max_retries:
                    print(
                        f"[BUILDER] ❌ Giving up on '{template_name}' after {max_retries + 1} attempts."
                    )
                    return f"<!-- ERROR: Failed to render {section_type} template after fix attempt: {e} -->"

                print(f"[BUILDER] 🛠️  Invoking AI-Fixer for '{template_name}'...")
                try:
                    with open(template_path, "r", encoding="utf-8") as f:
                        broken_html = f.read()

                    corrected_html = ai_engine.ai_fix_template(
                        broken_html, str(e), section_type
                    )

                    if corrected_html:
                        with open(template_path, "w", encoding="utf-8") as f:
                            f.write(corrected_html)

                        print(
                            "[BUILDER] 🔄  Reloading template environment after fix..."
                        )
                        self.env = Environment(
                            loader=FileSystemLoader(self.templates_dir)
                        )
                        continue
                    else:
                        return f"<!-- ERROR: AI-Fixer failed to correct {section_type} template. -->"
                except Exception as fix_error:
                    print(
                        f"[BUILDER] ❌ Unhandled error during AI-Fixer invocation: {fix_error}"
                    )
                    return f"<!-- ERROR: AI-Fixer process failed for {section_type}. Check logs. -->"

        return f"<!-- UNEXPECTED RENDER ERROR for {section_type} -->"

    def _extract_design_specs(self, design_doc_md):
        """Extracts color palette and typography from the design document markdown."""
        print("[BUILDER] 🔍 Extracting design specs from design_document.md...")
        specs = []
        try:
            # Extract Colors
            color_section = re.search(
                r"## 2\..*?Color Palette Rationale.*?(## 3\.|$)",
                design_doc_md,
                re.DOTALL | re.IGNORECASE,
            )
            if color_section:
                specs.append("/* --- Color Palette (from Design Doc) --- */")
                specs.append(":root {")
                # Find hex codes like #FFFFFF or #FFF
                hex_codes = re.findall(
                    r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})", color_section.group(0)
                )
                color_names = [
                    "primary",
                    "secondary",
                    "accent",
                    "background",
                    "text",
                    "surface",
                ]
                for i, code in enumerate(hex_codes):
                    name_index = i % len(color_names)
                    if i < len(color_names):
                        specs.append(f"    --color-{color_names[i]}: #{code};")
                    else:
                        specs.append(
                            f"    --color-accent-{i - len(color_names) + 1}: #{code};"
                        )
                specs.append("}\n")

            # Extract Fonts
            font_section = re.search(
                r"## 2\..*?Typography Rationale.*?(## 3\.|$)",
                design_doc_md,
                re.DOTALL | re.IGNORECASE,
            )
            if font_section:
                # Find fonts mentioned in backticks like `Poppins`
                fonts = re.findall(r"[`']([^`']+)['`]", font_section.group(0))
                # Filter for common font patterns (e.g., more than 3 chars, contains letters)
                google_fonts = [
                    f.strip()
                    for f in fonts
                    if len(f) > 3
                    and re.search("[a-zA-Z]", f)
                    and "sans" not in f.lower()
                    and "serif" not in f.lower()
                ]
                if google_fonts:
                    unique_fonts = sorted(
                        list(set(google_fonts)), key=len, reverse=True
                    )
                    font_url_part = "&family=".join(
                        [
                            f.replace(" ", "+") + ":wght@400;600;700"
                            for f in unique_fonts
                        ]
                    )
                    specs.insert(
                        0,
                        f"@import url('https://fonts.googleapis.com/css2?family={font_url_part}&display=swap');\n",
                    )
                    if len(unique_fonts) > 0:
                        specs.append(
                            f":root {{\n    --font-heading: '{unique_fonts[0]}', sans-serif;"
                        )
                    if len(unique_fonts) > 1:
                        specs.append(
                            f"    --font-body: '{unique_fonts[1]}', sans-serif;"
                        )
                    else:  # Fallback if only one font is found
                        specs.append(
                            f"    --font-body: '{unique_fonts[0]}', sans-serif;"
                        )
                    specs.append("}\n")

            print("[BUILDER] ✅ Design specs extracted successfully.")
            return "\n".join(specs)
        except Exception as e:
            print(f"[BUILDER] ⚠️  Could not extract design specs: {e}")
            return "/* Could not automatically extract design specs. */"

    def generate(self, user_prompt):
        # --- ！！！重大修改！！！ ---
        # 调整了整个生成流程的顺序
        # 1. 生成 Master Plan
        master_plan = ai_engine.ai_generate_master_plan(user_prompt)
        if not master_plan:
            print("\n[FATAL] Unable to generate master design plan, process aborted.")
            return

        with open(
            os.path.join(self.output_dir, "master_plan.json"), "w", encoding="utf-8"
        ) as f:
            json.dump(master_plan, f, indent=4, ensure_ascii=False)
        print("[BUILDER] ✅ master_plan.json saved for debugging.")

        # 2. 基于 Master Plan 生成设计文档
        design_doc_md = ai_engine.ai_write_design_doc(master_plan)
        with open(
            os.path.join(self.output_dir, "design_document.md"), "w", encoding="utf-8"
        ) as f:
            f.write(design_doc_md or "# Failed to generate design document.")
        print(f"[BUILDER] ✅ design_document.md generated.")

        # 3. 从设计文档中提取颜色和字体规范
        design_specs_str = self._extract_design_specs(design_doc_md)

        # 4. 基于 Master Plan 和提取的规范生成 CSS
        generated_css = ai_engine.ai_generate_css(master_plan, design_specs_str)
        with open(
            os.path.join(self.website_dir, "css", "style.css"), "w", encoding="utf-8"
        ) as f:
            f.write(generated_css)
        print(f"[BUILDER] ✅ AI-generated style.css saved.")

        # 5. 生成所有需要的 HTML 模板
        print("\n[BUILDER] 🔍 Regenerating all required templates...")
        if os.path.exists(self.templates_dir):
            shutil.rmtree(self.templates_dir)
        os.makedirs(self.templates_dir)
        print("[BUILDER] 🗑️  Cleared old templates.")

        required_section_types = {
            s.get("type") for s in master_plan.get("sections", []) if s.get("type")
        }
        for section_type in required_section_types:
            example_content = next(
                (
                    s.get("content")
                    for s in master_plan["sections"]
                    if s.get("type") == section_type
                ),
                None,
            )
            generated_html = ai_engine.ai_generate_template(
                section_type, example_content
            )
            if generated_html:
                with open(
                    os.path.join(self.templates_dir, f"{section_type}.html"),
                    "w",
                    encoding="utf-8",
                ) as f:
                    f.write(generated_html)

        self.env = Environment(loader=FileSystemLoader(self.templates_dir))
        print("[BUILDER] 🔄  Reloaded template environment.")

        # 6. 组装网站
        print("\n[BUILDER] ⚙️  Assembling website...")
        all_sections_html = ""
        for section in master_plan.get("sections", []):
            all_sections_html += self._render_component(section) + "\n"

        base_html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ site_title or 'AI Generated Website' }}</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    {{ website_content|safe }}
</body>
</html>"""
        with open(
            os.path.join(self.templates_dir, "base.html"), "w", encoding="utf-8"
        ) as f:
            f.write(base_html_content)

        base_template = self.env.get_template("base.html")
        final_html = base_template.render(
            site_title=master_plan.get("site_title", "AI Generated Website"),
            website_content=all_sections_html,
        )

        with open(
            os.path.join(self.website_dir, "index.html"), "w", encoding="utf-8"
        ) as f:
            f.write(final_html)
        print(f"[BUILDER] ✅ index.html generated.")

        print(
            f"\n[SUCCESS] 🚀 Website generation complete! Check the '{self.output_dir}' folder."
        )
