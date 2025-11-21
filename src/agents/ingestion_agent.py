from typing import Dict, Optional

from memory.session_store import SessionStore
from observability.logger import get_logger


class IngestionAgent:
    """
    Cleans raw text and creates/updates a session.
    """

    def __init__(self, session_store: SessionStore):
        self.session_store = session_store
        self.logger = get_logger("IngestionAgent")

    def _clean_text(self, text: str) -> str:
        # Basic cleanup: collapse whitespace
        return " ".join(text.split())

    def run(self, report_text: str, patient_id: Optional[str] = None) -> Dict:
        cleaned = self._clean_text(report_text)
        session_id = self.session_store.start_or_update_session(patient_id, cleaned)
        self.logger.info(
            f"Ingested report for session={session_id}, patient_id={patient_id}"
        )
        return {
            "session_id": session_id,
            "cleaned_report": cleaned,
            "patient_id": patient_id,
        }
