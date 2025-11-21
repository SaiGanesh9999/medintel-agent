from typing import Dict, List, Any


class MemoryBank:
    """
    Long-term memory per patient_id.
    Stores previous summaries / risk assessments.
    """

    def __init__(self):
        self._store: Dict[str, List[Dict[str, Any]]] = {}

    def add_entry(self, patient_id: str | None, entry: Dict[str, Any]) -> None:
        if not patient_id:
            return
        self._store.setdefault(patient_id, []).append(entry)

    def get_history(self, patient_id: str | None) -> List[Dict[str, Any]]:
        if not patient_id:
            return []
        return self._store.get(patient_id, [])
