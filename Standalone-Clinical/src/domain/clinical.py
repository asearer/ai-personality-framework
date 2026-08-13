import uuid
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .identity import Patient, Clinician

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import ClinicalEntity


class ClinicalCase(ClinicalEntity):
    __tablename__ = "clinical_cases"

    patient_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("patients.id"))
    patient: Mapped["Patient"] = relationship("Patient")

    clinician_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clinicians.id"))
    clinician: Mapped["Clinician"] = relationship("Clinician")

    status: Mapped[str] = mapped_column(
        String(50)
    )  # e.g. "active", "closed", "research_only"

    encounters: Mapped[List["Encounter"]] = relationship(back_populates="clinical_case")
    notes: Mapped[List["ClinicalNote"]] = relationship(back_populates="clinical_case")


class Encounter(ClinicalEntity):
    __tablename__ = "encounters"

    clinical_case_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clinical_cases.id"))
    clinical_case: Mapped["ClinicalCase"] = relationship(back_populates="encounters")

    clinician_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clinicians.id"))

    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ended_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    encounter_type: Mapped[str] = mapped_column(
        String(100)
    )  # e.g. "intake", "follow_up", "assessment"
    location_type: Mapped[str] = mapped_column(
        String(50)
    )  # e.g. "in_person", "telehealth"


class ClinicalNote(ClinicalEntity):
    __tablename__ = "clinical_notes"

    clinical_case_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clinical_cases.id"))
    clinical_case: Mapped["ClinicalCase"] = relationship(back_populates="notes")

    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clinicians.id"))

    note_type: Mapped[str] = mapped_column(String(100))
    content_encrypted: Mapped[str] = mapped_column(Text)
    is_signed: Mapped[bool] = mapped_column(default=False)
    signed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
