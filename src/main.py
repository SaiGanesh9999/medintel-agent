import argparse

from llm_client import GeminiClient
from memory.session_store import SessionStore
from memory.memory_bank import MemoryBank
from tools.lab_reference_tool import LabReferenceTool
from tools.ehr_mock_api_tool import EHRMockApiTool
from agents.ingestion_agent import IngestionAgent
from agents.summary_agent import SummaryAgent
from agents.risk_agent import RiskAgent
from agents.recommendation_agent import RecommendationAgent
from agents.logging_agent import LoggingAgent
from observability.metrics import Metrics
from observability.logger import get_logger


def main():
    parser = argparse.ArgumentParser(description="MedIntel Agent - Medical Report Triage")
    parser.add_argument(
        "--input",
        required=True,
        help="Path to input medical report text file",
    )
    parser.add_argument(
        "--patient_id",
        required=False,
        help="Optional patient ID (for session & memory)",
    )
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        report_text = f.read()

    logger = get_logger("Main")
    metrics = Metrics()

    # Shared components
    session_store = SessionStore()
    memory_bank = MemoryBank()
    lab_tool = LabReferenceTool()
    ehr_tool = EHRMockApiTool()  # not heavily used yet, but present as a tool
    client = GeminiClient()

    ingestion_agent = IngestionAgent(session_store)
    summary_agent = SummaryAgent(client)
    risk_agent = RiskAgent(client, lab_tool)
    recommendation_agent = RecommendationAgent(client)
    logging_agent = LoggingAgent()

    with metrics.time_block("total_pipeline"):
        ingest_out = ingestion_agent.run(report_text, args.patient_id)
        logging_agent.run("ingestion", {"session_id": ingest_out["session_id"]})

        summary_out = summary_agent.run(ingest_out["cleaned_report"])
        logging_agent.run("summary", {"summary": summary_out["summary"]})

        risk_out = risk_agent.run(
            ingest_out["cleaned_report"],
            summary_out["summary"],
        )
        logging_agent.run("risk", risk_out)

        rec_out = recommendation_agent.run(
            summary_out["summary"],
            risk_out,
        )
        logging_agent.run("recommendation", rec_out)

        # Save into long-term memory
        memory_bank.add_entry(
            ingest_out["patient_id"],
            {
                "summary": summary_out["summary"],
                "priority": risk_out.get("priority"),
                "reason": risk_out.get("reason"),
                "tags": risk_out.get("tags", []),
            },
        )

    logger.info("=== MEDINTEL OUTPUT ===")
    print("\n--- MEDINTEL REPORT ---\n")
    print("SUMMARY:\n", summary_out["summary"], "\n")
    print("PRIORITY:", risk_out.get("priority"))
    print("REASON:\n", risk_out.get("reason"), "\n")
    print("TAGS:", ", ".join(risk_out.get("tags", [])))
    print("\nEXPLANATION & SUGGESTIONS:\n", rec_out["explanation"])


if __name__ == "__main__":
    main()
