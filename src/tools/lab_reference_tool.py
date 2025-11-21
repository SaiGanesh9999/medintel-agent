from typing import Dict, Any, List
import re


class LabReferenceTool:
    """
    Very simple, fake lab reference checker.
    Only for demo. NOT for real clinical use.
    """

    def __init__(self):
        # Fake reference ranges (not accurate medically)
        self.ranges = {
            "hemoglobin": (12.0, 16.0),
            "creatinine": (0.6, 1.3),
        }

    def check_report(self, report_text: str) -> List[Dict[str, Any]]:
        text = report_text.lower()
        flags: List[Dict[str, Any]] = []

        for analyte, (low, high) in self.ranges.items():
            pattern = rf"{analyte}\s+(\d+(\.\d+)?)"
            match = re.search(pattern, text)
            if not match:
                continue

            value = float(match.group(1))
            status = "normal"
            if value < low:
                status = "low"
            elif value > high:
                status = "high"

            flags.append(
                {
                    "analyte": analyte,
                    "value": value,
                    "status": status,
                    "range": [low, high],
                }
            )

        return flags
