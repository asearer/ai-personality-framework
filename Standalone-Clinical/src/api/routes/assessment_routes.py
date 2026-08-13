import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from src.domain.assessment import AssessmentSession, Observation
from src.domain.identity import Clinician
from src.infrastructure.database import get_db
from src.security.audit import log_clinical_action
from src.security.auth import get_current_clinician

router = APIRouter(prefix="/assessments/sessions", tags=["assessments"])


class SessionCreate(BaseModel):
    patient_id: uuid.UUID
    assessment_id: uuid.UUID
    encounter_id: Optional[uuid.UUID] = None


class SessionResponse(BaseModel):
    id: uuid.UUID
    patient_id: uuid.UUID
    status: str
    started_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ObservationCreate(BaseModel):
    source: str
    modality: str
    feature_name: str
    value_raw: str
    confidence: float
    timestamp_offset: Optional[float] = None


@router.post("", response_model=SessionResponse)
def start_session(
    session_data: SessionCreate,
    db: Session = Depends(get_db),
    current_clinician: Clinician = Depends(get_current_clinician),
) -> Any:
    session = AssessmentSession(
        patient_id=session_data.patient_id,
        assessment_id=session_data.assessment_id,
        encounter_id=session_data.encounter_id,
        status="started",
        started_at=datetime.now(timezone.utc),
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    log_clinical_action(
        clinician_id=current_clinician.id,
        action="START_ASSESSMENT_SESSION",
        target_entity="AssessmentSession",
        target_id=session.id,
        details={"patient_id": str(session.patient_id)},
    )
    return session


@router.post("/{session_id}/observations")
def add_observation(
    session_id: uuid.UUID,
    obs_data: ObservationCreate,
    db: Session = Depends(get_db),
    current_clinician: Clinician = Depends(get_current_clinician),
) -> Any:
    session = (
        db.query(AssessmentSession).filter(AssessmentSession.id == session_id).first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    obs = Observation(session_id=session_id, **obs_data.model_dump())
    db.add(obs)
    db.commit()
    db.refresh(obs)

    log_clinical_action(
        clinician_id=current_clinician.id,
        action="ADD_OBSERVATION",
        target_entity="Observation",
        target_id=obs.id,
        details={"session_id": str(session_id), "feature": obs.feature_name},
    )
    return {"id": obs.id, "status": "recorded"}
