import uuid
from datetime import datetime
from typing import Any, List, Optional

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import ClinicalEntity


class Inference(ClinicalEntity):
    """An AI-generated or computational inference based on observations/measurements."""

    __tablename__ = "inferences"

    clinical_case_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clinical_cases.id"))
    assessment_session_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("assessment_sessions.id"), nullable=True
    )

    inference_type: Mapped[str] = mapped_column(
        String(100)
    )  # e.g. "trait_elevation", "affective_dysregulation"
    description: Mapped[str] = mapped_column(Text)
    confidence: Mapped[float] = mapped_column(Float)
    evidence_links: Mapped[dict[str, Any]] = mapped_column(
        JSON
    )  # Links to specific observations/measurements


class Formulation(ClinicalEntity):
    """A clinician-authored or clinician-approved case formulation."""

    __tablename__ = "formulations"

    clinical_case_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clinical_cases.id"))
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clinicians.id"))

    biopsychosocial_summary: Mapped[str] = mapped_column(Text)
    personality_functioning_summary: Mapped[str] = mapped_column(Text)
    is_draft: Mapped[bool] = mapped_column(Boolean, default=True)


class DiagnosisRecord(ClinicalEntity):
    __tablename__ = "diagnosis_records"

    clinical_case_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clinical_cases.id"))
    clinician_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clinicians.id"))

    code_system: Mapped[str] = mapped_column(String(50))  # e.g. "ICD-11", "DSM-5-TR"
    code: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(255))
    diagnosed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(50))  # "active", "resolved"


class TreatmentPlan(ClinicalEntity):
    __tablename__ = "treatment_plans"

    clinical_case_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clinical_cases.id"))
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clinicians.id"))

    status: Mapped[str] = mapped_column(String(50))
    goals: Mapped[List["Goal"]] = relationship(back_populates="treatment_plan")
    interventions: Mapped[List["Intervention"]] = relationship(
        back_populates="treatment_plan"
    )


class Goal(ClinicalEntity):
    __tablename__ = "goals"

    treatment_plan_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("treatment_plans.id")
    )
    treatment_plan: Mapped["TreatmentPlan"] = relationship(back_populates="goals")

    description: Mapped[str] = mapped_column(Text)
    target_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(50)
    )  # "in_progress", "achieved", "abandoned"


class Intervention(ClinicalEntity):
    __tablename__ = "interventions"

    treatment_plan_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("treatment_plans.id")
    )
    treatment_plan: Mapped["TreatmentPlan"] = relationship(
        back_populates="interventions"
    )

    intervention_type: Mapped[str] = mapped_column(
        String(100)
    )  # e.g. "CBT", "DBT_skills"
    description: Mapped[str] = mapped_column(Text)
    frequency: Mapped[str] = mapped_column(String(100))


class Outcome(ClinicalEntity):
    __tablename__ = "outcomes"

    clinical_case_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clinical_cases.id"))
    intervention_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("interventions.id"), nullable=True
    )

    date_evaluated: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    measure_used: Mapped[str] = mapped_column(String(100))
    score: Mapped[float] = mapped_column(Float)
    clinical_significance: Mapped[str] = mapped_column(String(100))


class Symptom(ClinicalEntity):
    __tablename__ = "symptoms"

    clinical_case_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clinical_cases.id"))

    name: Mapped[str] = mapped_column(String(100))
    severity: Mapped[str] = mapped_column(String(50))  # "mild", "moderate", "severe"
    onset_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class Trait(ClinicalEntity):
    __tablename__ = "traits"

    clinical_case_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clinical_cases.id"))

    domain: Mapped[str] = mapped_column(String(100))  # e.g. "Negative Affectivity"
    elevation: Mapped[float] = mapped_column(Float)  # Standardized score or percentile


class Facet(ClinicalEntity):
    __tablename__ = "facets"

    trait_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("traits.id"))
    name: Mapped[str] = mapped_column(String(100))  # e.g. "Emotional Lability"
    elevation: Mapped[float] = mapped_column(Float)


class FunctioningDomain(ClinicalEntity):
    __tablename__ = "functioning_domains"

    clinical_case_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clinical_cases.id"))

    domain_name: Mapped[str] = mapped_column(
        String(100)
    )  # e.g. "Identity", "Self-direction", "Empathy", "Intimacy"
    impairment_level: Mapped[int] = mapped_column(Float)  # e.g. Level 0-4 (LPFS)


class Relationship(ClinicalEntity):
    __tablename__ = "relationships"

    patient_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("patients.id"))

    relationship_type: Mapped[str] = mapped_column(
        String(50)
    )  # e.g. "spouse", "parent"
    quality: Mapped[str] = mapped_column(
        String(100)
    )  # e.g. "supportive", "conflictual"


class RiskObservation(ClinicalEntity):
    __tablename__ = "risk_observations"

    clinical_case_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clinical_cases.id"))

    risk_type: Mapped[str] = mapped_column(
        String(100)
    )  # e.g. "suicide", "self_harm", "violence"
    severity: Mapped[str] = mapped_column(String(50))
    imminence: Mapped[str] = mapped_column(String(50))


class ProtectiveFactor(ClinicalEntity):
    __tablename__ = "protective_factors"

    clinical_case_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clinical_cases.id"))

    factor_type: Mapped[str] = mapped_column(
        String(100)
    )  # e.g. "social_support", "insight"
    description: Mapped[str] = mapped_column(Text)
