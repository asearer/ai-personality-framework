import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.api.main import app
from src.domain.base import Base
from src.domain.identity import Clinician
from src.infrastructure.database import get_db
from src.security.auth import get_password_hash

# Setup in-memory SQLite for testing the API
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    # Create test clinician
    clinician = Clinician(
        email="doctor@test.com",
        hashed_password=get_password_hash("password123"),
        full_name="Dr. Test",
        role="Psychiatrist",
        organization_id=uuid.uuid4(),
    )
    db.add(clinician)
    db.commit()
    yield
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_login_success():
    response = client.post(
        "/auth/token", data={"username": "doctor@test.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_failure():
    response = client.post(
        "/auth/token", data={"username": "doctor@test.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401


def test_create_assessment_session_requires_auth():
    response = client.post(
        "/assessments/sessions",
        json={"patient_id": str(uuid.uuid4()), "assessment_id": str(uuid.uuid4())},
    )
    assert response.status_code == 401


def test_create_assessment_session_success():
    # Login
    login_res = client.post(
        "/auth/token", data={"username": "doctor@test.com", "password": "password123"}
    )
    token = login_res.json()["access_token"]

    # Setup test patient and assessment
    patient_id = str(uuid.uuid4())
    assessment_id = str(uuid.uuid4())

    response = client.post(
        "/assessments/sessions",
        headers={"Authorization": f"Bearer {token}"},
        json={"patient_id": patient_id, "assessment_id": assessment_id},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "started"
