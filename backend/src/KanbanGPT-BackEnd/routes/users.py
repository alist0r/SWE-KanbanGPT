from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.models import User
from classes.classes import UserCreate
from utils.database import SessionLocal
from utils import validators
from utils.security import hash_password
from sqlalchemy.exc import IntegrityError

# Import the JWT-based authentication dependency
from utils.auth import get_current_user

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
    ):
    '''
    Utilizes the create_user model from classes.py
    accepts:
    - username (str)
    - password (str)
    - email (str)
    - name (str)

    calls validation functions from validators.py
    queries database to ensure user name and email aren't used already

    hashes the password
    creates a User object from the pparse data

    trys adding the user, commits to db, and refreshes

    '''
    if not validators.is_valid_username(user.username):
        raise HTTPException(status_code=400, detail="Username must be between 8 and 32 characters and alphanumeric.")

    if not validators.is_valid_password(user.password):
        raise HTTPException(status_code=400, detail="Password must be 6–12 characters with at least one letter, number, and special character.")

    if not validators.is_valid_email_format(user.email):
        raise HTTPException(status_code=400, detail="Invalid email format.")

    if not validators.is_valid_name(user.name):
        raise HTTPException(status_code=400, detail="Name must only contain letters and spaces.")

    # Check if email exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    # Check if username is taken
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already taken.")

    hashed_pw = hash_password(user.password)

    new_user = User(
        username=user.username,
        password=hashed_pw,
        email=user.email,
        name=user.name
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database integrity error.")

    return {"message": "User created successfully", "user_id": new_user.UserID}

