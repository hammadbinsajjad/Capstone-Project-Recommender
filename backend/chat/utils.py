from google import genai

from .constants import GEMINI_MODEL


def google_ai_response(prompt):
    return genai.Client().models.generate_content(model=GEMINI_MODEL, contents=prompt).text


def chat_title(user_query):
    prompt = (
        f"Generate a concise chat title for the following query: '{user_query}'"
        "Keep the title under 250 characters. Just give me the title without any additional text."
    )

    return google_ai_response(prompt).strip('" \r\n')[:256]
