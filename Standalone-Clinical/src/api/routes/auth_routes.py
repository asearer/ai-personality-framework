from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.domain.identity import Clinician
from src.infrastructure.database import get_db
from src.security.auth import create_access_token, verify_password

router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Any:
    clinician = (
        db.query(Clinician).filter(Clinician.email == form_data.username).first()
    )
    if not clinician or not verify_password(
        form_data.password, clinician.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not clinician.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token = create_access_token(data={"sub": clinician.email})
    return {"access_token": access_token, "token_type": "bearer"}
