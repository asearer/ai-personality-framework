import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.domain.assessment import (Assessment, AssessmentSession,  # noqa: F401
                                   Measurement, Observation)
from src.domain.base import Base
from src.domain.clinical import (ClinicalCase, ClinicalNote,  # noqa: F401
                                 Encounter)
# Import all models to ensure they are registered with Base.metadata
from src.domain.identity import (Clinician, ConsentRecord,  # noqa: F401
                                 DataUseAuthorization, Organization, Patient)
from src.domain.reasoning import (DiagnosisRecord, Facet,  # noqa: F401
                                  Formulation, FunctioningDomain, Goal,
                                  Inference, Intervention, Outcome,
                                  ProtectiveFactor, Relationship,
                                  RiskObservation, Symptom, Trait,
                                  TreatmentPlan)


@pytest.fixture
def db_session():
    # Use SQLite in-memory database for testing model schema creation
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


def test_create_organization_and_clinician(db_session):
    org = Organization(name="Test Clinic")
    db_session.add(org)
    db_session.flush()

    clinician = Clinician(
        email="doctor@test.com",
        hashed_password="hashed",
        full_name="Dr. Test",
        role="Psychiatrist",
        organization=org,
    )
    db_session.add(clinician)
    db_session.commit()

    assert clinician.id is not None
    assert clinician.organization.name == "Test Clinic"


def test_create_patient_and_case(db_session):
    org = Organization(name="Research Center")
    clinician = Clinician(
        email="researcher@test.com",
        hashed_password="hash",
        full_name="Dr. Researcher",
        role="Researcher",
        organization=org,
    )
    patient = Patient(pseudonym="SUBJ-001")

    db_session.add_all([org, clinician, patient])
    db_session.flush()

    clinical_case = ClinicalCase(
        patient=patient, clinician_id=clinician.id, status="active"
    )
    db_session.add(clinical_case)
    db_session.commit()

    assert clinical_case.id is not None
    assert clinical_case.patient.pseudonym == "SUBJ-001"
