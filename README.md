# MedIntel Agent: Enterprise AI for Medical Report Triage

**Track:** Enterprise Agents  
**Competition:** 5-Day AI Agents Intensive – Capstone

MedIntel Agent is a multi-agent system that analyzes medical reports, generates concise summaries, classifies risk level (Low / Medium / High), and explains why a case may need clinician attention. It is designed as a **clinical decision-support helper**, not a diagnostic system.

> ⚠️ **Disclaimer:** This project is for educational purposes only.  
> It uses synthetic data and is **not** a medical device or a production system.  
> All outputs must be reviewed by qualified healthcare professionals.

---

## 1. Features

- Multi-agent architecture:
  - Ingestion Agent  
  - Summary Agent (Gemini)  
  - Risk Classification Agent (Gemini + simple rules)  
  - Recommendation Agent (Gemini)  
  - Logging Agent

- Tools:
  - Mock Lab Reference Tool for basic “low/normal/high” flags
  - Mock EHR API Tool for retrieving previous reports

- Memory:
  - Session store (per patient / case)
  - Simple long-term memory bank

- Observability:
  - Structured logging
  - Basic metrics counters

---

## 2. Architecture

The core pipeline:

1. **IngestionAgent**
   - Cleans raw text
   - Creates/updates a session for the patient or case

2. **SummaryAgent (Gemini)**
   - Produces a 3–5 bullet summary of the report
   - Uses non-diagnostic language and defers to clinician judgment

3. **RiskAgent (Gemini + Lab Tool)**
   - Consumes the cleaned report + summary
   - Uses lab reference ranges and LLM reasoning
   - Outputs: priority (`Low` / `Medium` / `High`), reason, tags

4. **RecommendationAgent (Gemini)**
   - Generates a short explanation and 2–3 review suggestions
   - No explicit diagnosis or treatment advice

5. **LoggingAgent**
   - Records inputs and outputs for each stage

See `/docs/architecture_diagram.png` and `/docs/workflow_diagram.png` for visual diagrams.

---

## 3. Setup

```bash
git clone https://github.com/<your-username>/medintel-agent.git
cd medintel-agent

python -m venv .venv
# Windows:
# .venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
