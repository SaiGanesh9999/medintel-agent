from typing import Dict, Any
import json
import google.generativeai as genai

from config import GEMINI_API_KEY, GEMINI_MODEL_NAME


class GeminiClient:
    """
    Thin wrapper over google-generativeai.
    """

    def __init__(self, model_name: str = GEMINI_MODEL_NAME):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(model_name)

    def generate_text(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return (response.text or "").strip()

    def generate_json(self, prompt: str, schema_hint: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ask the model to return a JSON object. Very simple parsing.
        In production you would want stricter validation.
        """
        system_instructions = (
            "Return ONLY a valid JSON object. "
            "Do not include backticks, markdown, or any explanation.\n"
        )

        full_prompt = system_instructions + "\n" + prompt
        response = self.model.generate_content(full_prompt)
        text = (response.text or "").strip()

        # Try to locate JSON object
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Fallback: attempt to extract JSON between first { and last }
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1 and end > start:
                snippet = text[start : end + 1]
                return json.loads(snippet)
            # If it still fails, return a default-safe structure
            return {
                "priority": "Medium",
                "reason": "JSON parsing failed, defaulting to Medium.",
                "tags": ["parse_error"],
            }
