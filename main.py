# ai_website_generator/main.py

import sys
from .config import configure_api
from .builder import WebsiteGenerator


def main():
    # 1. Configure the API
    if not configure_api():
        sys.exit(1)  # Exit if API configuration fails

    # 2. Get user input
    user_prompt = "我要一个kpop模特展示网站"
    print(f"\n[MAIN] 🚀 Starting website generation for prompt: '{user_prompt}'")

    # 3. Create a generator instance
    generator = WebsiteGenerator()

    # 4. Execute the generation process
    generator.generate(user_prompt)


if __name__ == "__main__":
    main()
