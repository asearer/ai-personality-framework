import uuid
from datetime import datetime
from typing import Any, List, Optional

from sqlalchemy import JSON, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import ClinicalEntity


class Assessment(ClinicalEntity):
    __tablename__ = "assessments"

    name: Mapped[str] = mapped_column(String(255))
    version: Mapped[str] = mapped_column(String(50))
    instrument_type: Mapped[str] = mapped_column(
        String(100)
    )  # e.g. "self_report", "clinician_administered"


class AssessmentSession(ClinicalEntity):
    __tablename__ = "assessment_sessions"

    assessment_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assessments.id"))
    patient_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("patients.id"))
    encounter_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("encounters.id"), nullable=True
    )

    status: Mapped[str] = mapped_column(String(50))  # "started", "completed", "invalid"
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    observations: Mapped[List["Observation"]] = relationship(back_populates="session")
    measurements: Mapped[List["Measurement"]] = relationship(back_populates="session")


class Observation(ClinicalEntity):
    __tablename__ = "observations"

    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assessment_sessions.id"))
    session: Mapped["AssessmentSession"] = relationship(back_populates="observations")

    source: Mapped[str] = mapped_column(
        String(100)
    )  # e.g. "video_analysis", "audio_analysis", "clinician_rating"
    modality: Mapped[str] = mapped_column(
        String(50)
    )  # e.g. "visual", "acoustic", "text"

    feature_name: Mapped[str] = mapped_column(String(100))
    value_raw: Mapped[str] = mapped_column(Text)
    confidence: Mapped[float] = mapped_column(Float)
    timestamp_offset: Mapped[Optional[float]] = mapped_column(
        Float, nullable=True
    )  # Seconds into session


class Measurement(ClinicalEntity):
    __tablename__ = "measurements"

    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assessment_sessions.id"))
    session: Mapped["AssessmentSession"] = relationship(back_populates="measurements")

    construct: Mapped[str] = mapped_column(
        String(100)
    )  # e.g. "Negative Affect", "Detachment"
    value_numeric: Mapped[float] = mapped_column(Float)
    standard_error: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    normative_sample: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    raw_data: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)
