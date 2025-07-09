# ai_website_generator/ai/core.py

import google.generativeai as genai
import re


def _clean_response_text(text):
    """Strips markdown code blocks from a string if they exist."""
    if text.startswith("```"):
        # Find the first newline and slice from there
        text = text[text.find("\n") + 1 :]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()


def generate_content(
    model_name: str, prompt: str, response_mime_type: str = None, timeout: int = 120
):
    """
    A robust wrapper for calling the Gemini API.

    Args:
        model_name: The name of the model to use.
        prompt: The prompt to send to the model.
        response_mime_type: The expected MIME type of the response (e.g., "application/json").
        timeout: The request timeout in seconds.

    Returns:
        The cleaned response text from the AI, or None if an error occurs.
    """
    print(f"[AI CORE]    > Calling model: {model_name} (timeout: {timeout}s)")
    try:
        generation_config = (
            {"response_mime_type": response_mime_type} if response_mime_type else None
        )

        model = genai.GenerativeModel(model_name, generation_config=generation_config)

        response = model.generate_content(prompt, request_options={"timeout": timeout})
        response_text = getattr(response, "text", None)

        if not response_text or not response_text.strip():
            raise ValueError("AI returned an empty response.")

        cleaned_text = _clean_response_text(response_text)
        print(f"[AI CORE]    > Response received and cleaned successfully.")
        return cleaned_text

    except Exception as e:
        print(f"[AI CORE] ❌ ERROR: Failed to generate content.")
        print(f"[AI CORE]    > Error Type: {type(e).__name__}")
        print(f"[AI CORE]    > Error Details: {e}")
        # In case of error, print raw response if available
        if "response" in locals() and hasattr(response, "text"):
            print(f"[AI CORE]    > Raw Response Text: {response.text}")
        return None
