from typing import Dict, List


class EHRMockApiTool:
    """
    Mock EHR-style tool storing previous reports per patient_id.
    Used to demonstrate how an external tool could be integrated.
    """

    def __init__(self):
        self._data: Dict[str, List[str]] = {}

    def add_report(self, patient_id: str, report_text: str) -> None:
        self._data.setdefault(patient_id, []).append(report_text)

    def get_reports(self, patient_id: str) -> List[str]:
        return self._data.get(patient_id, [])
