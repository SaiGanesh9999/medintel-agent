from typing import Dict

from llm_client import GeminiClient
from observability.logger import get_logger


class SummaryAgent:
    """
    Uses Gemini to generate a concise, non-diagnostic summary.
    """

    def __init__(self, client: GeminiClient):
        self.client = client
        self.logger = get_logger("SummaryAgent")

    def run(self, cleaned_report: str) -> Dict:
        prompt = f"""
You are a clinical decision-support assistant.

Summarize the following medical report in 3–5 bullet points.
Use neutral, cautious language. Do NOT make a definitive diagnosis.
Always mention that a qualified clinician must review these findings.

Report:
{cleaned_report}
"""
        summary = self.client.generate_text(prompt)
        self.logger.info("Generated summary for report.")
        return {"summary": summary}
