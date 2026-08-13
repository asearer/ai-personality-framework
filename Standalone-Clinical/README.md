# Standalone Clinical Personality Assessment & Research Platform

A highly secure, architecturally standalone clinical platform designed for rigorous personality assessment, dimensional personality modeling, longitudinal behavioral observation, and computational psychiatry research.

## Project Scope & Purpose

This system is built from the ground up for **clinical and research environments** where patient safety, data privacy, and clinical governance are paramount. 

Unlike experimental or consumer-grade AI systems, this platform enforces a strict epistemic boundary between AI inferences and clinical reality. It is designed to empower human clinicians with structured evidence, measurements, and uncertainty-aware inferences, rather than replacing clinical judgment.

### Core Design Principles

1. **Clinician-in-the-Loop:** The system provides structured evidence and decision support. A qualified human clinician always remains responsible for final clinical interpretations, diagnoses, and treatment plans.
2. **Epistemic Clarity:** The platform strictly distinguishes between:
   - *Observation* (e.g., reduced eye contact)
   - *Measurement* (e.g., self-reported distress score)
   - *Inference* (e.g., possible increase in social avoidance)
   - *Formulation* (e.g., clinician hypothesis)
   - *Diagnosis* (e.g., clinical determination)
   The AI will never silently escalate an observation into a diagnosis.
3. **Absolute Privacy & Security:** Built with strict Role-Based Access Control (RBAC), fine-grained consent management, and data minimization. Patient identities are pseudonymized, ensuring research datasets contain no direct identifiers.

## Technology Stack

The platform is built on a modern, robust Python backend designed for healthcare interoperability, high performance, and strict data integrity.

- **Language:** Python 3.12+ (Strict Type Checking)
- **API Framework:** FastAPI
- **Database / ORM:** SQLAlchemy 2.0 (PostgreSQL / SQLite)
- **Data Validation:** Pydantic V2
- **Testing:** Pytest & Pytest-Asyncio
- **Type Checking:** Mypy

## Domain Architecture

The clinical data model is vast and carefully normalized to represent complex psychological and clinical states. Key architectural domains include:

* **Identity & Access Management:** `Patient`, `Clinician`, `Organization`, `ConsentRecord`, `DataUseAuthorization`
* **Clinical Structure:** `ClinicalCase`, `Encounter`, `ClinicalNote`
* **Assessment Engine:** `Assessment`, `AssessmentSession`, `Observation`, `Measurement`
* **Clinical Reasoning:** `Inference`, `Formulation`, `DiagnosisRecord`, `TreatmentPlan`, `Goal`, `Intervention`, `Outcome`
* **Psychometrics & Functioning:** `Trait`, `Facet`, `FunctioningDomain`, `Symptom`, `Relationship`, `RiskObservation`, `ProtectiveFactor`

## Getting Started

### Prerequisites
- Python 3.10+

### Installation

1. Navigate to the project directory:
   ```bash
   cd Standalone-Clinical
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies (including development tools):
   ```bash
   pip install -e ".[dev]"
   ```

### Running Tests and Type Checks

The project enforces strict type checking and data integrity validation. To verify the environment:

**Run the Pytest Suite:**
```bash
pytest tests/
```
*(This will dynamically build the SQLAlchemy schemas in an in-memory SQLite database to verify all foreign key constraints and relationships.)*

**Run Static Type Checking:**
```bash
mypy src/domain
```

## Security & Ethics

This platform processes highly sensitive clinical data. 
- **Consent:** Explicit, versioned, and revocable consent is tracked for all actions (clinical care, research, audio/video analysis).
- **No Autonomous Diagnosis:** The system is hard-coded to prevent autonomous AI treatment decisions.
- **Auditability:** All clinical notes, formulations, and diagnoses are tied to the specific `Clinician` authoring them, maintaining a strict chain of accountability.
