from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from utils.util import (
    verify_password,
    create_access_token,
    create_refresh_token,
)
import models.models  # your user model should be in here
from utils.database import SessionLocal

router = APIRouter()

# Dependency to get a database session.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # Look up the user by username
    user = db.query(models.models.User).filter(
        models.models.User.username == form_data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Verify the provided password
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate tokens using your utility functions
    access_token = create_access_token(subject=user.username)
    refresh_token = create_refresh_token(subject=user.username)

    # Return tokens with a token type (bearer)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
