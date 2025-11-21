from typing import Dict, Any

from llm_client import GeminiClient
from tools.lab_reference_tool import LabReferenceTool
from observability.logger import get_logger


class RiskAgent:
    """
    Classifies priority: Low / Medium / High,
    using LLM reasoning + lab reference flags.
    """

    def __init__(self, client: GeminiClient, lab_tool: LabReferenceTool):
        self.client = client
        self.lab_tool = lab_tool
        self.logger = get_logger("RiskAgent")

    def run(self, cleaned_report: str, summary: str) -> Dict[str, Any]:
        lab_flags = self.lab_tool.check_report(cleaned_report)

        schema_hint = {
            "priority": "Low | Medium | High",
            "reason": "string explanation",
            "tags": ["string tags like follow_up_recommended, critical_values_present"],
        }

        prompt = f"""
You are triaging medical reports for clinician review.

Task:
- Assign a PRIORITY: one of "Low", "Medium", or "High".
- Explain briefly WHY you chose that priority.
- Add TAGS like: "follow_up_recommended", "critical_values_present", "routine", etc.

Rules:
- Always assume a clinician will review the case.
- Do NOT give any definitive diagnosis or treatment.
- Be conservative and safe.

Return a JSON object with keys: priority, reason, tags.

Report:
{cleaned_report}

Summary:
{summary}

Lab flags (from reference ranges):
{lab_flags}
"""

        result = self.client.generate_json(prompt, schema_hint)
        priority = result.get("priority", "Medium")
        self.logger.info(f"Assigned priority={priority}")
        return result
