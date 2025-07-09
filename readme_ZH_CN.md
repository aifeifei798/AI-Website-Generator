# AI Website Generator

**AI Website Generator** 是一个先进的、基于生成式AI的自动化工具，能够将用户的单一文本提示（例如“我想要一个关于K-Pop模特的网站”）转化为一个功能齐全、设计统一、包含完整规划文档的网站原型。

这个项目不仅仅是一个简单的代码生成器，它模拟了一个专业Web开发团队的完整工作流程：从战略规划、视觉设计到前端编码，并内置了AI驱动的自我修复能力，以确保最终交付的可靠性。

## ✨ 项目亮点

*   **端到端自动化**: 从一个简单的想法到包含HTML, CSS和设计文档的完整网站，整个过程完全自动化。
*   **深度AI集成**: 利用Google Gemini模型（包括Flash和Pro版本）进行多阶段的智能创作，包括内容规划、UI/UX设计、代码生成和错误修复。
*   **专业级输出**: 生成的不仅仅是代码，还包括：
    *   **总体规划 (`master_plan.json`)**: 网站的结构、内容和主题的JSON蓝图。
    *   **设计文档 (`design_document.md`)**: 一份详尽的专业设计文档，阐述了品牌故事、视觉语言（颜色、字体）和用户体验策略。
*   **设计一致性**: 独创的“规划驱动编码”流程。系统会先生成设计文档，然后从中提取出颜色、字体等具体设计规范，再强制后续的CSS生成AI遵循这些规范，确保视觉风格的高度统一。
*   **强大的自我修复能力**: 内置“AI修正层”（AI-Fixer）。当AI在生成Jinja2模板时产生语法错误，系统能自动捕获、诊断，并调用另一个AI来修复错误的代码，极大地提高了端到端的成功率。
*   **BEM规范**: 强制要求HTML和CSS生成遵循BEM（Block, Element, Modifier）命名约定，使得代码结构清晰，样式易于维护。

## 🚀 工作流程

该项目模拟了一个专业团队的工作流，分为以下几个自动化步骤：

1.  **🧠 规划 (Planning)**
    *   **输入**: 用户提供的一句简单的网站描述。
    *   **AI任务**: `ai_generate_master_plan` 函数被调用。AI扮演“网站策略师”的角色，生成一个包含网站标题、主题描述和所有页面版块（sections）详细内容的JSON文件 (`master_plan.json`)。

2.  **✍️ 设计 (Designing)**
    *   **AI任务**: `ai_write_design_doc` 函数被调用。AI扮演“高级网页设计顾问”的角色，基于`master_plan.json`，撰写一份专业的Markdown格式设计文档 (`design_document.md`)。文档详细阐述了品牌故事、视觉设计语言（并提出具体的颜色和字体建议）以及用户体验分析。

3.  **🎨 编码 - CSS (Coding - CSS)**
    *   **提取规范**: `_extract_design_specs` 函数通过正则表达式解析`design_document.md`，提取出AI建议的颜色（HEX码）和Google字体。
    *   **AI任务**: `ai_generate_css` 函数被调用。AI扮演“CSS专家”的角色，它接收到`master_plan`的主题描述和**从设计文档中提取出的严格设计规范**，然后生成一份遵循BEM命名法、响应式且风格统一的`style.css`文件。

4.  **🏗️ 编码 - HTML模板 (Coding - HTML Templates)**
    *   **AI任务**: `ai_generate_template` 函数被为`master_plan.json`中的每一个版块调用。AI扮演“Jinja2和HTML专家”的角色，根据严格的指令（包括BEM类名、图片和列表的处理方式）为每个版块生成一个HTML模板文件（如 `hero_section.html`）。

5.  **🧩 组装与修复 (Assembly & Self-Correction)**
    *   **渲染**: `_render_component` 方法开始遍历所有版块，使用Jinja2引擎将`master_plan.json`中的数据渲染到对应的HTML模板中。
    *   **自我修复**: 如果在渲染过程中遇到Jinja2模板语法错误（例如，AI生成了一个未闭合的标签），异常会被捕获。`ai_fix_template` 函数会被立即调用，AI扮演“代码调试器”的角色，接收错误代码和错误信息，并提供修复后的代码。修复后的模板会覆盖旧文件，然后系统继续渲染。
    *   **整合**: 所有渲染好的HTML片段被组合起来，嵌入到一个基础的HTML骨架中，最终生成`index.html`。

## 📁 项目结构

```
ai_website_generator/
├── ai/                      # AI核心逻辑子包
│   ├── __init__.py          # 导出公共AI函数
│   ├── core.py              # 封装对Gemini API的核心调用
│   ├── generator.py         # 包含主要的AI生成函数 (planning, coding)
│   ├── prompts.py           # 集中管理所有的AI提示词
│   └── fixer.py             # (可选) 可将修复逻辑移到此处
├── templates/               # AI动态生成的Jinja2模板存放处
├── __init__.py
├── builder.py               # 网站构建器，负责编排整个生成流程
├── config.py                # API密钥配置和模型常量
├── main.py                  # 项目入口
└── ...
```

## 🛠️ 如何运行

### 1. 准备环境

*   确保你已安装 Python 3.9 或更高版本。
*   安装所有依赖项：
    ```bash
    pip install -r requirements.txt
    ```
    *注：`requirements.txt` 文件应包含 `google-generativeai`, `Jinja2`等库。*

### 2. 配置API密钥

你需要一个Google Gemini API密钥。可以通过以下方式之一进行配置：

*   **环境变量**:
    ```bash
    export GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```
*   **`.env` 文件**: (需要 `python-dotenv` 库)
    在项目根目录创建一个 `.env` 文件，并添加：
    ```
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```
*   **Google Colab**: 如果在Colab中运行，请使用左侧边栏的“Secrets”功能来存储你的`GOOGLE_API_KEY`。

### 3. 运行项目

修改 `main.py` 文件中的 `user_prompt` 变量为你想要的网站主题：

```python
# ai_website_generator/main.py

def main():
    # ...
    # 2. Get user input
    user_prompt = "创建一个关于太空探索的未来主义风格网站" # <-- 修改这里
    print(f"\n[MAIN] 🚀 Starting website generation for prompt: '{user_prompt}'")
    # ...
```

然后，从项目根目录运行 `main.py`：

```bash
python -m ai_website_generator.main
```

### 4. 查看结果

脚本运行完成后，所有的输出文件都将位于 `output_website/` 目录下：

*   `output_website/master_plan.json`
*   `output_website/design_document.md`
*   `output_website/website/`
    *   `index.html`
    *   `css/style.css`
    *   `images/` (如果未来实现图片下载功能)

直接在浏览器中打开 `output_website/website/index.html` 即可预览生成的网站。

## 🔮 未来展望

*   **真实图片生成**: 将`mock_generate_image_url`替换为调用真实文生图模型（如DALL-E, Midjourney, Imagen）的API，并将生成的图片下载到本地。
*   **多页面支持**: 扩展`master_plan`的结构，以支持生成多个HTML页面（如 `/about`, `/contact`），并自动处理页面间的链接。
*   **交互性增强**: 引入JavaScript生成能力，为网站添加交互元素，如导航菜单的汉堡包按钮、表单验证、动态效果等。
*   **组件库**: 将常见的section类型（如 `hero`, `footer`）的优秀模板保存起来，形成一个可复用的组件库，在某些情况下可以跳过AI生成，直接使用高质量的预制模板。

---