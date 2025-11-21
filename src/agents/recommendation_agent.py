from typing import Dict, Any

from llm_client import GeminiClient
from observability.logger import get_logger


class RecommendationAgent:
    """
    Generates explanation & suggested review actions (non-prescriptive).
    """

    def __init__(self, client: GeminiClient):
        self.client = client
        self.logger = get_logger("RecommendationAgent")

    def run(self, summary: str, risk_result: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""
You are a clinical decision-support assistant.

Given:
- Summary: {summary}
- Priority: {risk_result.get('priority')}
- Reason: {risk_result.get('reason')}

Write:
1. A short explanation (2–3 sentences) of why this case may require attention.
2. 2–3 high-level review suggestions as bullet points.
   Examples of suggestions:
   - review lab trends
   - consider specialist consultation
   - check for missing information
   - schedule follow-up review

Important:
- Do NOT give explicit diagnoses or treatment instructions.
- Always keep the clinician in control of final decisions.
"""
        explanation = self.client.generate_text(prompt)
        self.logger.info("Generated explanation and suggestions.")
        return {"explanation": explanation}
