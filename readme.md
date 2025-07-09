# AI Website Generator

The **AI Website Generator** is an advanced, AI-driven tool that automates the creation of a complete website prototype from a single text prompt (e.g., "I want a website for a K-Pop model agency").

This project simulates the entire workflow of a professional web development team, moving from strategic planning and visual design to front-end coding. It features a unique, AI-powered self-correction mechanism to ensure a reliable and high-quality final output.

## ✨ Key Features

*   **End-to-End Automation**: Transforms a simple idea into a complete website, including HTML, CSS, and planning documents, with a single command.
*   **Deep AI Integration**: Leverages Google Gemini models (both Flash and Pro versions) for multi-stage intelligent creation, including content strategy, UI/UX design, code generation, and error correction.
*   **Professional-Grade Deliverables**: The output goes beyond just code, providing a full project suite:
    *   **Master Plan (`master_plan.json`)**: A JSON blueprint detailing the website's structure, content, and thematic direction.
    *   **Design Document (`design_document.md`)**: A comprehensive and professional design document that articulates the brand story, visual language (colors, typography), and UX strategy.
*   **Design Consistency**: Implements an innovative "Plan-Driven-Coding" process. The system first generates a design document, extracts specific design rules (like colors and fonts), and then enforces these rules upon the CSS generation AI, ensuring a high degree of visual consistency.
*   **Robust Self-Correction**: Features a built-in "AI Fixer" layer. If the AI makes a syntax error while generating Jinja2 templates, the system automatically detects the issue, diagnoses it, and invokes another AI to fix the faulty code, dramatically increasing end-to-end success rates.
*   **BEM Convention**: Enforces the BEM (Block, Element, Modifier) naming convention for both HTML and CSS generation, resulting in clean, structured, and maintainable code.

## 🚀 The Workflow

The project automates a professional team's workflow through the following sequential steps:

1.  **🧠 Planning**
    *   **Input**: A simple, one-sentence description of the desired website from the user.
    *   **AI Task**: The `ai_generate_master_plan` function is called. The AI, acting as a "Website Strategist," generates a JSON file (`master_plan.json`) that outlines the site title, theme description, and detailed content for every section of the website.

2.  **✍️ Designing**
    *   **AI Task**: The `ai_write_design_doc` function is called. The AI, acting as a "Senior Web Design Consultant," uses `master_plan.json` as a brief to write a professional design document in Markdown (`design_document.md`). This document details the brand narrative, visual language (proposing specific colors and fonts), and user experience analysis.

3.  **🎨 Coding - CSS**
    *   **Specification Extraction**: The `_extract_design_specs` function parses the `design_document.md` using regular expressions to extract the AI-proposed color palette (HEX codes) and Google Fonts.
    *   **AI Task**: The `ai_generate_css` function is called. The AI, acting as a "CSS Expert," receives the theme description from the `master_plan` and the **strict design specifications extracted from the design document**. It then generates a responsive `style.css` file that adheres to the BEM convention and the specified visual guidelines.

4.  **🏗️ Coding - HTML Templates**
    *   **AI Task**: For each section defined in the `master_plan`, the `ai_generate_template` function is called. The AI, acting as a "Jinja2 & HTML Specialist," follows a strict set of instructions (including BEM class naming and rules for handling images and lists) to generate a corresponding HTML template (e.g., `hero_section.html`).

5.  **🧩 Assembly & Self-Correction**
    *   **Rendering**: The `_render_component` method iterates through all sections, using the Jinja2 engine to render the data from `master_plan.json` into the corresponding HTML templates.
    *   **Self-Correction**: If a Jinja2 syntax error is encountered during rendering (e.g., an unclosed tag), the exception is caught. The `ai_fix_template` function is immediately invoked. The AI, acting as a "Code Debugger," receives the broken code and the error message, then provides a corrected version. The fixed template overwrites the faulty one, and the rendering process continues.
    *   **Integration**: All rendered HTML snippets are combined and injected into a base HTML skeleton, producing the final `index.html`.

## 📁 Project Structure

```
ai_website_generator/
├── ai/                      # Core AI logic sub-package
│   ├── __init__.py          # Exports public AI functions
│   ├── core.py              # Wraps core calls to the Gemini API
│   ├── generator.py         # Contains the main AI generation functions (planning, coding)
│   └── prompts.py           # Centralized management for all AI prompts
├── templates/               # Directory for dynamically generated Jinja2 templates
├── __init__.py
├── builder.py               # The website builder, orchestrates the entire workflow
├── config.py                # API key configuration and model constants
├── main.py                  # Project entry point
└── ...
```

## 🛠️ How to Run

### 1. Setup Your Environment

*   Ensure you have Python 3.9 or newer installed.
*   Install all required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: Your `requirements.txt` file should include libraries like `google-generativeai` and `Jinja2`.*

### 2. Configure Your API Key

You will need a Google Gemini API key. Configure it using one of the following methods:

*   **Environment Variable**:
    ```bash
    export GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```
*   **`.env` File**: (Requires `python-dotenv` library)
    Create a `.env` file in the project's root directory and add:
    ```
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```
*   **Google Colab**: If running in Colab, use the "Secrets" tab in the left sidebar to store your `GOOGLE_API_KEY`.

### 3. Run the Project

Modify the `user_prompt` variable in the `main.py` file to define your desired website theme:

```python
# ai_website_generator/main.py

def main():
    # ...
    # 2. Get user input
    user_prompt = "Create a futuristic website about space exploration" # <-- Change this line
    print(f"\n[MAIN] 🚀 Starting website generation for prompt: '{user_prompt}'")
    # ...
```

Then, run the `main.py` module from the project's root directory:

```bash
python -m ai_website_generator.main
```

### 4. Check the Output

Once the script finishes, all generated files will be available in the `output_website/` directory:

*   `output_website/master_plan.json`
*   `output_website/design_document.md`
*   `output_website/website/`
    *   `index.html`
    *   `css/style.css`
    *   `images/` (for future implementation of image downloading)

Open `output_website/website/index.html` in your web browser to preview the generated site.

## 🔮 Future Enhancements

*   **Real Image Generation**: Replace `mock_generate_image_url` with actual API calls to a text-to-image model (like DALL-E, Midjourney, or Imagen) and download the generated images locally.
*   **Multi-Page Support**: Extend the `master_plan` structure to support the generation of multiple HTML pages (e.g., `/about`, `/contact`) and automatically handle the linking between them.
*   **Enhanced Interactivity**: Introduce JavaScript generation capabilities to add interactive elements like hamburger menus for navigation, form validation, and dynamic on-scroll effects.
*   **Component Library**: Save high-quality, successfully generated templates for common section types (e.g., `hero`, `footer`) into a reusable component library. This would allow the system to skip AI generation in some cases and use proven, pre-built components for faster and more reliable results.

---