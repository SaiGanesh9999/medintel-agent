from typing import Dict, Any

from observability.logger import get_logger


class LoggingAgent:
    """
    Thin wrapper for logging pipeline stages.
    """

    def __init__(self):
        self.logger = get_logger("LoggingAgent")

    def run(self, stage: str, payload: Dict[str, Any]) -> None:
        self.logger.info(f"[{stage}] payload={payload}")
