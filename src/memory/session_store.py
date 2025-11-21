from typing import Dict, Any
import uuid


class SessionStore:
    """
    Simple in-memory session store.
    Maps session_id -> { patient_id, reports: [...] }.
    """

    def __init__(self):
        self._sessions: Dict[str, Dict[str, Any]] = {}

    def start_or_update_session(self, patient_id: str | None, report_text: str) -> str:
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = {
            "patient_id": patient_id,
            "reports": [report_text],
        }
        return session_id

    def get_session(self, session_id: str) -> Dict[str, Any] | None:
        return self._sessions.get(session_id)
