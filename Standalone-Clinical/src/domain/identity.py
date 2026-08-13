import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import ClinicalEntity


class Organization(ClinicalEntity):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    clinicians: Mapped[List["Clinician"]] = relationship(back_populates="organization")


class Clinician(ClinicalEntity):
    __tablename__ = "clinicians"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(
        String(50)
    )  # e.g. Psychiatrist, Psychologist, Researcher
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    organization: Mapped["Organization"] = relationship(back_populates="clinicians")


class Patient(ClinicalEntity):
    __tablename__ = "patients"

    # Minimal PII, often pseudonymous in research contexts
    pseudonym: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    date_of_birth: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    consents: Mapped[List["ConsentRecord"]] = relationship(back_populates="patient")


class ConsentRecord(ClinicalEntity):
    __tablename__ = "consent_records"

    patient_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("patients.id"))
    patient: Mapped["Patient"] = relationship(back_populates="consents")

    consent_type: Mapped[str] = mapped_column(
        String(100)
    )  # e.g. "research", "clinical_care"
    is_granted: Mapped[bool] = mapped_column(Boolean, default=False)
    granted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    revoked_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    version: Mapped[str] = mapped_column(String(50))


class DataUseAuthorization(ClinicalEntity):
    __tablename__ = "data_use_authorizations"

    patient_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("patients.id"))
    purpose: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
