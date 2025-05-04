from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.models import User, ProjectHasUsers, Project, Task, Assignment
from classes.classes import UserCreate, ProjectSummary, UserInfo
from utils.database import SessionLocal
from utils import validators
from utils.security import hash_password
from sqlalchemy.exc import IntegrityError
from typing import List

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

@router.get("/users/projects", response_model=List[ProjectSummary])
def get_user_projects(
        current_user: User = Depends(get_current_user), # uncomment this line when full release is ready
        db: Session = Depends(get_db)):
    #user_id = 1
    user_id = current_user.UserID

    user = db.query(User).filter(User.UserID == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    project_ids = db.query(ProjectHasUsers.ProjectID).filter(ProjectHasUsers.UserID == user_id).all()
    if not project_ids:
        raise HTTPException(status_code=404, detail="User is not assigned to any projects")

    projects = db.query(Project).filter(Project.ProjectID.in_([pid[0] for pid in project_ids])).all()
    return [ProjectSummary(project_id=p.ProjectID, title=p.title) for p in projects]

@router.get("/users/{user_id}/assignments", response_model=List[str])
def get_user_assignments(
        user_id: int,
        # current_user: User = Depends(get_current_user), # uncomment this line when full release is ready
        db: Session = Depends(get_db)):
    user = db.query(User).filter(User.UserID == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    assignments = db.query(Task).join(Assignment).filter(Assignment.AssigneeID == user_id).all()
    if not assignments:
        raise HTTPException(status_code=404, detail="User is not assigned to any tasks")

    return [task.title for task in assignments]



@router.get("/users/", response_model=List[UserInfo])
def get_all_users(
        #current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"user_id": u.UserID, "username": u.username} for u in users]
