# ai_website_generator/config.py

import os
import sys
import google.generativeai as genai


def configure_api():
    """
    Reads the API Key from environment variables or Colab Secrets and configures the genai library.
    """
    try:
        # Read API Key
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not GOOGLE_API_KEY and "google.colab" in sys.modules:
            try:
                from google.colab import userdata

                GOOGLE_API_KEY = userdata.get("GOOGLE_API_KEY") or userdata.get(
                    "GEMINI_API_KEY"
                )
            except ImportError:
                pass  # Not in Colab

        if not GOOGLE_API_KEY:
            raise ValueError(
                "Error: GOOGLE_API_KEY or GEMINI_API_KEY not found in environment or Colab Secrets."
            )

        # Configure genai library
        genai.configure(api_key=GOOGLE_API_KEY)
        print("[CONFIG] ⚙️  API Key configured successfully.")
        return True

    except Exception as e:
        print(f"[CONFIG] ❌ API Configuration Error: {e}")
        return False


# Define model names to be used across the application
MODEL_NAME_PRO = "gemini-2.5-flash-preview-04-17"
MODEL_NAME_FLASH = os.getenv("FLASH_MODEL", "gemini-2.5-flash-preview-04-17")
